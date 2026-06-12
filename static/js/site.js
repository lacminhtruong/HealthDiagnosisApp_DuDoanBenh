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
    const dockSelectedCount = document.getElementById("dock-selected-count");
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
        if (dockSelectedCount) {
            dockSelectedCount.textContent = selected.length;
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

function setupSmartSuggestions() {
    const checkboxes = [...document.querySelectorAll("input[name='symptoms']")];
    const suggestionBox = document.getElementById("suggestion-box");
    const suggestionTags = suggestionBox?.querySelector("[data-suggestion-tags]");
    const suggestionMessage = suggestionBox?.querySelector("[data-suggestion-message]");
    const loadingLabel = suggestionBox?.querySelector("[data-suggestion-loading]");
    const toggleButton = suggestionBox?.querySelector("[data-suggestion-toggle]");
    const searchInput = document.getElementById("symptom-search");

    if (!checkboxes.length || !suggestionBox || !suggestionTags || !suggestionMessage) {
        return;
    }

    const checkboxBySymptom = new Map(
        checkboxes.map((checkbox) => [normalizeText(checkbox.value), checkbox]),
    );
    let activeRequest;

    const toggleSuggestionBox = () => {
        const isCollapsed = suggestionBox.classList.toggle("is-collapsed");
        if (toggleButton) {
            toggleButton.setAttribute("aria-expanded", String(!isCollapsed));
            toggleButton.title = isCollapsed ? "Mở rộng gợi ý" : "Thu gọn gợi ý";
        }
    };

    const showMessage = (message) => {
        suggestionTags.replaceChildren();
        suggestionMessage.textContent = message;
        suggestionMessage.hidden = false;
    };

    const selectSuggestion = (symptom) => {
        const checkbox = checkboxBySymptom.get(normalizeText(symptom));
        if (!checkbox || checkbox.checked) {
            return;
        }

        if (searchInput?.value) {
            searchInput.value = "";
            searchInput.dispatchEvent(new Event("input", { bubbles: true }));
        }

        checkbox.checked = true;
        checkbox.dispatchEvent(new Event("change", { bubbles: true }));
        const option = checkbox.closest("[data-symptom-option]");
        option?.classList.remove("suggestion-selected");
        window.requestAnimationFrame(() => option?.classList.add("suggestion-selected"));
        option?.scrollIntoView({ behavior: "smooth", block: "center" });
    };

    const renderSuggestions = (details) => {
        suggestionTags.replaceChildren();
        suggestionMessage.hidden = true;

        const availableDetails = details.filter((suggestion) => (
            checkboxBySymptom.has(normalizeText(suggestion.symptom))
        ));
        if (!availableDetails.length) {
            showMessage("Chưa có gợi ý phù hợp cho tổ hợp triệu chứng hiện tại.");
            return;
        }

        availableDetails.forEach((suggestion) => {
            const tag = document.createElement("button");
            tag.className = "suggestion-tag";
            tag.type = "button";
            tag.title = `Độ tin cậy ${suggestion.confidence_percent}%`;

            const label = document.createTextNode(suggestion.symptom);
            const confidence = document.createElement("span");
            confidence.textContent = `+ ${suggestion.confidence_percent}%`;
            tag.append(label, confidence);
            tag.addEventListener("click", () => selectSuggestion(suggestion.symptom));
            suggestionTags.appendChild(tag);
        });
    };

    const loadSuggestions = async () => {
        const selectedSymptoms = checkboxes
            .filter((checkbox) => checkbox.checked)
            .map((checkbox) => checkbox.value);

        activeRequest?.abort();
        if (!selectedSymptoms.length) {
            suggestionBox.hidden = true;
            return;
        }

        const requestController = new AbortController();
        activeRequest = requestController;
        suggestionBox.hidden = false;
        if (loadingLabel) {
            loadingLabel.hidden = false;
        }
        suggestionMessage.hidden = true;

        try {
            const response = await fetch(suggestionBox.dataset.suggestionUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ symptoms: selectedSymptoms }),
                signal: requestController.signal,
            });
            if (!response.ok) {
                throw new Error(`Suggestion API returned ${response.status}`);
            }

            const payload = await response.json();
            renderSuggestions(Array.isArray(payload.details) ? payload.details : []);
        } catch (error) {
            if (error.name !== "AbortError") {
                showMessage("Chưa thể tải gợi ý lúc này. Bạn vẫn có thể tiếp tục chọn triệu chứng.");
            }
        } finally {
            if (activeRequest === requestController && loadingLabel) {
                loadingLabel.hidden = true;
            }
        }
    };

    checkboxes.forEach((checkbox) => checkbox.addEventListener("change", loadSuggestions));
    toggleButton?.addEventListener("click", toggleSuggestionBox);
    loadSuggestions();
}

