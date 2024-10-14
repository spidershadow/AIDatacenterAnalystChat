document.addEventListener('DOMContentLoaded', function() {
    fetchInterviewData();
});

function fetchInterviewData() {
    fetch('/api/interview_data')
        .then(response => response.json())
        .then(data => {
            updateDashboard(data);
            createCharts(data);
        })
        .catch(error => console.error('Error:', error));
}

function updateDashboard(data) {
    const interviewList = document.getElementById('interview-list');
    interviewList.innerHTML = '';
    
    data.forEach(interview => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.innerHTML = `
            <strong>${interview.company_name}</strong> (${interview.participant_type})
            <br>Date: ${new Date(interview.interview_date).toLocaleDateString()}
            <br>Status: ${interview.completed ? 'Completed' : 'Pending'}
        `;
        interviewList.appendChild(li);
    });
}

function createCharts(data) {
    const participantTypes = data.reduce((acc, interview) => {
        acc[interview.participant_type] = (acc[interview.participant_type] || 0) + 1;
        return acc;
    }, {});
    
    const ctx = document.getElementById('participant-chart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(participantTypes),
            datasets: [{
                data: Object.values(participantTypes),
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
            title: {
                display: true,
                text: 'Participant Type Distribution'
            }
        }
    });
}
