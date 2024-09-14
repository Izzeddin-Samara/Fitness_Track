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

function showForm(formType) {
    document.getElementById('user-form').style.display = 'none';
    document.getElementById('coach-form').style.display = 'none';
    document.getElementById('admin-form').style.display = 'none';  // Updated to hide admin form

    if (formType === 'user') {
        document.getElementById('user-form').style.display = 'block';
    } else if (formType === 'coach') {
        document.getElementById('coach-form').style.display = 'block';
    } else if (formType === 'admin') {
        document.getElementById('admin-form').style.display = 'block';  // Updated to show admin form
    }
}

document.addEventListener("DOMContentLoaded", function () {
    showForm(document.getElementById('form-select').value);
});