function setupSubmitDock() {
    const submitButton = document.querySelector("[data-primary-submit]");
    const submitDock = document.querySelector("[data-submit-dock]");
    const selectedCard = document.querySelector(".selected-card");

    if (!submitButton || !submitDock) {
        return;
    }

    let buttonIsVisible = false;
    let updateFrame;

    const updateDockVisibility = () => {
        const selectedRect = selectedCard?.getBoundingClientRect();
        const dockBottom = Number.parseFloat(window.getComputedStyle(submitDock).bottom) || 0;
        const dockTop = window.innerHeight - dockBottom - submitDock.offsetHeight;
        const overlapsSelection = window.innerWidth <= 1120
            && selectedRect
            && selectedRect.bottom > dockTop - 12
            && selectedRect.top < window.innerHeight - dockBottom + 12;

        submitDock.classList.toggle("is-visible", !buttonIsVisible && !overlapsSelection);
    };

    const scheduleDockUpdate = () => {
        window.cancelAnimationFrame(updateFrame);
        updateFrame = window.requestAnimationFrame(updateDockVisibility);
    };

    if (!("IntersectionObserver" in window)) {
        window.addEventListener("scroll", scheduleDockUpdate, { passive: true });
        window.addEventListener("resize", scheduleDockUpdate);
        updateDockVisibility();
        return;
    }

    const observer = new IntersectionObserver(
        ([entry]) => {
            buttonIsVisible = entry.isIntersecting;
            scheduleDockUpdate();
        },
        { threshold: 0.7, rootMargin: "-76px 0px -12px" },
    );
    observer.observe(submitButton);
    window.addEventListener("scroll", scheduleDockUpdate, { passive: true });
    window.addEventListener("resize", scheduleDockUpdate);
    updateDockVisibility();
}

function drawNeighborChart(progress = 1) {
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
        const sliceAngle = (percentage / total) * Math.PI * 2 * progress;
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
    context.fillText(`${Math.round(maxEntry[1] * progress)}%`, centerX, centerY - 7);
    context.fillStyle = "#6a7f8e";
    context.font = "800 12px Segoe UI, Arial";
    context.fillText("cao nhất", centerX, centerY + 22);

    const legendX = isCompact ? 20 : 300;
    const legendStartY = isCompact ? 250 : 76;
    const legendWidth = isCompact ? cssWidth - 40 : cssWidth - legendX - 20;
    const rowHeight = 34;

    context.globalAlpha = Math.min(1, progress * 1.6);
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
    context.globalAlpha = 1;
}

function animateResultVisuals() {
    const confidenceRing = document.querySelector(".confidence-ring");
    const confidenceNumber = document.querySelector("[data-count-up]");
    const voteCard = document.querySelector(".vote-card");
    const chartCard = document.querySelector(".chart-card");
    const canvas = document.getElementById("neighbor-chart");

    if (!confidenceRing && !voteCard && !chartCard) {
        return;
    }

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const duration = reducedMotion ? 1 : 1250;
    const targetScore = Number(confidenceRing?.dataset.score || 0);
    let started = false;

    const easeOutCubic = (value) => 1 - Math.pow(1 - value, 3);
    const startAnimations = () => {
        if (started) {
            return;
        }
        started = true;
        confidenceRing?.classList.add("is-animated");
        voteCard?.classList.add("is-animated");
        chartCard?.classList.add("is-animated");

        const startedAt = performance.now();
        const animateFrame = (now) => {
            const progress = Math.min(1, (now - startedAt) / duration);
            const easedProgress = easeOutCubic(progress);

            confidenceRing?.style.setProperty("--ring-progress", targetScore * easedProgress);
            if (confidenceNumber) {
                confidenceNumber.textContent = `${Math.round(targetScore * easedProgress)}%`;
            }
            if (canvas) {
                drawNeighborChart(easedProgress);
            }

            if (progress < 1) {
                requestAnimationFrame(animateFrame);
            }
        };
        requestAnimationFrame(animateFrame);
    };

    if (!("IntersectionObserver" in window)) {
        startAnimations();
        return;
    }

    const target = confidenceRing || document.querySelector(".result-grid-primary");
    const observer = new IntersectionObserver(
        ([entry]) => {
            if (entry.isIntersecting) {
                startAnimations();
                observer.disconnect();
            }
        },
        { threshold: 0.18 },
    );
    if (target) {
        observer.observe(target);
    }
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
    setupSmartSuggestions();
    setupSubmitDock();
    animateResultVisuals();
});

window.addEventListener("resize", () => {
    window.clearTimeout(window.neighborChartResizeTimer);
    window.neighborChartResizeTimer = window.setTimeout(() => drawNeighborChart(1), 120);
});
