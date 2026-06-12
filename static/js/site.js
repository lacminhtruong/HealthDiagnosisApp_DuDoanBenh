function normalizeText(value) {
    return String(value || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLocaleLowerCase("vi")
        .trim();
}

function setupSymptomSearch() {
    const searchInput = document.getElementById("symptom-search");
    const resultCount = document.getElementById("search-result-count");
    const emptyState = document.getElementById("search-empty");
    const groups = [...document.querySelectorAll("[data-symptom-group]")];

    if (!searchInput || !groups.length) {
        return;
    }

    const filterSymptoms = () => {
        const query = normalizeText(searchInput.value);
        let totalVisible = 0;

        groups.forEach((group) => {
            const options = [...group.querySelectorAll("[data-symptom-option]")];
            let visibleCount = 0;

            options.forEach((option) => {
                const haystack = normalizeText(option.dataset.symptomName || option.textContent);
                const isVisible = !query || haystack.includes(query);
                option.hidden = !isVisible;
                if (isVisible) {
                    visibleCount += 1;
                    totalVisible += 1;
                }
            });

            group.hidden = Boolean(query) && visibleCount === 0;
        });

        if (resultCount) {
            resultCount.textContent = `${totalVisible} kết quả`;
        }
        if (emptyState) {
            emptyState.hidden = totalVisible > 0;
        }
    };

    searchInput.addEventListener("input", filterSymptoms);
    document.addEventListener("keydown", (event) => {
        if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
            event.preventDefault();
            searchInput.focus();
            searchInput.select();
        }
    });
    filterSymptoms();
}

function syncPatientPreview() {
    const checkboxes = [...document.querySelectorAll("input[name='symptoms']")];
    const selectedCount = document.getElementById("selected-count");
    const selectedCountSide = document.getElementById("selected-count-side");
    const selectedList = document.getElementById("selected-symptom-list");
    const heightInput = document.getElementById("height-input");
    const weightInput = document.getElementById("weight-input");
    const bmiPreview = document.getElementById("bmi-preview");
    const bmiLabel = document.getElementById("bmi-label");

    if (!checkboxes.length) {
        return;
    }

    const updateSymptoms = () => {
        const selected = checkboxes
            .filter((checkbox) => checkbox.checked)
            .map((checkbox) => checkbox.value);

        if (selectedCount) {
            selectedCount.textContent = selected.length;
        }
        if (selectedCountSide) {
            selectedCountSide.textContent = selected.length;
        }

        if (!selectedList) {
            return;
        }

        selectedList.replaceChildren();
        if (!selected.length) {
            const emptyChip = document.createElement("span");
            emptyChip.className = "muted-chip";
            emptyChip.textContent = "Chưa chọn triệu chứng";
            selectedList.appendChild(emptyChip);
            return;
        }

        selected.forEach((symptom) => {
            const chip = document.createElement("span");
            chip.textContent = symptom;
            selectedList.appendChild(chip);
        });
    };

    const updateBmi = () => {
        if (!heightInput || !weightInput || !bmiPreview) {
            return;
        }

        const height = Number(heightInput.value);
        const weight = Number(weightInput.value);
        if (height <= 0 || weight <= 0) {
            bmiPreview.textContent = "--";
            if (bmiLabel) {
                bmiLabel.textContent = "Nhập chiều cao và cân nặng";
            }
            return;
        }

        const heightInMeters = height / 100;
        const bmi = weight / (heightInMeters * heightInMeters);
        bmiPreview.textContent = bmi.toFixed(2);
        if (bmiLabel) {
            if (bmi < 18.5) {
                bmiLabel.textContent = "Mức cân nặng thấp";
            } else if (bmi < 25) {
                bmiLabel.textContent = "Trong ngưỡng cân đối";
            } else if (bmi < 30) {
                bmiLabel.textContent = "Mức thừa cân";
            } else {
                bmiLabel.textContent = "Mức BMI cao";
            }
        }
    };

    checkboxes.forEach((checkbox) => checkbox.addEventListener("change", updateSymptoms));
    [heightInput, weightInput].forEach((input) => {
        if (input) {
            input.addEventListener("input", updateBmi);
        }
    });

    updateSymptoms();
    updateBmi();
}

