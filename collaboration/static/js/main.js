const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/'
);

notificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === 'new_message') {
        const notificationDiv = document.getElementById('notifications');
        notificationDiv.innerHTML = `Nouveau message : ${data.message}`;
        notificationDiv.style.display = 'block';
        setTimeout(() => {
            notificationDiv.style.display = 'none';
        }, 5000);
    }
};

notificationSocket.onclose = function(e) {
    console.error('Notification socket closed unexpectedly');
};