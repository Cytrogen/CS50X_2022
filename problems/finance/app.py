import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

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

    balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    balance_total = balance
    portfolio = db.execute("SELECT symbol, SUM(quantity) FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
    prices = []
    cash_new = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Calculate the total balance by times prices of each symbol to the quantities of shares
    # enumerate() -> adds counter to an iterable and returns it in a form of enumerating object
    for i, owned in enumerate(portfolio):
        temp = lookup(owned["symbol"])["price"]
        prices.append(temp)
        balance_total += portfolio[i]["SUM(quantity)"] * prices[i]

    return render_template("index.html", portfolio=portfolio, prices=prices, balance_total=balance_total, balance=balance, cash_new=cash_new)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        if request.form.get("shares"):
            # If the number is a number
            if str(request.form.get("shares")).isdigit():
                # If the number is a whole number
                if int(request.form.get("shares")) % 1 == 0:
                    # If negative number
                    if int(request.form.get("shares")) < 0:
                        return apology("must provide valid number of shares", 400)
                else:
                    return apology("must provide valid number of shares", 400)
            else:
                return apology("must provide valid number of shares", 400)
        else:
            return apology("must provide valid number of shares", 400)
        symbol = lookup(request.form.get("symbol"))
        if not symbol:
            return apology("symbol not found", 400)

        price = symbol["price"]
        # Get the new cash balance by subtracting the shares from cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        cash_new = cash - (price * int(request.form.get("shares")))

        # Check if enough cash to complete the purchase
        if cash_new < 0:
            return apology("can't afford shares")
        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash_new, session["user_id"])
            db.execute("INSERT INTO transactions (user_id, symbol, quantity, price)VALUES(?, ?, ?, ?)",
                       session["user_id"], request.form.get("symbol"), int(request.form.get("shares")), price)

            return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    portfolio = db.execute(
        "SELECT id, symbol, quantity, price FROM transactions WHERE user_id = ? ORDER BY id DESC", session["user_id"])

    return render_template("history.html", portfolio=portfolio)


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


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change():
    """Customized function"""
    """Change user's password"""

    if request.method == "POST":
        if not request.form.get("password_old"):
            return apology("must provide old password", 403)

        if not request.form.get("password_new"):
            return apology("must provide new password", 403)

        if not request.form.get("password_new_confirm"):
            return apology("must provide new password confirmation", 403)

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # If old password does not match hashed password
        if not check_password_hash(rows[0]["hash"], request.form.get("password_old")):
            return apology("incorrect old password", 403)

        # If new passwords don't match
        if request.form.get("password_new") != request.form.get("password_new_confirm"):
            return apology("confirmation does not match", 403)
        else:
            hash = generate_password_hash(request.form.get("password_new"))

        # Insert the user inputs into the database
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_password.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        result = lookup(request.form.get("symbol"))

        if not result:
            return apology("symbol not found", 400)

        return render_template("quote.html", results=result)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Get user's username and password inputs
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("must match your previous password", 400)
        else:
            hash = generate_password_hash(request.form.get("password"))

        # Check username's availability
        check = db.execute("SELECT username FROM users WHERE username=?", request.form.get("username"))
        if len(check) > 0:
            return apology("username is not available", 400)

        # Insert the user inputs into the database
        db.execute("INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)", request.form.get("username"), hash, 10000.00)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    portfolio = db.execute("SELECT symbol, SUM(quantity) FROM transactions WHERE user_id=? GROUP BY symbol", session["user_id"])

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("symbol not found", 400)

        if request.form.get("shares"):
            # If the number is a number
            if str(request.form.get("shares")).isdigit():
                try:
                    # If the number is a whole number
                    if int(request.form.get("shares")) % 1 == 0:
                        # If negative number
                        if int(request.form.get("shares")) < 0:
                            return apology("must provide valid number of shares", 400)
                    else:
                        return apology("must provide valid number of shares", 400)
                except ValueError:
                    return apology("must provide valid number of shares", 400)
            else:
                return apology("must provide valid number of shares", 400)
        else:
            return apology("must provide valid number of shares", 400)

        # If share is less than user's owned share
        shares_available = db.execute("SELECT quantity FROM transactions WHERE user_id = ? AND symbol = ?",
                                      session["user_id"], request.form.get("symbol"))
        shares = shares_available[0]
        if int(request.form.get("shares")) > int(shares["quantity"]):
            return apology("not enough shares", 400)

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        symbol = request.form.get("symbol")
        price = lookup(symbol)["price"]
        cash_new = cash + (int(request.form.get("shares")) * price)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash_new, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, quantity, price) VALUES(?, ?, ?, ?)",
                   session["user_id"], symbol, -int(request.form.get("shares")), price)

        return redirect("/")

    return render_template("sell.html", portfolio=portfolio)