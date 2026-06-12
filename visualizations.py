from __future__ import annotations

import json
import math
from pathlib import Path
import unicodedata

import networkx as nx
import plotly.graph_objects as go
from pyvis.network import Network


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_ASSOCIATION_RULES_PATH = PROJECT_ROOT / "trained_models" / "association_rules_meta.json"


def normalize_text(value: object) -> str:
    return " ".join(unicodedata.normalize("NFC", str(value or "")).strip().split()).casefold()


def load_matching_rules(
    selected_symptoms: list[str],
    rules_path: Path = DEFAULT_ASSOCIATION_RULES_PATH,
    limit: int = 12,
) -> tuple[list[str], list[dict[str, object]]]:
    if not rules_path.exists():
        return [], []

    try:
        artifact = json.loads(rules_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [], []

    symptom_lookup: dict[str, str] = {}
    prepared_rules: list[dict[str, object]] = []
    for rule in artifact.get("rules", []):
        antecedents = _clean_symptoms(rule.get("antecedents"))
        consequents = _clean_symptoms(rule.get("consequents"))
        if not antecedents or not consequents:
            continue

        for symptom in [*antecedents, *consequents]:
            symptom_lookup.setdefault(normalize_text(symptom), symptom)

        prepared_rules.append(
            {
                "antecedents": antecedents,
                "antecedent_keys": {normalize_text(symptom) for symptom in antecedents},
                "consequents": consequents,
                "confidence_percent": float(rule.get("confidence_percent", 0)),
                "support_percent": float(rule.get("support_percent", 0)),
                "lift": float(rule.get("lift", 0)),
            }
        )

    selected_keys = {
        normalize_text(symptom)
        for symptom in selected_symptoms
        if normalize_text(symptom) in symptom_lookup
    }
    canonical_selected = [
        symptom_lookup[key]
        for key in selected_keys
    ]
    matched_rules: list[dict[str, object]] = []

    for rule in prepared_rules:
        if not rule["antecedent_keys"].issubset(selected_keys):
            continue

        suggested = [
            symptom
            for symptom in rule["consequents"]
            if normalize_text(symptom) not in selected_keys
        ]
        if not suggested:
            continue

        matched_rules.append({**rule, "suggested": suggested})

    matched_rules.sort(
        key=lambda rule: (
            len(rule["antecedents"]),
            rule["confidence_percent"],
            rule["lift"],
            rule["support_percent"],
        ),
        reverse=True,
    )
    return canonical_selected, matched_rules[:limit]


def build_rule_network_html(
    selected_symptoms: list[str],
    rules_path: Path = DEFAULT_ASSOCIATION_RULES_PATH,
) -> str:
    selected, matched_rules = load_matching_rules(selected_symptoms, rules_path, limit=18)
    graph = nx.DiGraph()

    for symptom in selected:
        graph.add_node(
            symptom,
            label=symptom,
            title="Triệu chứng người dùng đã chọn",
            color="#dc3545",
            size=28,
            shape="dot",
            level=0,
            font={"color": "#102536", "size": 15, "face": "Manrope"},
        )

    for rule in matched_rules:
        for consequent in rule["suggested"]:
            graph.add_node(
                consequent,
                label=consequent,
                title="Triệu chứng liên quan được luật kết hợp gợi ý",
                color="#18a67e",
                size=21,
                shape="dot",
                level=1,
                font={"color": "#102536", "size": 13, "face": "Manrope"},
            )
            for antecedent in rule["antecedents"]:
                edge_data = {
                    "confidence_percent": rule["confidence_percent"],
                    "support_percent": rule["support_percent"],
                    "lift": rule["lift"],
                }
                existing = graph.get_edge_data(antecedent, consequent)
                if existing and existing.get("confidence_percent", 0) >= rule["confidence_percent"]:
                    continue

                graph.add_edge(
                    antecedent,
                    consequent,
                    **edge_data,
                    title=(
                        f"Confidence: {rule['confidence_percent']:.2f}% | "
                        f"Support: {rule['support_percent']:.2f}% | Lift: {rule['lift']:.3f}"
                    ),
                    width=max(1.5, min(8.0, rule["confidence_percent"] / 14)),
                    color="#5ab8a0",
                    arrows="to",
                )

    selected_set = set(selected)
    related = [node for node in graph.nodes if node not in selected_set]
    for index, symptom in enumerate(selected):
        angle = (2 * math.pi * index / max(1, len(selected))) - math.pi / 2
        graph.nodes[symptom]["x"] = round(math.cos(angle) * 65, 2)
        graph.nodes[symptom]["y"] = round(math.sin(angle) * 65, 2)

    for index, symptom in enumerate(related):
        angle = (2 * math.pi * index / max(1, len(related))) - math.pi / 2
        graph.nodes[symptom]["x"] = round(math.cos(angle) * 310, 2)
        graph.nodes[symptom]["y"] = round(math.sin(angle) * 230, 2)

    network = Network(
        height="480px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#102536",
        cdn_resources="remote",
    )
    network.from_nx(graph)
    network.set_options(
        """
        {
          "layout": {"improvedLayout": true, "randomSeed": 12},
          "physics": {"enabled": false},
          "interaction": {"hover": true, "navigationButtons": true, "keyboard": true},
          "edges": {"smooth": {"enabled": true, "type": "cubicBezier"}, "arrowStrikethrough": false}
        }
        """
    )
    return network.generate_html(name="association-rule-network.html", notebook=False)


def build_rule_metrics_chart_html(
    selected_symptoms: list[str],
    rules_path: Path = DEFAULT_ASSOCIATION_RULES_PATH,
) -> str:
    _, matched_rules = load_matching_rules(selected_symptoms, rules_path)
    figure = go.Figure()

    if matched_rules:
        labels = [
            " + ".join(rule["suggested"])
            for rule in matched_rules
        ]
        hover_text = [
            (
                f"Nếu có: {', '.join(rule['antecedents'])}<br>"
                f"Gợi ý: {', '.join(rule['suggested'])}<br>"
                f"Confidence: {rule['confidence_percent']:.2f}%<br>"
                f"Support: {rule['support_percent']:.2f}%<br>"
                f"Lift: {rule['lift']:.3f}"
            )
            for rule in matched_rules
        ]
        max_lift = max(rule["lift"] for rule in matched_rules) or 1
        sizes = [14 + (rule["lift"] / max_lift) * 26 for rule in matched_rules]

        figure.add_trace(
            go.Scatter(
                x=[rule["confidence_percent"] for rule in matched_rules],
                y=[rule["support_percent"] for rule in matched_rules],
                mode="markers+text",
                text=labels,
                textposition="top center",
                customdata=hover_text,
                hovertemplate="%{customdata}<extra></extra>",
                marker={
                    "size": sizes,
                    "color": [rule["lift"] for rule in matched_rules],
                    "colorscale": "Tealgrn",
                    "showscale": True,
                    "colorbar": {"title": "Lift", "thickness": 12},
                    "line": {"color": "#ffffff", "width": 1.5},
                    "opacity": 0.88,
                },
            )
        )
    else:
        figure.add_annotation(
            text="Chưa có luật kết hợp phù hợp với các triệu chứng đã chọn.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font={"size": 15, "color": "#6a7f8e"},
        )

    figure.update_layout(
        height=480,
        margin={"l": 62, "r": 32, "t": 24, "b": 58},
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f6fafc",
        font={"family": "Manrope, Segoe UI, Arial", "color": "#102536"},
        hoverlabel={"bgcolor": "#0a2135", "font": {"color": "#ffffff"}},
        xaxis={
            "title": "Confidence (%)",
            "range": [0, 105],
            "gridcolor": "#dce8ec",
            "zeroline": False,
        },
        yaxis={
            "title": "Support (%)",
            "rangemode": "tozero",
            "gridcolor": "#dce8ec",
            "zeroline": False,
        },
        showlegend=False,
    )
    return figure.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config={"responsive": True, "displaylogo": False},
    )


def _clean_symptoms(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    return [
        " ".join(unicodedata.normalize("NFC", str(value)).strip().split())
        for value in values
        if str(value).strip()
    ]
