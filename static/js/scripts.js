

document.getElementById('registerForm').addEventListener('submit', function(event) {
    var isValid = true;
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm_password').value;
    
    // Exemple de validation de mot de passe
    if (password.length < 8) {
        isValid = false;
        alert('Le mot de passe doit contenir au moins 8 caractères.');
    }
    
    if (password !== confirmPassword) {
        isValid = false;
        alert('Les mots de passe ne correspondent pas.');
    }
    
    if (!isValid) {
        event.preventDefault();
    }
});
