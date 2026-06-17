function initQAGenEvents() {
    const radios = document.querySelectorAll('input[name="qaMode"]');
    radios.forEach(radio => {
        radio.addEventListener('change', function () {
            const isPdf = this.value === 'pdf';
            document.getElementById('qaPdfSection').style.display = isPdf ? 'block' : 'none';
            document.getElementById('qaTextSection').style.display = isPdf ? 'none' : 'block';
        });
    });
}

function renderQAPairs(pairs) {
    const resultDiv = document.getElementById("qaResult");
    resultDiv.innerHTML = ""; // Clear previous results

    pairs.forEach((pair, index) => {
        const card = document.createElement("div");
        card.className = "card border-0 shadow-sm mb-4 rounded-4";

        // Card header with gradient styling
        const cardHeader = document.createElement("div");
        cardHeader.className = "card-header text-black rounded-top-4";
        cardHeader.innerHTML = `<strong>Q${index + 1}:</strong> ${pair.key}`;

        // Card body
        const cardBody = document.createElement("div");
        cardBody.className = "card-body";

        const answer = document.createElement("p");
        answer.className = "card-text mb-0";
        answer.innerHTML = `<strong class="text-secondary">A:</strong> ${pair.value}`;

        // Append elements
        cardBody.appendChild(answer);
        card.appendChild(cardHeader);
        card.appendChild(cardBody);
        resultDiv.appendChild(card);
    });
}


async function submitQAGen() {
    const mode = document.querySelector('input[name="qaMode"]:checked').value;
    const resultDiv = document.getElementById("qaResult");
    resultDiv.innerHTML = "";
    const n = parseInt(document.getElementById("qaN").value, 10);
    const btn = document.getElementById("qaSubmitBtn");

    if (isNaN(n) || n <= 0) {
        resultDiv.innerHTML = `
        <div class="alert alert-warning">
            Enter a valid number of questions.
        </div>`;
        return;
    }
    btn.disabled = true;

    try {
        if (mode === "pdf") {
            const fileInput = document.getElementById("qaFile");
            const file = fileInput.files[0];

            if (!file) {
                resultDiv.innerHTML = `<div class="alert alert-warning" role="alert">
                    Please upload a PDF file.
                </div>`;
                return;
            }

            if (file.type !== "application/pdf") {
                resultDiv.innerHTML = `
                    <div class="alert alert-warning">
                        Please upload a PDF file.
                    </div>`;
                return;
            }

            const formData = new FormData();
            formData.append("file", file);
            formData.append("n", n);

            resultDiv.innerHTML = `
            <div class="text-center py-3">
                <div class="spinner-border text-primary"></div>
                <p class="mt-2">Generating...</p>
            </div>`;

            const response = await fetch("/qa_gen/pdf", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error(await response.text());
            }

            const data = await response.json();
            renderQAPairs(data);

        } else {
            const text = document.getElementById("qaText").value.trim();

            if (!text) {
                resultDiv.innerHTML = `<div class="alert alert-warning" role="alert">
                    Please enter some text.
                </div>`;
                return;
            }

            const formData = new FormData();
            formData.append("text", text);
            formData.append("n", n);

            resultDiv.innerHTML = `
                <div class="text-center py-3">
                    <div class="spinner-border text-primary"></div>
                    <p class="mt-2">Generating...</p>
                </div>`;

            const response = await fetch("/qa_gen/text", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error(await response.text());
            }

            const data = await response.json();
            renderQAPairs(data);
        }
    } catch (error) {
        console.error("Error generating Q&A:", error);
        resultDiv.innerHTML = `<div class="alert alert-danger" role="alert">
            Something went wrong. Please try again.
        </div>`;
    } finally {
        btn.disabled = false;
    }
}
