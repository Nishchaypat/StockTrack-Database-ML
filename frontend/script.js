const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const signupLink = document.querySelector('.signup-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

// Event listeners for form toggling
signupLink.addEventListener('click', () => {
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', () => {
    wrapper.classList.remove('active');
});

btnPopup.addEventListener('click', () => {
    wrapper.classList.add('active-popup');
});

iconClose.addEventListener('click', () => {
    wrapper.classList.remove('active-popup');
});

// Event listener for the login form submission
document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch('http://localhost:8000/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email, password: password }),
        });

        const result = await response.json();
        alert(result.message); // Show login result message

        // Optional: You can also handle successful login here (e.g., redirect)
    } catch (error) {
        console.error('Error during login:', error);
        alert('Login failed. Please try again.');
    }
});

// Event listener for the signup form submission
document.getElementById('signup-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const firstname = document.getElementById('signup-username').value; // Assuming username is first name
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    try {
        const response = await fetch('http://localhost:8000/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ firstname: firstname, lastname: '', email: email, password: password }),
        });

        const result = await response.json();
        alert(result.message); // Show registration result message

        // Optional: You can handle successful registration here (e.g., redirect)
    } catch (error) {
        console.error('Error during registration:', error);
        alert('Registration failed. Please try again.');
    }
});
