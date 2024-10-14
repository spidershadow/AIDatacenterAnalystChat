document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('interview-form');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        loadingIndicator.style.display = 'block';
        
        const formData = new FormData(form);
        fetch('/interview', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingIndicator.style.display = 'none';
            window.location.href = '/dashboard';
        })
        .catch(error => {
            console.error('Error:', error);
            loadingIndicator.style.display = 'none';
            alert('An error occurred during the interview process. Please try again.');
        });
    });
});
