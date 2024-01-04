const form = document.querySelector('form'); // Select the upload form element

form.addEventListener('submit', async (event) => { // Add event listener for form submission
    event.preventDefault(); // Prevent default form submission behavior

    const file = event.target.elements.image.files[0]; // Get the selected file from the form

    if (!file) { // Check if a file is selected
        alert('Please select an image to upload!');
        return;
    }
    if (!selectedLabel) { // Check if a label is selected
        alert('Please select an inventory classification!');
        return;
    }

    const formData = new FormData(); // Create a new FormData object
    formData.append('image', file); // Add the selected file to the FormData
    formData.append('label', selectedLabel); // Add the selected label to the FormData
    
    // Display loading indicator
    const loadingIndicator = document.createElement('div');
    loadingIndicator.textContent = 'Uploading...';
    document.body.appendChild(loadingIndicator);

    try {
        // Send a POST request to the upload endpoint
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        // Handle successful upload
        if (response.ok) {
            const data = await response.json();
            alert(data.message);
            document.getElementById('uploaded-image').src = data.url;
        } else {
            throw new Error('Upload failed');
        }
    } catch (error) {
        // Handle upload errors
        console.error(error);
        alert('Error uploading image');
    } finally {
        // Remove loading indicator
        document.body.removeChild(loadingIndicator);
    }
});