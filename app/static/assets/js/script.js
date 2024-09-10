$(document).ready(function () {
    var passwordField = $('#password');
    var confirmPasswordField = $('#confirm_password');
    var message = $('#passwordMatchMessage');

    // Check if passwords match while typing
    function checkPasswords() {
        var password = passwordField.val();
        var confirmPassword = confirmPasswordField.val();

        if (password === confirmPassword) {
            message.text("Passwords match");
            message.removeClass('text-danger');
            message.addClass('text-success');
        } else {
            message.text("Passwords do not match!");
            message.removeClass('text-success');
            message.addClass('text-danger');
        }
    }

    passwordField.on('input', checkPasswords);
    confirmPasswordField.on('input', checkPasswords);
});

function showForm(type) {
    if (type === 'user') {
        document.getElementById('user-form').classList.add('active');
        document.getElementById('coach-form').classList.remove('active');
    } else if (type === 'coach') {
        document.getElementById('coach-form').classList.add('active');
        document.getElementById('user-form').classList.remove('active');
    }
}