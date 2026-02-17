document.addEventListener('DOMContentLoaded', function() {
    // Get current tab URL
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        const url = tabs[0].url;
        document.getElementById('currentUrl').textContent = url;
        
        // Auto-check on open
        checkUrl(url);
    });
    
    document.getElementById('checkBtn').addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            checkUrl(tabs[0].url);
        });
    });
});

async function checkUrl(url) {
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    
    try {
        const response = await fetch('http://localhost:5000/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({url: url})
        });
        
        const data = await response.json();
        displayResult(data);
    } catch (error) {
        document.getElementById('result').innerHTML = 'Error connecting to server';
        document.getElementById('result').style.display = 'block';
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function displayResult(data) {
    const resultDiv = document.getElementById('result');
    
    if (data.is_phishing) {
        resultDiv.className = 'result phishing';
        resultDiv.innerHTML = `
            <strong>⚠️ PHISHING DETECTED!</strong>
            <p>Confidence: ${data.confidence}%</p>
            <p>Risk: ${data.risk}</p>
            ${data.reasons ? '<small>' + data.reasons[0] + '</small>' : ''}
        `;
    } else {
        resultDiv.className = 'result safe';
        resultDiv.innerHTML = `
            <strong>✅ Safe URL</strong>
            <p>Confidence: ${data.confidence}%</p>
        `;
    }
    
    resultDiv.style.display = 'block';
}