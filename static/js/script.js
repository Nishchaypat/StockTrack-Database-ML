const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const signupLink = document.querySelector('.signup-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

// Toggle to signup form
signupLink.addEventListener('click', () => {
    wrapper.classList.add('active');
});

// Toggle to login form
loginLink.addEventListener('click', () => {
    wrapper.classList.remove('active');
});

// Show login popup
btnPopup.addEventListener('click', () => {
    wrapper.classList.add('active-popup');
});

// Close login/signup popup
iconClose.addEventListener('click', () => {
    wrapper.classList.remove('active-popup');
});

// Handle login form submission
document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.querySelector('.form-box.login form');
    
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission
        
        const email = document.querySelector('#loginEmail').value;
        const password = document.querySelector('#loginPassword').value;

        fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                sessionStorage.setItem("user_id", data.user_id); // Store user ID for future requests
                window.location.href = "/dashboard"; // Redirect to dashboard on success
            } else {
                alert(data.error); // Show error message on failure
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

// Handle signup form submission
const signupForm = document.querySelector('.form-box.signup form');

signupForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission
    
    const firstname = document.querySelector('#signupFirstName').value;
    const lastname = document.querySelector('#signupLastName').value;
    const email = document.querySelector('#signupEmail').value;
    const password = document.querySelector('#signupPassword').value;
    const confirmPassword = document.querySelector('#signupConfirmPassword').value;

    fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            firstname: firstname,
            lastname: lastname,
            email: email,
            password: password,
            confirm_password: confirmPassword
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            document.querySelector(".login-link").click(); // Switch to login form
        } else {
            alert(data.error); // Show error message on failure
        }
    })
    .catch(error => console.error('Error:', error));
});

// Fetch and display user data in the sidebar
function loadUserData() {
    const userId = sessionStorage.getItem("user_id");
    if (userId) {
        fetch(`/user/${userId}`)
            .then(response => response.json())
            .then(data => {
                if (data) {
                    document.getElementById('userFirstName').textContent = data.firstname;
                    document.getElementById('userLastName').textContent = data.lastname;
                    document.getElementById('userEmail').textContent = data.email;
                } else {
                    console.error("Error fetching user data");
                }
            })
            .catch(error => console.error("Error:", error));
    }
}

// Fetch and display stocks in the stocks page
function loadStockData() {
    const userId = sessionStorage.getItem("user_id");
    if (userId) {
        fetch(`/api/stocks/${userId}`)
            .then(response => response.json())
            .then(data => {
                const stocksContainer = document.getElementById('stocksContainer'); // Make sure this ID matches your HTML
                stocksContainer.innerHTML = ''; // Clear previous content

                data.stocks.forEach(stock => {
                    const stockElement = document.createElement('div');
                    stockElement.classList.add('stock-item');
                    stockElement.innerHTML = `
                        <h3>${stock.companyName}</h3>
                        <p>Ticker: ${stock.ticker}</p>
                        <p>Price: $${stock.price}</p>
                    `;
                    stocksContainer.appendChild(stockElement);
                });
            })
            .catch(error => console.error("Error fetching stock data:", error));
    }
}

// Call functions when loading respective pages
if (window.location.pathname === '/dashboard') {
    loadUserData();
} else if (window.location.pathname === '/stocks') {
    loadUserData();
    loadStockData();
}
