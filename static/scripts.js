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
        const rucVendor = data.process.rucs.vendor ? `<li>${data.process.rucs.vendor}</li>` : '';
        const rucClient = data.process.rucs.client ? `<li>${data.process.rucs.client}</li>` : '';
        document.getElementById('process-rucs').innerHTML = `<ul>${rucVendor}${rucClient}</ul>`;

        // Process and display Dates
        const dateList = data.process.dates.map(date => `<li>${date}</li>`).join('');
        document.getElementById('process-dates').innerHTML = `<ul>${dateList}</ul>`;

        // Display Total Value
        const totalValue = data.process.total_value.length ? data.process.total_value.join(', ') : 'No values found';
        document.getElementById('process-total').innerText = `Total Value: ${totalValue}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});