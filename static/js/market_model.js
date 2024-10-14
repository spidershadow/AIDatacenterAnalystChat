
let allData = {};
let charts = {};

document.addEventListener('DOMContentLoaded', function() {
    fetchMarketModelData();
});

function fetchMarketModelData() {
    fetch('/api/market_model_summary')
        .then(response => response.json())
        .then(data => {
            allData = data;
            populateFilters(data);
            createCategoryChart(data);
            createParticipantChart(data);
            createTimelineChart(data);
            displayDataPointDetails(data);
        })
        .catch(error => console.error('Error:', error));
}

function populateFilters(data) {
    const categoryFilter = document.getElementById('category-filter');
    const participantFilter = document.getElementById('participant-filter');

    // Populate participant filter
    const allParticipants = new Set();
    Object.values(data).forEach(category => {
        Object.keys(category).forEach(participant => allParticipants.add(participant));
    });

    allParticipants.forEach(participant => {
        const option = document.createElement('option');
        option.value = participant;
        option.textContent = participant;
        participantFilter.appendChild(option);
    });

    // Add event listeners
    categoryFilter.addEventListener('change', updateCharts);
    participantFilter.addEventListener('change', updateCharts);
}

function createCategoryChart(data) {
    const ctx = document.getElementById('category-chart').getContext('2d');
    const categories = Object.keys(data);
    const dataPoints = categories.map(category => 
        Object.values(data[category]).reduce((sum, participantData) => sum + participantData.length, 0)
    );

    charts.category = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories,
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
                title: {
                    display: true,
                    text: 'Data Points by Category'
                }
            }
        }
    });
}

function createParticipantChart(data) {
    const ctx = document.getElementById('participant-chart').getContext('2d');
    const participants = new Set();
    const participantData = {};

    Object.values(data).forEach(category => {
        Object.entries(category).forEach(([participant, dataPoints]) => {
            participants.add(participant);
            if (!participantData[participant]) {
                participantData[participant] = 0;
            }
            participantData[participant] += dataPoints.length;
        });
    });

    const participantLabels = Array.from(participants);
    const dataPoints = participantLabels.map(participant => participantData[participant]);

    charts.participant = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: participantLabels,
            datasets: [{
                data: dataPoints,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Data Points by Participant Type'
                }
            }
        }
    });
}

function createTimelineChart(data) {
    const ctx = document.getElementById('timeline-chart').getContext('2d');
    const timelineData = {};

    Object.entries(data).forEach(([category, participants]) => {
        Object.values(participants).forEach(dataPoints => {
            dataPoints.forEach(point => {
                const date = new Date(point.date).toISOString().split('T')[0];
                if (!timelineData[date]) {
                    timelineData[date] = 0;
                }
                timelineData[date]++;
            });
        });
    });

    const sortedDates = Object.keys(timelineData).sort();
    const dataPoints = sortedDates.map(date => timelineData[date]);

    charts.timeline = new Chart(ctx, {
        type: 'line',
        data: {
            labels: sortedDates,
            datasets: [{
                label: 'Number of Data Points',
                data: dataPoints,
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Timeline of Data Points'
                }
            }
        }
    });
}

function displayDataPointDetails(data) {
    const detailsElement = document.getElementById('data-point-details');
    let detailsHTML = '<ul class="list-group">';

    Object.entries(data).forEach(([category, participants]) => {
        Object.entries(participants).forEach(([participant, dataPoints]) => {
            dataPoints.forEach(point => {
                detailsHTML += `
                    <li class="list-group-item">
                        <strong>Category:</strong> ${category}<br>
                        <strong>Participant:</strong> ${participant}<br>
                        <strong>Date:</strong> ${new Date(point.date).toLocaleDateString()}<br>
                        <strong>Value:</strong> ${point.value}
                    </li>
                `;
            });
        });
    });

    detailsHTML += '</ul>';
    detailsElement.innerHTML = detailsHTML;
}

function updateCharts() {
    const selectedCategory = document.getElementById('category-filter').value;
    const selectedParticipant = document.getElementById('participant-filter').value;

    let filteredData = JSON.parse(JSON.stringify(allData)); // Deep clone

    if (selectedCategory !== 'all') {
        filteredData = { [selectedCategory]: filteredData[selectedCategory] };
    }

    if (selectedParticipant !== 'all') {
        Object.keys(filteredData).forEach(category => {
            filteredData[category] = { [selectedParticipant]: filteredData[category][selectedParticipant] || [] };
        });
    }

    // Update category chart
    const categoryData = Object.keys(filteredData).map(category => 
        Object.values(filteredData[category]).reduce((sum, participantData) => sum + participantData.length, 0)
    );
    charts.category.data.labels = Object.keys(filteredData);
    charts.category.data.datasets[0].data = categoryData;
    charts.category.update();

    // Update participant chart
    const participantData = {};
    Object.values(filteredData).forEach(category => {
        Object.entries(category).forEach(([participant, dataPoints]) => {
            if (!participantData[participant]) {
                participantData[participant] = 0;
            }
            participantData[participant] += dataPoints.length;
        });
    });
    charts.participant.data.labels = Object.keys(participantData);
    charts.participant.data.datasets[0].data = Object.values(participantData);
    charts.participant.update();

    // Update timeline chart
    const timelineData = {};
    Object.values(filteredData).forEach(category => {
        Object.values(category).forEach(dataPoints => {
            dataPoints.forEach(point => {
                const date = new Date(point.date).toISOString().split('T')[0];
                if (!timelineData[date]) {
                    timelineData[date] = 0;
                }
                timelineData[date]++;
            });
        });
    });
    const sortedDates = Object.keys(timelineData).sort();
    charts.timeline.data.labels = sortedDates;
    charts.timeline.data.datasets[0].data = sortedDates.map(date => timelineData[date]);
    charts.timeline.update();

    // Update data point details
    displayDataPointDetails(filteredData);
}
