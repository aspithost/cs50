import os

from cs50 import SQL
import datetime
import time
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Create table for stock holdings
db.execute("CREATE TABLE IF NOT EXISTS stock_holdings (user_id INTEGER NOT NULL, stock TEXT NOT NULL,\
        amount INTEGER DEFAULT 0, FOREIGN KEY(user_id) REFERENCES users(id))")

# Create purchases table if it doesn't exist
db.execute("CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
    user_id INTEGER NOT NULL, date NUMERIC NOT NULL, action TEXT NOT NULL, stock TEXT NOT NULL, \
    price NUMERIC NOT NULL, amount INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]

    # Get user balance
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Get list of stocks owned
    stocks = db.execute("SELECT stock, amount FROM stock_holdings WHERE user_id = ?", user_id)

    # Calculate total stock holdings at current prices
    stock_holdings = 0
    show_worst_performing_stocks = False
    if len(stocks) >= 6:
        show_worst_performing_stocks = True

    for stock in stocks:
        # Calculate prices of stocks owned
        stock["price"] = lookup(stock["stock"])["price"]
        total_value = stock["amount"] * stock["price"]
        stock_holdings += total_value

        # Calculate stock value compared to purchase price
        purchases = db.execute("SELECT price, amount \
                               FROM transactions \
                               WHERE user_id = ? \
                               AND stock = ? \
                               AND action = 'buy' \
                               ORDER BY date desc", user_id, stock["stock"])

        # Calculate total value of most recent purchases of stock
        stocks_to_count = stock["amount"]
        total_purchase_value = 0
        while stocks_to_count > 0:
            for purchase in purchases:
                amount, price = purchase["amount"], purchase["price"]

                # If purchase amount exceeds remaining sum of stocks held, exit loop
                if amount > stocks_to_count:
                    total_purchase_value += stocks_to_count * price
                    stocks_to_count = 0
                    break

                total_purchase_value += amount * price
                stocks_to_count -= amount

        # Calculate yield of stock based on current value compared to purchase price
        stock["yield"] = (total_value - total_purchase_value) / total_purchase_value

    return render_template("index.html", stocks=stocks, cash=cash, stock_holdings=stock_holdings, show_worst_performing_stocks=show_worst_performing_stocks)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # Check symbol
        input = request.form.get("symbol").strip()
        if not input:
            return apology("Please enter a stock symbol", 400)

        # Check number of shares
        shares = get_shares(request.form.get("shares"))
        if not shares:
            return apology("Please enter a valid number above 0", 400)

        # Check price of stock
        response = lookup(input)
        if not response:
            return apology("Please enter a valid stock symbol", 400)
        price, symbol = response["price"], response["symbol"]
        cost = round(price * shares, 2)

        # Check user balance
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        if cost > cash:
            return apology("Balance too low, please add more cash", 403)

        # Insert purchase into transactions table
        timestamp = time.time()
        db.execute("INSERT INTO transactions (user_id, date, action, stock, price, amount) \
            VALUES(?, ?, ?, ?, ?, ?)", user_id, timestamp, 'buy', symbol, price, shares)

        # Check if user owns stock
        try:
            amount = db.execute("SELECT amount FROM stock_holdings WHERE user_id = ? AND stock  = ?", user_id, symbol)[0]["amount"]
            # Update stock holdings
            db.execute("UPDATE stock_holdings SET amount = ? WHERE user_id = ? AND stock = ?", amount + shares, user_id, symbol)
        except IndexError:
            # Create new entry in stock holdings
            db.execute("INSERT INTO stock_holdings (user_id, stock, amount) VALUES(?, ?, ?)", user_id, symbol, shares)

        # Deduct cash from users table
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - cost, user_id)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    transactions = db.execute("SELECT date, action, stock, price, amount FROM transactions WHERE user_id = ?", user_id)

    for transaction in transactions:
        transaction["date"] = datetime.datetime.fromtimestamp(transaction["date"]).strftime('%Y-%m-%d %H:%M:%S')

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Stock does not exist", 400)
        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Check if user entered username
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check if user has entered username and if username is still available
        if not username:
            return apology("must provide username", 400)

        elif db.execute("SELECT * FROM users WHERE username = ?", username):
            return apology("username already taken", 400)

        elif not password or not confirmation or password != confirmation:
            return apology("must provide valid passwords", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]

    if request.method == "POST":
        # Check if user entered a valid number of shares to sell
        shares = get_shares(request.form.get("shares"))
        if not shares:
            return apology("Please enter a valid number above 0", 403)

        # Check number of shares user owns of that stock
        symbol = request.form.get("symbol")
        amount = db.execute("SELECT amount FROM stock_holdings WHERE user_id = ? AND stock = ?", user_id, symbol)[0]["amount"]
        print("amount", amount)
        if not amount:
            return apology(f"You do not own any {symbol} stock")
        if shares > amount:
            return apology(f"You do not own that many {symbol} stocks")

        # Get latest price of stock and calculate transaction price
        price = lookup(symbol)["price"]
        transaction_price = price * shares

        # Handle sale of stocks
        timestamp = time.time()

        # Enter transaction into transactions table
        db.execute("INSERT INTO transactions (user_id, date, action, stock, price, amount) \
            VALUES(?, ?, ?, ?, ?, ?)", user_id, timestamp, 'sell', symbol, price, shares)

        # Update user's stock holdings
        db.execute("UPDATE stock_holdings SET amount = amount - ? WHERE user_id = ? AND stock = ?", shares, user_id, symbol)

        # Add cash to users table
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", transaction_price, user_id)

        return redirect("/")

    else:
        stocks = db.execute("SELECT stock, amount FROM stock_holdings WHERE user_id = ?", user_id)
        if not len(stocks):
            return apology("You do not own any stocks", 403)
        return render_template("sell.html", stocks=stocks)


def get_shares(shares):
    try:
        shares = int(shares)
        return shares if shares % 1 == 0 and shares > 0 else None
    except ValueError:
        return None

