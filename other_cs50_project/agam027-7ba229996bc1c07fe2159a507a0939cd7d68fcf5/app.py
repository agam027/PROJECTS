import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


wallet_history = 0


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    sys = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session.get("user_id"))

    wallet = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))[0]["cash"]

    random = 0
    for i in range(len(sys)):
        random += (sys[i]["price"] * sys[i]["shares"])

    return render_template("home.html", sys_dict=sys, balance=wallet, temp=random, )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate input
        if not symbol or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid symbol or shares")

        shares = int(shares)
        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid stock symbol")

        price = stock["price"]
        total_cost = price * shares

        user_id = session.get("user_id")
        if not user_id:
            return apology("Session expired, try later")

        # Check user cash
        wallet = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if wallet < total_cost:
            return apology("Not enough money")

        # Deduct cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", wallet - total_cost, user_id)

        # Record transaction
        rows = db.execute(
            "SELECT * FROM portfolio WHERE symbol = ? AND user_id = ?", symbol.upper(), session.get("user_id")
        )

        if len(rows) == 0:
            db.execute("INSERT INTO portfolio (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                       user_id, symbol.upper(), shares, price)
        else:
            have = db.execute("SELECT shares FROM portfolio WHERE symbol = ? AND user_id = ?",
                              symbol.upper(), session.get("user_id"))[0]["shares"]
            db.execute("UPDATE portfolio SET shares = ? WHERE symbol = ? AND user_id = ?",
                       (have+shares), symbol.upper(), session.get("user_id"))

        db.execute("INSERT INTO history (symbol, shares, price, user_id, action, time) VALUES (?, ?, ?, ?, ?, ?)",
                   symbol.upper(), shares, price, session.get("user_id"), "BOUGHT", datetime.now())

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    sys = db.execute("SELECT * FROM history WHERE user_id = ?", session.get("user_id"))

    wallet = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))[0]["cash"]

    random = 0
    for i in range(len(sys)):
        random += (sys[i]["price"] * sys[i]["shares"])

    return render_template("history.html", sys_dict=sys, balance=wallet, temp=random)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return apology("invalid username", 403)

        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid password", 403)

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
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        quotes = lookup(request.form.get("symbol"))
        if quotes == None:
            return apology("wrong symbol!")
        return render_template("quoted.html", quote=quotes)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        if not password or not confirmation:
            return apology("must provide password", 400)
        elif password != confirmation:
            return apology("passwords don't match", 400)

        existed_user = db.execute("SELECT * FROM users WHERE username = ?",
                                  request.form.get("username"))
        # Query database to Ensure username does not exists
        if not existed_user:

            hashed_password = generate_password_hash(request.form.get("password"))

            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       request.form.get("username"), hashed_password)

            print("loged in")

            # Redirect user to login page
            return redirect("/")

    else:
        return render_template("register.html")

    return apology("password can't be saved \n try later")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol or not shares:
            return apology("invalid symbol/shares!")

        limit = db.execute("SELECT shares FROM portfolio WHERE user_id = ? ",
                           session.get("user_id"))[0]["shares"]
        if int(shares) > (limit):
            return apology("too much shares!")
        # Validate input
        if not symbol or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid symbol or shares")

        shares = int(shares)
        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid stock symbol")

        price = stock["price"]
        total_cost = price * shares

        user_id = session.get("user_id")
        if not user_id:
            return apology("Session expired, try later")

        # Check user cash
        wallet = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        # Deduct cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", wallet + total_cost, user_id)

        # Record transaction
        rows = db.execute(
            "SELECT * FROM portfolio WHERE symbol = ? AND user_id = ?", symbol.upper(), session.get("user_id")
        )

        if len(rows) == 0:
            db.execute("INSERT INTO portfolio (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                       user_id, symbol.upper(), shares, price)
        else:
            have = db.execute("SELECT shares FROM portfolio WHERE symbol = ? AND user_id = ?",
                              symbol.upper(), session.get("user_id"))[0]["shares"]
            db.execute("UPDATE portfolio SET shares = ? WHERE symbol = ? AND user_id = ?",
                       (have-shares), symbol.upper(), session.get("user_id"))

        db.execute("INSERT INTO history (symbol, shares, price, user_id, action, time) VALUES (?, ?, ?, ?, ?, ?)",
                   symbol.upper(), shares, price, session.get("user_id"), "SOLD", datetime.now())

        return redirect("/")

    else:
        portf = db.execute("SELECT symbol FROM portfolio WHERE user_id = ?", session.get("user_id"))
        return render_template("sell.html", port=portf)
