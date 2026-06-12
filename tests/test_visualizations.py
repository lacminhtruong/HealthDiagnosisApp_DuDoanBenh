import unittest

from visualizations import build_rule_metrics_chart_html, build_rule_network_html, load_matching_rules


class AssociationVisualizationTest(unittest.TestCase):
    symptoms = ["Chảy nước mắt", "Đổ ghèn"]

    def test_loads_rules_matching_all_selected_antecedents(self):
        selected, rules = load_matching_rules(self.symptoms)

        self.assertTrue(selected)
        self.assertTrue(rules)
        self.assertTrue(all(set(rule["antecedents"]).issubset(set(selected)) for rule in rules))

    def test_builds_interactive_pyvis_network_html(self):
        html = build_rule_network_html(self.symptoms)

        self.assertIn("vis-network", html)
        self.assertIn("arrows", html)
        self.assertIn("#dc3545", html)
        self.assertIn("#18a67e", html)

    def test_builds_interactive_plotly_html(self):
        html = build_rule_metrics_chart_html(self.symptoms)

        self.assertIn("plotly", html.lower())
        self.assertIn("responsive", html)


if __name__ == "__main__":
    unittest.main()
