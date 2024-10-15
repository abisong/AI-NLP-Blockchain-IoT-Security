document.addEventListener('DOMContentLoaded', function() {
    const sentimentForm = document.getElementById('sentiment-form');
    const sentimentResult = document.getElementById('sentiment-result');
    const iotData = document.getElementById('iot-data');

    if (sentimentForm) {
        sentimentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const text = document.getElementById('text-input').value;
            
            fetch('/analyze_sentiment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `text=${encodeURIComponent(text)}`
            })
            .then(response => response.json())
            .then(data => {
                sentimentResult.textContent = `Sentiment: ${data.sentiment}`;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    if (iotData) {
        setInterval(() => {
            fetch('/dashboard')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newIotData = doc.getElementById('iot-data');
                if (newIotData) {
                    iotData.innerHTML = newIotData.innerHTML;
                }
            })
            .catch(error => {
                console.error('Error updating IoT data:', error);
            });
        }, 5000); // Update every 5 seconds
    }
});
