document.addEventListener('DOMContentLoaded', function () {
    // Function to fetch all log metrics
    async function fetchAllMetrics() {
        try {
            const response = await fetch('/get-all-metrics');
            if (!response.ok) {
                throw new Error('Failed to fetch metrics.');
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching metrics:', error);
            return [];
        }
    }

    // Function to render the metrics table
    async function renderMetricsTable() {
        const metricsTableBody = document.querySelector('#metrics-table tbody');
        const metrics = await fetchAllMetrics();

        // Clear existing rows
        metricsTableBody.innerHTML = '';

        // Add a row for each metric
        metrics.forEach(metric => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${new Date(metric.timestamp).toLocaleString()}</td>
                <td>${metric.steps}</td>
                <td>${metric.water}</td>
                <td>${metric.sleep}</td>
                <td>${metric.calories}</td>
                <td>${metric.heart_rate}</td>
                <td>${metric.blood_pressure}</td>
                <td>${metric.blood_sugar}</td>
            `;
            metricsTableBody.appendChild(row);
        });
    }

    // Attach the renderMetricsTable function to the window object
    window.renderMetricsTable = renderMetricsTable;

    // Render the table when the page loads (optional)
    renderMetricsTable();
});