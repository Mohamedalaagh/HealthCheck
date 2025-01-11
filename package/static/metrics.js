document.addEventListener('DOMContentLoaded', () => {
    const metricsForm = document.getElementById('metrics-form');

    if (metricsForm) {
        metricsForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(metricsForm);

            try {
                const response = await fetch('/log-metrics', {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });

                const data = await response.json();
                alert(data.message || data.error);
                if (data.message) {
                    metricsForm.reset();
                    window.renderMetricsTable?.();
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while logging metrics.');
            }
        });
    }

    window.showSection = (sectionId) => {
        document.querySelectorAll('.content-section').forEach(section => section.style.display = 'none');
        document.getElementById('welcome-sections').style.display = 'none';

        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'block';
            if (sectionId === 'metrics-insights') {
                window.renderMetricsTable?.();
            }
        }
    };
});
