from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from sql_connect import sql_connector
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests
db = sql_connector()  # Shared database instance for all routes

@app.route('/')
def index():
    return render_template('index.html')  # Main landing page (frontend HTML)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # Validations
    if not firstname or not lastname:
        return jsonify({"error": "First and last names are required."}), 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Invalid email format."}), 400
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match."}), 400
    if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
        return jsonify({"error": "Password must be at least 8 characters with letters and numbers."}), 400

    # Register user
    response = db.register(firstname, lastname, email, password)
    if response:
        return jsonify({"message": "Registration successful."}), 201
    else:
        return jsonify({"error": "Error during registration."}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    response = db.login(email, password)

    if response:
        return jsonify({"message": "Login successful.", "user_id": response[0]}), 200
    else:
        return jsonify({"error": "Login failed. Check credentials."}), 401

@app.route('/portfolio', methods=['POST'])
def add_to_portfolio():
    data = request.get_json()
    user_id = data.get("user_id")
    ticker = data.get("ticker")

    response = db.insert_portfolio(user_id, ticker)
    if response:
        return jsonify({"message": f"Company {ticker} added to portfolio."}), 200
    else:
        return jsonify({"error": f"Error adding {ticker} to portfolio."}), 500

@app.route('/portfolio', methods=['DELETE'])
def delete_company():
    data = request.get_json()
    user_id = data.get("user_id")
    ticker = data.get("ticker")

    response = db.delete_company_from_portfolio(user_id, ticker)
    if response:
        return jsonify({"message": f"Company {ticker} removed from portfolio."}), 200
    else:
        return jsonify({"error": f"Error deleting {ticker} from portfolio."}), 500

@app.route('/portfolio/<int:user_id>', methods=['GET'])
def view_portfolio(user_id):
    response = db.search_portfolio(user_id)
    if response:
        return jsonify({"portfolio": response}), 200
    else:
        return jsonify({"error": "No portfolio data found."}), 404

@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    user_id = data.get("user_id")
    new_password = data.get("new_password")

    if len(new_password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    response = db.update_password(user_id, new_password)
    if response:
        return jsonify({"message": "Password changed successfully."}), 200
    else:
        return jsonify({"error": "Error changing password."}), 500

@app.route('/delete_account', methods=['DELETE'])
def delete_account():
    data = request.get_json()
    user_id = data.get("user_id")

    response = db.delete_user(user_id)
    if response:
        return jsonify({"message": "Account deleted successfully."}), 200
    else:
        return jsonify({"error": "Error deleting account."}), 500

# Fetch user information for sidebar display
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    user_info = db.get_user_info(user_id)
    if user_info:
        return jsonify(user_info), 200
    else:
        return jsonify({"error": "User not found."}), 404

# Fetch stocks associated with a user
@app.route('/api/stocks/<int:user_id>', methods=['GET'])
def get_user_stocks(user_id):
    stocks = db.get_user_stocks(user_id)
    if stocks:
        return jsonify({"stocks": stocks}), 200
    else:
        return jsonify({"error": "No stocks found for user."}), 404

if __name__ == "__main__":
    app.run(debug=True)
