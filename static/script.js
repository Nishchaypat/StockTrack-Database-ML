// DOM elements for form handling and visibility toggling
const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const signupLink = document.querySelector('.signup-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

// Show signup form and hide login form
signupLink.addEventListener('click', () => {
    wrapper.classList.add('active');
});

// Show login form and hide signup form
loginLink.addEventListener('click', () => {
    wrapper.classList.remove('active');
});

// Open the login/signup popup
btnPopup.addEventListener('click', () => {
    wrapper.classList.add('active-popup');
});

// Close the popup
iconClose.addEventListener('click', () => {
    wrapper.classList.remove('active-popup');
});

// Handle Login Form Submission
document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        const result = await response.json();
        document.getElementById("loginResponse").innerText = result.status === "success" ? "Login successful!" : result.message;

        // Close the popup if login is successful
        if (result.status === "success") {
            wrapper.classList.remove('active-popup');
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("loginResponse").innerText = "Error logging in.";
    }
});

// Handle SignUp Form Submission
document.getElementById("signupForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const firstname = document.getElementById("signupFirstname").value;
    const lastname = document.getElementById("signupLastname").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;

    try {
        const response = await fetch("/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ firstname, lastname, email, password })
        });
        const result = await response.json();
        document.getElementById("signupResponse").innerText = result.status === "success" ? "Sign up successful!" : result.message;

        // Close the popup if signup is successful and switch to login form
        if (result.status === "success") {
            wrapper.classList.remove('active');
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("signupResponse").innerText = "Error signing up.";
    }
});
