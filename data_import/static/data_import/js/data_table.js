let currentPage = 1;
let itemsPerPage = 50;
let totalRows = 0;
let columns = [];

function loadMetadata() {
    fetch('/static/data_import/dhis2_metadata.json')
        .then(response => response.json())
        .then(data => {
            columns = data.columns || [];  // Assurez-vous que columns est toujours un tableau
            totalRows = data.total_rows || 0;  // Assurez-vous que totalRows est toujours un nombre
            updatePagination();
            loadData(currentPage);  // Charger les données initiales après avoir chargé les métadonnées
        })
        .catch(error => {
            console.error('Erreur lors du chargement des métadonnées:', error);
        });
}

function loadData(page = 1) {
    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const searchInput = document.getElementById('search-input');
    const categorySelect = document.getElementById('category-select');
    const dateFrom = document.getElementById('date-from');
    const dateTo = document.getElementById('date-to');

    const searchQuery = searchInput ? searchInput.value : '';
    const category = categorySelect ? categorySelect.value : '';
    const dateFromValue = dateFrom ? dateFrom.value : '';
    const dateToValue = dateTo ? dateTo.value : '';

    fetch(`/data_import/api/dhis2-data/?start=${start}&end=${end}&search=${searchQuery}&category=${category}&date_from=${dateFromValue}&date_to=${dateToValue}`)
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                updateTable(data);
                currentPage = page;
                updatePagination();
            } else {
                console.error('Les données reçues ne sont pas un tableau:', data);
            }
        })
        .catch(error => {
            console.error('Erreur lors du chargement des données:', error);
        });
}

function updateTable(data) {
    const tableHeader = document.getElementById('table-header');
    const tableBody = document.getElementById('table-body');

    if (!tableHeader || !tableBody) {
        console.error('Éléments de table manquants');
        return;
    }

    tableHeader.innerHTML = '';
    tableBody.innerHTML = '';

    const headerRow = document.createElement('tr');
    columns.forEach(column => {
        const th = document.createElement('th');
        th.textContent = column;
        headerRow.appendChild(th);
    });
    tableHeader.appendChild(headerRow);

    if (Array.isArray(data) && data.length > 0) {
        data.forEach(row => {
            const tr = document.createElement('tr');
            columns.forEach(column => {
                const td = document.createElement('td');
                td.textContent = row[column] || '';
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });
    } else {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = columns.length;
        td.textContent = 'Aucune donnée disponible';
        tr.appendChild(td);
        tableBody.appendChild(tr);
    }
}

function updatePagination() {
    const totalPages = Math.ceil(totalRows / itemsPerPage);
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');

    if (prevPageBtn) prevPageBtn.disabled = currentPage === 1;
    if (nextPageBtn) nextPageBtn.disabled = currentPage === totalPages;
    if (pageInfo) pageInfo.textContent = `Page ${currentPage} sur ${totalPages}`;
}

// Écouteurs d'événements
document.addEventListener('DOMContentLoaded', () => {
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');

    if (prevPageBtn) prevPageBtn.addEventListener('click', () => loadData(currentPage - 1));
    if (nextPageBtn) nextPageBtn.addEventListener('click', () => loadData(currentPage + 1));

    // Charge les métadonnées initiales
    loadMetadata();
});