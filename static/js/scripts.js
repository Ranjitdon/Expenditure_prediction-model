// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('predictionForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        // Get form data
        var date = document.getElementById('date').value;
        var categoryCode = document.getElementById('categoryCode').value;

        // Send data to server
        fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    date: date,
                    category_code: categoryCode
                })
            })
            .then(response => response.json())
            .then(data => {
                // Display prediction result
                document.getElementById('predictionResult').innerText = 'Predicted Expense: ' + data.prediction;
            })
            .catch(error => console.error('Error:', error));
    });
});