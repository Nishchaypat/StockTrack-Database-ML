from fastapi import FastAPI, HTTPException
from sql_connect import sql_connector
import re

app = FastAPI()
db = sql_connector()

# Register user
@app.post("/register/")
async def register_user(firstname: str, lastname: str, email: str, password: str):
    if not firstname or not lastname or not re.match(r"[^@]+@[^@]+\.[^@]+", email) or len(password) < 8:
        raise HTTPException(status_code=400, detail="Invalid input.")
    
    response = db.register(firstname, lastname, email, password)
    if response:
        return {"message": "Registration successful."}
    else:
        raise HTTPException(status_code=400, detail="Error occurred during registration.")

# User login
@app.post("/login/")
async def login_user(email: str, password: str):
    response = db.login(email, password)
    if response:
        return {"message": "Login successful.", "user_id": response[0]}
    else:
        raise HTTPException(status_code=401, detail="Login failed. Please check your credentials.")

# Add company to portfolio
@app.post("/portfolio/{user_id}/")
async def add_to_portfolio(user_id: int, ticker: str):
    if db.insert_portfolio(user_id, ticker):
        return {"message": f"{ticker} added to portfolio."}
    else:
        raise HTTPException(status_code=400, detail="Failed to add to portfolio.")

# Delete company from portfolio
@app.delete("/portfolio/{user_id}/{ticker}/")
async def remove_from_portfolio(user_id: int, ticker: str):
    if db.delete_company_from_portfolio(user_id, ticker):
        return {"message": f"{ticker} removed from portfolio."}
    else:
        raise HTTPException(status_code=400, detail="Failed to remove from portfolio.")

# View user portfolio
@app.get("/portfolio/{user_id}/")
async def get_portfolio(user_id: int):
    portfolio_data = db.search_portfolio(user_id)
    if portfolio_data:
        return portfolio_data
    else:
        raise HTTPException(status_code=404, detail="Portfolio not found.")

# Change password
@app.put("/users/{user_id}/password/")
async def change_password(user_id: int, new_password: str):
    if db.update_password(user_id, new_password):
        return {"message": "Password changed successfully."}
    else:
        raise HTTPException(status_code=400, detail="Failed to change password.")
