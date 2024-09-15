// Fonction pour initialiser les tooltips Bootstrap
function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
}

// Fonction pour initialiser les popovers Bootstrap
function initPopovers() {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })
}

// Fonction pour gérer les formulaires de filtre
function initFilterForm() {
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const searchParams = new URLSearchParams(formData);
            window.location.search = searchParams.toString();
        });
    }
}

// Fonction pour gérer la pagination AJAX
function initAjaxPagination() {
    const paginationLinks = document.querySelectorAll('.pagination .page-link');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            fetch(url)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newContent = doc.querySelector('#content-area').innerHTML;
                    document.querySelector('#content-area').innerHTML = newContent;
                    history.pushState(null, '', url);
                    initAjaxPagination(); // Réinitialiser pour les nouveaux liens
                })
                .catch(error => console.error('Erreur:', error));
        });
    });
}

// Fonction pour gérer le chargement dynamique des graphiques
function loadChart(chartId, chartData) {
    Plotly.newPlot(chartId, chartData.data, chartData.layout);
}

// Fonction pour exporter le graphique en PNG
function exportChartAsPNG(chartId) {
    Plotly.downloadImage(chartId, {format: 'png', width: 800, height: 600, filename: 'chart'});
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    initPopovers();
    initFilterForm();
    initAjaxPagination();

    // Exemple d'utilisation de la fonction loadChart
    // Vous devrez adapter cela en fonction de la façon dont vous fournissez les données du graphique
    const chartElement = document.getElementById('plotly-chart');
    if (chartElement && chartElement.dataset.chartJson) {
        const chartData = JSON.parse(chartElement.dataset.chartJson);
        loadChart('plotly-chart', chartData);
    }

    // Ajout d'un gestionnaire d'événements pour le bouton d'exportation PNG
    const exportButton = document.getElementById('export-png');
    if (exportButton) {
        exportButton.addEventListener('click', function() {
            exportChartAsPNG('plotly-chart');
        });
    }
});