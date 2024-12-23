
    document.addEventListener('DOMContentLoaded', function() {
    // Mark message as read when opened
    const messageDetail = document.querySelector('.message-detail');
    if (messageDetail) {
        const messageId = messageDetail.dataset.messageId;
        fetch(`/collaboration/mark_as_read/${messageId}/`, {method: 'POST'})
            .then(response => response.json())
            .then(data => console.log(data));
    }

    // Add new tag
    const addTagForm = document.getElementById('add-tag-form');
    if (addTagForm) {
        addTagForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(addTagForm);
            fetch('/collaboration/add_tag/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    const tagSelect = document.getElementById('id_tags');
                    const option = new Option(data.name, data.id);
                    tagSelect.add(option);
                    addTagForm.reset();
                }
            });
        });
    }
});
