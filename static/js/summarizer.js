function initSummarizerEvents() {
  document.querySelectorAll('input[name="summaryMode"]').forEach(radio => {
    radio.addEventListener('change', function () {
      const isPdf = this.value === 'pdf';
      document.getElementById('summaryPdfSection').style.display = isPdf ? 'block' : 'none';
      document.getElementById('summaryTextSection').style.display = isPdf ? 'none' : 'block';
    });
  });
}


async function submitSummarizer() {
  const mode = document.querySelector('input[name="summaryMode"]:checked').value;
  const resultDiv = document.getElementById("summaryResult");
  resultDiv.innerHTML = ""; // Clear previous result

  const summaryLength = document.getElementById("summaryLength").value;
  const btn = document.getElementById("summarySubmitBtn");
  btn.disabled = true;

  try {
    if (mode === "pdf") {
      const fileInput = document.getElementById("summaryFile");
      const file = fileInput.files[0];

      if (!file) {
        resultDiv.innerHTML = `<div class="alert alert-warning" role="alert">
          Please upload a PDF file to summarize.
        </div>`;
        return;
      }

      if (file.type !== "application/pdf") {
        resultDiv.innerHTML = `
            <div class="alert alert-warning">
                Please upload a valid PDF file.
            </div>`;
        return;
      }


      const formData = new FormData();
      formData.append("file", file);
      formData.append("summary_length", summaryLength);

      resultDiv.innerHTML = `
      <div class="text-center py-3">
          <div class="spinner-border text-success"></div>
          <p class="mt-2">Processing...</p>
      </div>`;

      const response = await fetch("/summarize/pdf", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.text();
      const html = marked.parse(data);
      resultDiv.innerHTML = html;

    } else {
      const text = document.getElementById("summaryText").value.trim();

      if (!text) {
        resultDiv.innerHTML = `<div class="alert alert-warning" role="alert">
          Please enter some text to summarize.
        </div>`;
        return;
      }

      const formData = new FormData();
      formData.append("text", text);
      formData.append("summaryLength", summaryLength);

      resultDiv.innerHTML = `
      <div class="text-center py-3">
          <div class="spinner-border text-success"></div>
          <p class="mt-2">Processing...</p>
      </div>`;

      const response = await fetch("/summarize/text", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.text();
      const html = marked.parse(data);
      resultDiv.innerHTML = html;
    }

  } catch (error) {
    console.error("Summarization failed:", error);
    resultDiv.innerHTML = `<div class="alert alert-danger" role="alert">
      An error occurred while summarizing. Please try again.
    </div>`;
  } finally {
    btn.disabled = false;
  }
}