function drawNeighborChart() {
    const canvas = document.getElementById("neighbor-chart");
    const dataElement = document.getElementById("chart-data");

    if (!canvas || !dataElement) {
        return;
    }

    const values = JSON.parse(dataElement.textContent);
    const entries = Object.entries(values)
        .map(([label, percentage]) => [label, Number(percentage)])
        .filter(([, percentage]) => percentage > 0);

    if (!entries.length) {
        return;
    }

    const context = canvas.getContext("2d");
    const ratio = window.devicePixelRatio || 1;
    const cssWidth = canvas.clientWidth || 560;
    const isCompact = cssWidth < 520;
    const cssHeight = isCompact ? 390 : 300;

    canvas.width = Math.round(cssWidth * ratio);
    canvas.height = Math.round(cssHeight * ratio);
    canvas.style.height = `${cssHeight}px`;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    context.clearRect(0, 0, cssWidth, cssHeight);

    const colors = ["#0d9488", "#3b82f6", "#d28a2e", "#d95f75", "#7760c9", "#2588a8"];
    const total = entries.reduce((sum, [, percentage]) => sum + percentage, 0);
    const maxEntry = entries.reduce((best, entry) => (entry[1] > best[1] ? entry : best), entries[0]);

    const centerX = isCompact ? cssWidth / 2 : 145;
    const centerY = isCompact ? 118 : 150;
    const radius = isCompact ? 88 : 96;
    const innerRadius = radius * 0.62;
    let startAngle = -Math.PI / 2;

    entries.forEach(([, percentage], index) => {
        const sliceAngle = (percentage / total) * Math.PI * 2;
        context.beginPath();
        context.moveTo(centerX, centerY);
        context.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
        context.closePath();
        context.fillStyle = colors[index % colors.length];
        context.fill();
        startAngle += sliceAngle;
    });

    context.beginPath();
    context.arc(centerX, centerY, innerRadius, 0, Math.PI * 2);
    context.fillStyle = "#ffffff";
    context.fill();

    context.fillStyle = "#0d9488";
    context.font = "800 28px Segoe UI, Arial";
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.fillText(`${maxEntry[1]}%`, centerX, centerY - 7);
    context.fillStyle = "#6a7f8e";
    context.font = "800 12px Segoe UI, Arial";
    context.fillText("cao nhất", centerX, centerY + 22);

    const legendX = isCompact ? 20 : 300;
    const legendStartY = isCompact ? 250 : 76;
    const legendWidth = isCompact ? cssWidth - 40 : cssWidth - legendX - 20;
    const rowHeight = 34;

    entries.forEach(([label, percentage], index) => {
        const y = legendStartY + index * rowHeight;

        context.fillStyle = colors[index % colors.length];
        roundRect(context, legendX, y - 11, 12, 12, 4);
        context.fill();

        context.fillStyle = "#102536";
        context.font = "800 13px Segoe UI, Arial";
        context.textAlign = "left";
        context.textBaseline = "middle";
        context.fillText(trimText(context, label, Math.max(80, legendWidth - 58)), legendX + 22, y - 5);

        context.fillStyle = "#0d9488";
        context.textAlign = "right";
        context.fillText(`${percentage}%`, legendX + legendWidth, y - 5);
    });
}

function trimText(context, text, maxWidth) {
    if (context.measureText(text).width <= maxWidth) {
        return text;
    }

    let trimmed = text;
    while (trimmed.length > 1 && context.measureText(`${trimmed}...`).width > maxWidth) {
        trimmed = trimmed.slice(0, -1);
    }
    return `${trimmed}...`;
}

function roundRect(context, x, y, width, height, radius) {
    const safeRadius = Math.min(radius, width / 2, height / 2);
    context.beginPath();
    context.moveTo(x + safeRadius, y);
    context.lineTo(x + width - safeRadius, y);
    context.quadraticCurveTo(x + width, y, x + width, y + safeRadius);
    context.lineTo(x + width, y + height - safeRadius);
    context.quadraticCurveTo(x + width, y + height, x + width - safeRadius, y + height);
    context.lineTo(x + safeRadius, y + height);
    context.quadraticCurveTo(x, y + height, x, y + height - safeRadius);
    context.lineTo(x, y + safeRadius);
    context.quadraticCurveTo(x, y, x + safeRadius, y);
    context.closePath();
}

document.addEventListener("DOMContentLoaded", () => {
    setupSymptomSearch();
    syncPatientPreview();
    drawNeighborChart();
});

window.addEventListener("resize", () => {
    window.clearTimeout(window.neighborChartResizeTimer);
    window.neighborChartResizeTimer = window.setTimeout(drawNeighborChart, 120);
});
