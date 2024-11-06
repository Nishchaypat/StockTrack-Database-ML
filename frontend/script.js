const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const signupLink = document.querySelector('.signup-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');
let userId = null; // to store logged-in user's ID

// Event listeners for toggling forms
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

// Register user
document.getElementById('signup-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const firstname = document.getElementById('signup-firstname').value;
    const lastname = document.getElementById('signup-lastname').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    try {
        const response = await fetch('http://localhost:8000/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ firstname, lastname, email, password }),
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
        } else {
            alert(result.detail);
        }
    } catch (error) {
        console.error('Error during registration:', error);
        alert('Registration failed. Please try again.');
    }
});

// Login user
document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch('http://localhost:8000/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            userId = result.user_id; // Store user ID for later use
        } else {
            alert(result.detail);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('Login failed. Please try again.');
    }
});

// Add company to portfolio
async function addToPortfolio(ticker) {
    if (!userId) {
        alert('Please log in first.');
        return;
    }
    try {
        const response = await fetch(`http://localhost:8000/portfolio/${userId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ticker }),
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
        } else {
            alert(result.detail);
        }
    } catch (error) {
        console.error('Error adding to portfolio:', error);
        alert('Failed to add to portfolio. Please try again.');
    }
}

// Remove company from portfolio
async function removeFromPortfolio(ticker) {
    if (!userId) {
        alert('Please log in first.');
        return;
    }
    try {
        const response = await fetch(`http://localhost:8000/portfolio/${userId}/${ticker}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
        } else {
            alert(result.detail);
        }
    } catch (error) {
        console.error('Error removing from portfolio:', error);
        alert('Failed to remove from portfolio. Please try again.');
    }
}

// View user portfolio
async function viewPortfolio() {
    if (!userId) {
        alert('Please log in first.');
        return;
    }
    try {
        const response = await fetch(`http://localhost:8000/portfolio/${userId}/`, {
            method: 'GET',
        });

        if (response.ok) {
            const portfolioData = await response.json();
            console.log('Portfolio:', portfolioData);
            // You can render the portfolio data here as needed
        } else {
            alert('Portfolio not found');
        }
    } catch (error) {
        console.error('Error fetching portfolio:', error);
        alert('Failed to retrieve portfolio. Please try again.');
    }
}

// Change password
async function changePassword(newPassword) {
    if (!userId) {
        alert('Please log in first.');
        return;
    }
    try {
        const response = await fetch(`http://localhost:8000/users/${userId}/password/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ new_password: newPassword }),
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
        } else {
            alert(result.detail);
        }
    } catch (error) {
        console.error('Error changing password:', error);
        alert('Failed to change password. Please try again.');
    }
}
