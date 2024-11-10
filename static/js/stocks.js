// Fetch stocks from the backend and render them in the stocks container
document.addEventListener('DOMContentLoaded', () => {
    loadStockData();
    loadFavorites(); // Mark any favorite stocks
});

// Load stocks from backend
function loadStockData() {
    const userId = sessionStorage.getItem("user_id");
    if (userId) {
        fetch(`/api/stocks/${userId}`)
            .then(response => response.json())
            .then(data => {
                renderStocks(data.stocks);
            })
            .catch(error => console.error("Error fetching stock data:", error));
    }
}

// Render stocks in the stocks container
function renderStocks(stocks) {
    stocksContainer.innerHTML = ''; // Clear any existing content

    stocks.forEach(stock => {
        const stockRow = document.createElement('div');
        stockRow.classList.add('stock-row');
        stockRow.innerHTML = `
            <span class="dot"></span>
            <span class="company-name">${stock.companyName}</span>
            <span class="stock-symbol">${stock.ticker}</span>
            <span class="sector">${stock.sector || "Unknown"}</span>
            <span class="open-value">${stock.price || "N/A"}</span>
            <span class="star-button">☆</span>
        `;

        const starButton = stockRow.querySelector('.star-button');
        starButton.addEventListener('click', () => toggleFavorite(starButton, stock));

        stocksContainer.appendChild(stockRow);
    });

    loadFavorites(); // Ensure favorites are marked after rendering
}

// Load favorite stocks from local storage
function loadFavorites() {
    const favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    favorites.forEach(favorite => {
        const starButton = Array.from(stocksContainer.querySelectorAll('.stock-row')).find(row => {
            return row.querySelector('.stock-symbol').textContent === favorite.stockSymbol;
        })?.querySelector('.star-button');

        if (starButton) {
            starButton.textContent = '★';
            starButton.classList.add('active');
        }
    });
}

// Toggle favorite status and save to local storage
function toggleFavorite(button, stock) {
    const { companyName, ticker: stockSymbol, sector, price: openValue } = stock;

    if (button.textContent === '☆') {
        // Mark as favorite
        button.textContent = '★';
        button.classList.add('active');
        saveFavorite({ companyName, stockSymbol, sector, openValue });
    } else {
        // Remove from favorites
        button.textContent = '☆';
        button.classList.remove('active');
        removeFavorite(stockSymbol);
    }
}

// Save favorite stock to local storage
function saveFavorite(stock) {
    let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    favorites.push({
        companyName: stock.companyName,
        stockSymbol: stock.stockSymbol,
        sector: stock.sector,
        openValue: stock.openValue
    });
    localStorage.setItem('favorites', JSON.stringify(favorites));
}

// Remove favorite stock from local storage
function removeFavorite(stockSymbol) {
    let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    favorites = favorites.filter(stock => stock.stockSymbol !== stockSymbol);
    localStorage.setItem('favorites', JSON.stringify(favorites));
}

// Get references to the search input, search button, and stock container
const searchInput = document.querySelector('.search-input');
const searchButton = document.querySelector('.search-button');
const stocksContainer = document.querySelector('.stocks-container');

// Function to filter and display stocks based on search query
function filterStocks() {
    const query = searchInput.value.trim().toUpperCase();
    const stockRows = stocksContainer.querySelectorAll('.stock-row');

    stockRows.forEach(row => {
        const stockSymbol = row.querySelector('.stock-symbol').textContent.toUpperCase();
        if (stockSymbol.startsWith(query)) {
            row.style.display = 'flex';
        } else {
            row.style.display = 'none';
        }
    });
}

// Listen for the 'input' event on the search bar for real-time filtering
searchInput.addEventListener('input', filterStocks);

// Listen for the 'click' event on the search button to filter stocks
searchButton.addEventListener('click', (event) => {
    event.preventDefault();
    filterStocks();
});
