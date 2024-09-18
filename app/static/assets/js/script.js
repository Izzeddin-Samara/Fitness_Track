document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    const passwordMatchSuccess = document.getElementById('password_match_success');

    signupForm.addEventListener('input', function(e) {
        validateField(e.target);
        checkPasswordMatch();
    });

    signupForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent form submission to validate fields first

        let valid = true;
        const fields = ['first_name', 'last_name', 'email', 'password', 'password_confirmation'];
        
        fields.forEach(field => {
            const input = document.querySelector(`[name="${field}"]`);
            if (!validateField(input)) {
                valid = false;
            }
        });

        if (valid) {
            signupForm.submit(); // Submit if all fields are valid
        }
    });

    function validateField(field) {
        const errorElement = document.getElementById(`${field.name}_error`);
        errorElement.textContent = '';
        field.classList.remove('is-invalid');
        field.classList.remove('is-valid');

        switch (field.name) {
            case 'email':
                if (!validateEmail(field.value)) {
                    errorElement.textContent = 'Invalid email format!';
                    field.classList.add('is-invalid');
                    return false;
                }
                break;
            case 'password':
                if (field.value.length < 8) {
                    errorElement.textContent = 'Password should be at least 8 characters.';
                    field.classList.add('is-invalid');
                    return false;
                }
                break;
            case 'password_confirmation':
                const passwordField = document.querySelector('[name="password"]');
                if (field.value !== passwordField.value) {
                    errorElement.textContent = 'Passwords do not match.';
                    field.classList.add('is-invalid');
                    return false;
                }
                break;
            default:
                if (field.value.trim().length < 2) {
                    errorElement.textContent = 'This field must be at least 2 characters.';
                    field.classList.add('is-invalid');
                    return false;
                }
        }
        return true;
    }

    function checkPasswordMatch() {
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;

        if (confirmPassword && password === confirmPassword) {
            passwordMatchSuccess.textContent = 'Passwords match';
            confirmPasswordField.classList.add('is-valid');
            confirmPasswordField.classList.remove('is-invalid');
        } else {
            passwordMatchSuccess.textContent = '';
            confirmPasswordField.classList.remove('is-valid');
        }
    }

    function validateEmail(email) {
        const re = /^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$/;
        return re.test(email);
    }

    // Function to toggle password visibility
    function togglePassword(inputId, iconId) {
        const input = document.getElementById(inputId);
        const icon = document.getElementById(iconId);
        if (input.type === "password") {
            input.type = "text";
            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash");
        } else {
            input.type = "password";
            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye");
        }
    }
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