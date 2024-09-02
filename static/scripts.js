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
    event.preventDefault();  // Prevent the form from submitting the traditional way
    const formData = new FormData(this);

    fetch('/photo/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('results').style.display = 'block';

        // Display JSON output in a pretty format
        const jsonOutput = JSON.stringify(data, null, 4); // 4 spaces for indentation
        document.getElementById('json-output').innerText = jsonOutput;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});