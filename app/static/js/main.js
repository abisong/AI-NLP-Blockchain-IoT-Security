document.addEventListener('DOMContentLoaded', function() {
    const sentimentForm = document.getElementById('sentiment-form');
    const sentimentResult = document.getElementById('sentiment-result');
    const iotData = document.getElementById('iot-data');
    const mineButton = document.getElementById('mine-button');
    const miningResult = document.getElementById('mining-result');
    const transactionForm = document.getElementById('transaction-form');
    const transactionResult = document.getElementById('transaction-result');
    const viewChainButton = document.getElementById('view-chain-button');
    const blockchainData = document.getElementById('blockchain-data');

    if (sentimentForm) {
        sentimentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const text = document.getElementById('text-input').value;
            
            fetch('/analyze_sentiment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `text=${encodeURIComponent(text)}`
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                sentimentResult.textContent = `Sentiment: ${data.sentiment}`;
            })
            .catch(error => {
                console.error('Error in sentiment analysis:', error);
                sentimentResult.textContent = `Error: ${error.message}`;
            });
        });
    }

    if (iotData) {
        function updateIoTData() {
            fetch('/dashboard', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                iotData.innerHTML = `
                    <h3>IoT Sensor Data</h3>
                    <p>Temperature: ${data.temperature}°C</p>
                    <p>Humidity: ${data.humidity}%</p>
                    <p>Timestamp: ${data.timestamp}</p>
                `;
            })
            .catch(error => {
                console.error('Error updating IoT data:', error);
                iotData.innerHTML = `<p>Error updating IoT data: ${error.message}</p>`;
            });
        }

        setInterval(updateIoTData, 5000); // Update every 5 seconds
    }

    if (mineButton) {
        mineButton.addEventListener('click', function() {
            fetch('/mine', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                miningResult.textContent = `Block mined: ${JSON.stringify(data)}`;
            })
            .catch(error => {
                console.error('Error in mining:', error);
                miningResult.textContent = `Error: ${error.message}`;
            });
        });
    }

    if (transactionForm) {
        transactionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const recipient = document.getElementById('recipient').value;
            const amount = document.getElementById('amount').value;

            fetch('/transactions/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({recipient: recipient, amount: parseFloat(amount)})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                transactionResult.textContent = data.message;
            })
            .catch(error => {
                console.error('Error in transaction:', error);
                transactionResult.textContent = `Error: ${error.message}`;
            });
        });
    }

    if (viewChainButton) {
        viewChainButton.addEventListener('click', function() {
            fetch('/chain', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                blockchainData.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            })
            .catch(error => {
                console.error('Error viewing blockchain:', error);
                blockchainData.innerHTML = `<p>Error: ${error.message}</p>`;
            });
        });
    }
});
