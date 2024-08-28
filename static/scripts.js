document.getElementById('file-input').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('image-preview').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting the traditional way
    const formData = new FormData(this);

    fetch('/photo/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('results').style.display = 'block';
        document.getElementById('response-title').innerText = `Title: ${data.title}`;
        document.getElementById('response-text').innerText = `Response: ${data.response}`;
        
        // Clear previous process data
        document.getElementById('process-rucs').innerHTML = '';
        document.getElementById('process-dates').innerHTML = '';
        document.getElementById('process-total').innerText = '';

        // Process and display RUCs
        const rucList = data.process.rucs.map(ruc => `<li>${ruc}</li>`).join('');
        document.getElementById('process-rucs').innerHTML = `<ul>${rucList}</ul>`;

        // Process and display Dates
        const dateList = data.process.dates.map(date => `<li>${date}</li>`).join('');
        document.getElementById('process-dates').innerHTML = `<ul>${dateList}</ul>`;

        // Display Total Value
        document.getElementById('process-total').innerText = `Total Value: ${data.process.total_value.join(', ')}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
