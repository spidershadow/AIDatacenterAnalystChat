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
        .then(response => {
            loadingIndicator.style.display = 'none';
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data && data.error) {
                throw new Error(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            loadingIndicator.style.display = 'none';
            const errorMessage = error.message || 'An error occurred during the interview process. Please try again.';
            const alertElement = document.createElement('div');
            alertElement.className = 'alert alert-danger alert-dismissible fade show mt-3';
            alertElement.role = 'alert';
            alertElement.innerHTML = `
                ${errorMessage}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            `;
            form.insertAdjacentElement('beforebegin', alertElement);
        });
    });
});
