document.addEventListener('DOMContentLoaded', () => {
    const metricsTableBody = document.querySelector('#metrics-table tbody');

    const fetchAllMetrics = async () => {
        try {
            const response = await fetch('/get-all-metrics');
            if (!response.ok) throw new Error('Failed to fetch metrics.');
            return await response.json();
        } catch (error) {
            console.error('Error fetching metrics:', error);
            return [];
        }
    };

    const renderMetricsTable = async () => {
        const metrics = await fetchAllMetrics();
        metricsTableBody.innerHTML = metrics.map(metric => `
            <tr>
                <td>${new Date(metric.timestamp).toLocaleString()}</td>
                <td>${metric.steps}</td>
                <td>${metric.water}</td>
                <td>${metric.sleep}</td>
                <td>${metric.calories}</td>
                <td>${metric.heart_rate}</td>
                <td>${metric.blood_pressure}</td>
                <td>${metric.blood_sugar}</td>
            </tr>
        `).join('');
    };

   
    window.renderMetricsTable = renderMetricsTable;
    renderMetricsTable();
});
