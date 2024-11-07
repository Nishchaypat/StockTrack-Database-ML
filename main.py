from flask import Flask, request, jsonify
from sql_connect import sql_connector
import re

app = Flask(__name__)

class StockTrack:

    def __init__(self):
        self.db = sql_connector()
        self.user_id = None

    def register(self, firstname, lastname, email, password):
        # Registration validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {"status": "error", "message": "Invalid email format"}
        
        response = self.db.register(firstname, lastname, email, password)
        return {"status": "success"} if response else {"status": "error", "message": "Registration failed"}

    def login(self, email, password):
        response = self.db.login(email, password)
        if response:
            self.user_id = int(response[0])
            return {"status": "success", "user_id": self.user_id}
        else:
            return {"status": "error", "message": "Login failed"}

    def portfolio(self, ticker):
        response = self.db.insert_portfolio(self.user_id, ticker)
        return {"status": "success"} if response else {"status": "error", "message": "Error adding company to portfolio"}

    def delete_user(self):
        response = self.db.delete_user(self.user_id)
        return {"status": "success"} if response else {"status": "error", "message": "Error deleting user"}

    def delete_company(self, ticker):
        response = self.db.delete_company_from_portfolio(self.user_id, ticker)
        return {"status": "success"} if response else {"status": "error", "message": "Error deleting company from portfolio"}

    def view_portfolio(self):
        response = self.db.search_portfolio(self.user_id)
        return {"portfolio": response}

    def change_password(self, new_password):
        response = self.db.update_password(self.user_id, new_password)
        return {"status": "success"} if response else {"status": "error", "message": "Error changing password"}

st = StockTrack()

# Flask Routes
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')
    result = st.register(firstname, lastname, email, password)
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    result = st.login(email, password)
    return jsonify(result)

@app.route('/portfolio', methods=['POST'])
def add_to_portfolio():
    if st.user_id:
        data = request.json
        ticker = data.get('ticker')
        result = st.portfolio(ticker)
        return jsonify(result)
    else:
        return jsonify({"status": "error", "message": "User not logged in"}), 401

@app.route('/delete_user', methods=['POST'])
def delete_user_account():
    if st.user_id:
        result = st.delete_user()
        return jsonify(result)
    else:
        return jsonify({"status": "error", "message": "User not logged in"}), 401

@app.route('/delete_company', methods=['POST'])
def delete_company():
    if st.user_id:
        data = request.json
        ticker = data.get('ticker')
        result = st.delete_company(ticker)
        return jsonify(result)
    else:
        return jsonify({"status": "error", "message": "User not logged in"}), 401

@app.route('/view_portfolio', methods=['GET'])
def view_portfolio():
    if st.user_id:
        result = st.view_portfolio()
        return jsonify(result)
    else:
        return jsonify({"status": "error", "message": "User not logged in"}), 401

@app.route('/change_password', methods=['POST'])
def change_password():
    if st.user_id:
        data = request.json
        new_password = data.get('new_password')
        result = st.change_password(new_password)
        return jsonify(result)
    else:
        return jsonify({"status": "error", "message": "User not logged in"}), 401

if __name__ == '__main__':
    app.run(debug=True)
