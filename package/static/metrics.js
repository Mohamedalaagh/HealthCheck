document.addEventListener('DOMContentLoaded', function () {
    const metricsForm = document.getElementById('metrics-form');

    // Handle form submission
    if (metricsForm) {
        metricsForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent default form submission

            const formData = new FormData(metricsForm);

            // Send form data to the server
            fetch('/log-metrics', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Identify as an AJAX request
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message); // Show success message
                    metricsForm.reset(); // Reset the form

                    // Refresh the metrics table
                    if (window.renderMetricsTable) {
                        renderMetricsTable();
                    }
                } else if (data.error) {
                    alert(data.error); // Show error message
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while logging metrics.');
            });
        });
    }

    // Function to show/hide sections
    function showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.style.display = 'none';
        });

        // Hide the welcome message
        document.getElementById('welcome-sections').style.display = 'none';

        // Show the selected section
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'block';
        }

        // If the selected section is "metrics-insights", refresh the table
        if (sectionId === 'metrics-insights' && window.renderMetricsTable) {
            renderMetricsTable();
        }
    }

    // Attach the showSection function to the window object
    window.showSection = showSection;
});