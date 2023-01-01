import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from time import strftime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Create new tables for all transactions and user stocks
db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER, user_id NUMERIC NOT NULL, symbol TEXT NOT NULL, \
            name TEXT NOT NULL, shares NUMERIC NOT NULL, price NUMERIC NOT NULL, time TEXT, PRIMARY KEY(id), \
            FOREIGN KEY(user_id) REFERENCES users(id))")

db.execute("CREATE TABLE IF NOT EXISTS stocks (id INTEGER, user_id NUMERIC NOT NULL, symbol TEXT NOT NULL, \
            name TEXT NOT NULL, shares NUMERIC NOT NULL, PRIMARY KEY(id), FOREIGN KEY(user_id) REFERENCES users(id))")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    """Show portfolio of stocks"""
    rows = db.execute("SELECT * FROM stocks WHERE user_id=?", session["user_id"])

    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

    total_stock_price_all = 0
    current_price = 0
    total_stock_price = 0

    for row in rows:
        current_price = lookup(row["symbol"])["price"]
        total_stock_price = current_price * int(row["shares"])
        total_stock_price_all += total_stock_price

    grand_total = total_stock_price_all + cash
    return render_template("portfolio.html", rows=rows, price=usd(current_price), total=usd(total_stock_price), cash=usd(cash), grand=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
        stock_dict = lookup(request.form.get("symbol"))
        number = request.form.get("shares")

        try:
            number = int(number)
        except:
            return apology("Invalid amount")
        if stock_dict is None:
            return apology("Invalid Symbol")
        if number <= 0:
            return apology("Invalid amount")

        price_per_share = stock_dict["price"]
        total_price = float(price_per_share) * number
        available_cash = rows[0]["cash"]

        if total_price > available_cash:
            return apology("Not enough cash")
        else:
            date = strftime('%Y-%m-%d %H:%M:%S')
            db.execute("UPDATE users SET cash=? WHERE id=?", available_cash - total_price, session["user_id"])
            db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, time) VALUES (?,?,?,?,?,?)", \
                       session["user_id"], stock_dict["symbol"], stock_dict["name"], number, total_price, date)

            instock = db.execute("SELECT symbol FROM stocks WHERE user_id=? and symbol=?", session["user_id"], stock_dict["symbol"])

            if not instock:
                db.execute("INSERT INTO stocks (user_id, symbol, name, shares) VALUES (?,?,?,?)", \
                           session["user_id"], stock_dict["symbol"], stock_dict["name"], number)

            else:
                old_amount = db.execute("SELECT shares FROM stocks WHERE user_id=? and symbol=?", session["user_id"], \
                                        stock_dict["symbol"])[0]["shares"]
                db.execute("UPDATE stocks SET shares=? WHERE user_id=? AND symbol=?", \
                           (number + old_amount), session["user_id"], stock_dict["symbol"])

            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM transactions WHERE user_id=?", session["user_id"])
    return render_template("history.html", rows=rows)


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


@app.route("/change", methods=["GET", "POST"])
def change():
    """Log user out"""
    # Redirect user to login form
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        rows = db.execute("SELECT * FROM users WHERE username = ?", name)

        if not name:
            return apology("Invalid Username")
        if not password or not confirmation or password != confirmation:
            return apology("Invalid Password")
        if len(rows) == 0:
            return apology("Account does not exist")

        db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(password), rows[0]["id"])
        return render_template("login.html")

    else:
        return render_template("change.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        stock = request.form.get("symbol")
        stock_dict = lookup(stock)
        if stock_dict is None:
            return apology("Stock Not Found")
        else:
            return render_template("quoted.html", stock_dict=stock_dict)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        rows = db.execute("SELECT * FROM users WHERE username = ?", name)

        if not name:
            return apology("Invalid Username")
        if not password or not confirmation or password != confirmation:
            return apology("Invalid Password")
        if len(rows) == 1:
            return apology("Account already exists")

        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", name, generate_password_hash(password))

        rows = db.execute("SELECT * FROM users WHERE username = ?", name)
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    rows = db.execute("SELECT * FROM stocks WHERE user_id=?", session["user_id"])

    if request.method == "POST":
        symbol = request.form.get("symbol")
        number = int(request.form.get("shares"))
        stock_dict = lookup(symbol)
        available = db.execute("SELECT shares FROM stocks WHERE user_id=? AND symbol=?", session["user_id"], symbol)[0]["shares"]
        date = strftime('%Y-%m-%d %H:%M:%S')

        if not number:
            return apology("Invalid amount")
        if not symbol:
            return apology("Invalid symbol")
        if not available:
            return apology("No shares")
        if number > available or number <= 0:
            return apology("Invalid amount")

        # Update cash
        quote = lookup(symbol)
        price_per_share = float(quote["price"])
        total_value = price_per_share * number
        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        db.execute("UPDATE users SET cash=? WHERE id=?", rows[0]["cash"] + total_value, session["user_id"])

        # Update transaction
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, time) VALUES (?,?,?,?,?,?)", \
                   session["user_id"], symbol, stock_dict["name"], -number, total_value, date)

        # Update stock amount
        if number == available:
            db.execute("DELETE FROM stocks WHERE user_id=? and symbol=?", session["user_id"], symbol)
        else:
            db.execute("UPDATE stocks SET shares=? WHERE user_id=? and symbol=?", available - number, session["user_id"], symbol)

        return redirect("/")

    else:
        return render_template("sell.html", rows=rows)
