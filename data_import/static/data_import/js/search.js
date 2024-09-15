// data_import/static/data_import/js/search.js

$(document).ready(function() {
    $('form').on('submit', function() {
        $('button[type="submit"]').prop('disabled', true);
    });
});