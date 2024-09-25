
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('visualization-form');
    const chartContainer = document.getElementById('chart-container');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            chartContainer.innerHTML = `Chart`;
        });
    });
});