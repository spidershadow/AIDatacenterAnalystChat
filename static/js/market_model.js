document.addEventListener('DOMContentLoaded', function() {
    fetchMarketModelSummary();
    fetchCategoryData('product_offerings');
    fetchCategoryData('market_trends');
    fetchCategoryData('competitive_landscape');
    fetchCategoryData('technology_advancements');
});

function fetchMarketModelSummary() {
    fetch('/api/market_model_summary')
        .then(response => response.json())
        .then(data => {
            displayModelSummary(data);
        })
        .catch(error => console.error('Error:', error));
}

function displayModelSummary(data) {
    const summaryElement = document.getElementById('model-summary');
    let summaryHTML = '<ul class="list-group">';
    for (const [category, participants] of Object.entries(data)) {
        summaryHTML += `<li class="list-group-item d-flex justify-content-between align-items-center">
            ${category}
            <span class="badge bg-primary rounded-pill">${Object.values(participants).reduce((a, b) => a + b, 0)}</span>
        </li>`;
    }
    summaryHTML += '</ul>';
    summaryElement.innerHTML = summaryHTML;
}

function fetchCategoryData(category) {
    fetch(`/api/market_model/${category}`)
        .then(response => response.json())
        .then(data => {
            createChart(category, data);
        })
        .catch(error => console.error('Error:', error));
}

function createChart(category, data) {
    const ctx = document.getElementById(`${category.replace('_', '-')}-chart`).getContext('2d');
    const participantTypes = Object.keys(data);
    const dataPoints = participantTypes.map(type => data[type].length);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: participantTypes,
            datasets: [{
                label: 'Number of Data Points',
                data: dataPoints,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: category.replace('_', ' ').toUpperCase()
                }
            }
        }
    });
}
