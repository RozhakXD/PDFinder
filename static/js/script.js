document.getElementById('searchForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const query = document.getElementById('query').value;
    const count = document.getElementById('count').value;

    const loadingText = document.getElementById('loading');
    loadingText.style.display = 'block';

    const response = await fetch('/search/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, count })
    });

    const result = await response.json();

    loadingText.style.display = 'none';

    const modal = document.getElementById('modal');
    const modalStatus = document.getElementById('modal-status');
    const modalMessage = document.getElementById('modal-message');

    if (result.Sukses) {
        modalStatus.textContent = 'Sukses!';
        modalMessage.textContent = 'File PDF berhasil ditemukan!';
        displayResults(result.Message);
    } else {
        modalStatus.textContent = 'Gagal!';
        modalMessage.textContent = `${result.Message}!`;
        document.getElementById('results').innerHTML = '';
    }

    modal.style.display = 'block';
});

document.querySelector('.close-btn').addEventListener('click', function () {
    document.getElementById('modal').style.display = 'none';
});

window.addEventListener('click', function (event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

document.getElementById('copy-close-btn').addEventListener('click', function () {
    document.getElementById('copy-modal').style.display = 'none';
});

window.addEventListener('click', function (event) {
    const copyModal = document.getElementById('copy-modal');
    if (event.target === copyModal) {
        copyModal.style.display = 'none';
    }
});

function displayResults(PDF) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

    PDF.forEach(item => {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';

        const title = document.createElement('h3');
        title.textContent = item.title;

        const snippet = document.createElement('p');
        snippet.textContent = item.snippet;

        const iframe = document.createElement('iframe');
        iframe.src = item.url;
        iframe.width = "100%";
        iframe.height = "500px";
        iframe.style.border = "none";

        const buttonContainer = document.createElement('div');
        buttonContainer.className = 'button-container';

        const downloadButton = document.createElement('button');
        downloadButton.innerHTML = '<img src="../static/icons/unduh.png" alt="Download Icon"> Unduh PDF';
        downloadButton.onclick = () => window.open(item.url, '_blank');

        const copyButton = document.createElement('button');
        copyButton.innerHTML = '<img src="../static/icons/salin.png" alt="Copy Icon"> Copy Link';
        copyButton.onclick = () => {
            navigator.clipboard.writeText(item.url);

            const copyModal = document.getElementById('copy-modal');
            copyModal.style.display = 'block';
        };

        buttonContainer.appendChild(downloadButton);
        buttonContainer.appendChild(copyButton);

        resultItem.appendChild(title);
        resultItem.appendChild(snippet);
        resultItem.appendChild(iframe);
        resultItem.appendChild(buttonContainer);

        resultsContainer.appendChild(resultItem);
    });
}