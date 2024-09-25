// Déclarations globales
let columnSelect, searchForm, resultsTable, exportPdfButton;

// Fonction principale d'initialisation
function initializeApp() {
    columnSelect = document.getElementById('column-select');
    searchForm = document.getElementById('search-form');
    resultsTable = document.getElementById('results-table');
    exportPdfButton = document.getElementById('export-pdf');

    if (!columnSelect || !searchForm || !resultsTable || !exportPdfButton) {
        console.error('Un ou plusieurs éléments DOM requis sont manquants');
        return;
    }

    loadColumns();
    setupEventListeners();
}

// Charger les colonnes
function loadColumns() {
    fetch('/api/get-columns/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la récupération des colonnes');
            }
            return response.json();
        })
        .then(columns => {
            if (Array.isArray(columns) && columns.length > 0) {
                columns.forEach(column => {
                    const option = document.createElement('option');
                    option.value = column;
                    option.textContent = column;
                    columnSelect.appendChild(option);
                });
            } else {
                console.error('Aucune colonne reçue ou format invalide');
            }
        })
        .catch(error => {
            console.error('Erreur lors du chargement des colonnes:', error);
        });
}

// Configurer les écouteurs d'événements
function setupEventListeners() {
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        performSearch(1);
    });

    exportPdfButton.addEventListener('click', exportToPdf);
}

// Fonction de recherche
function performSearch(page) {
    const column = columnSelect.value;
    const searchInput = document.getElementById('search-input');
    const dateFrom = document.getElementById('date-from');
    const dateTo = document.getElementById('date-to');

    if (!searchInput || !dateFrom || !dateTo) {
        console.error('Éléments de formulaire manquants');
        return;
    }

    const searchValue = searchInput.value;
    const dateFromValue = dateFrom.value;
    const dateToValue = dateTo.value;

    const url = `/api/advanced-search/?column=${encodeURIComponent(column)}&search=${encodeURIComponent(searchValue)}&date_from=${encodeURIComponent(dateFromValue)}&date_to=${encodeURIComponent(dateToValue)}&page=${page}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la recherche');
            }
            return response.json();
        })
        .then(data => {
            if (data && Array.isArray(data.data)) {
                displayResults(data.data);
                updatePagination(data.total_count, data.page, data.items_per_page);
            } else {
                console.error('Format de données invalide reçu de l\'API');
                displayResults([]);
            }
        })
        .catch(error => {
            console.error('Erreur lors de la recherche:', error);
            displayResults([]);
        });
}

// Afficher les résultats
function displayResults(data) {
    const thead = resultsTable.querySelector('thead');
    const tbody = resultsTable.querySelector('tbody');

    if (!thead || !tbody) {
        console.error('Structure de table invalide');
        return;
    }

    // Effacer les résultats précédents
    thead.innerHTML = '';
    tbody.innerHTML = '';

    if (data.length > 0) {
        // Créer les en-têtes
        const headerRow = document.createElement('tr');
        Object.keys(data[0]).forEach(key => {
            const th = document.createElement('th');
            th.textContent = key;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);

        // Ajouter les données
        data.forEach(row => {
            const tr = document.createElement('tr');
            Object.values(row).forEach(value => {
                const td = document.createElement('td');
                td.textContent = value !== null && value !== undefined ? value : '';
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    } else {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = 5;
        td.textContent = 'Aucun résultat trouvé';
        tr.appendChild(td);
        tbody.appendChild(tr);
    }
}

// Mettre à jour la pagination
function updatePagination(totalCount, currentPage, itemsPerPage) {
    const pagination = document.querySelector('.pagination');
    if (!pagination) {
        console.error('Élément de pagination non trouvé');
        return;
    }

    pagination.innerHTML = '';

    const totalPages = Math.ceil(totalCount / itemsPerPage);

    for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === currentPage ? 'active' : ''}`;
        const a = document.createElement('a');
        a.className = 'page-link';
        a.href = '#';
        a.textContent = i;
        a.addEventListener('click', (e) => {
            e.preventDefault();
            performSearch(i);
        });
        li.appendChild(a);
        pagination.appendChild(li);
    }
}

// Exporter en PDF
function exportToPdf() {
    if (typeof window.jspdf === 'undefined' || typeof window.jspdf.jsPDF === 'undefined') {
        console.error('La bibliothèque jsPDF n\'est pas chargée');
        return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.autoTable({ html: resultsTable });
    doc.save('results.pdf');
}

// Initialiser l'application lorsque le DOM est chargé
document.addEventListener('DOMContentLoaded', initializeApp);