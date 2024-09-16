# import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
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

# Create tables
query = """
create table IF NOT EXISTS main.transaction_types
(
    Type TEXT not null
        constraint transaction_types_pk
            primary key
);
"""
db.execute(query)

query = """
create table IF NOT EXISTS users
(
    id       INTEGER                  not null
        primary key autoincrement,
    username TEXT                     not null,
    hash     TEXT                     not null,
    cash     NUMERIC default 10000.00 not null
);
"""
db.execute(query)

query = """
create table IF NOT EXISTS portfolio
(
    Symbol TEXT    not null,
    Shares INTEGER not null,
    User   INTEGER not null
        constraint portfolio_users_id_fk
            references users,
    unique (Symbol, User)
);
"""
db.execute(query)

query = """
create table IF NOT EXISTS transactions
(
    Id        integer                            not null
        constraint transactions_pk
            primary key autoincrement,
    User      integer                            not null
        constraint transactions_users_id_fk
            references users,
    Stock     TEXT                               not null,
    Amount    integer                            not null,
    Price     float                              not null,
    Total     float                              not null,
    Timestamp datetime default current_timestamp not null,
    Type      text                               not null
        constraint transactions_transaction_types_Type_fk
            references transaction_types
);
"""
db.execute(query)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    if request.method == "GET":
        # user_owned_stocks = db.execute("SELECT Stock, SUM(Amount) as 'shares', Price, SUM(Total) as 'total'"
        #                                " FROM transactions WHERE User = ? AND Type = ? GROUP BY Stock", user_id,
        #                                'buy')

        # Get user's stocks
        user_owned_stocks = db.execute("SELECT Symbol, SUM(Shares) as 'shares' FROM portfolio WHERE User = ? GROUP BY "
                                       "Symbol", user_id)

        # Get user's cash
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

        user_cash = f"%.2f" % user_cash[0]['cash']
        user_cash = float(user_cash)

        stock_total_value = 0

        for stock in user_owned_stocks:
            if stock['shares'] >= 1:
                valid_stock = lookup(stock['Symbol'])
                stock_quantity = int(stock['shares'])
                valid_stock_price = valid_stock['price']

                stock_total_value += valid_stock_price * stock_quantity
                stock_total_value = f"%.2f" % float(stock_total_value)
                valid_stock_price = f"%.2f" % float(valid_stock_price)
                valid_stock_price = usd(float(valid_stock_price))
                stock_total_value = float(stock_total_value)

                stock['price'] = valid_stock_price
                stock['total'] = usd(stock_total_value)

        user_total_assets = user_cash + stock_total_value
        user_total_assets = f"%.2f" % user_total_assets
        user_total_assets = usd(float(user_total_assets))

        return render_template("index.html", user_stocks=user_owned_stocks, user_cash=usd(user_cash),
                               user_total_assets=user_total_assets)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        user_input_symbol = request.form.get("symbol")
        shares_quantity = request.form.get("shares")

        # Validate user's input
        valid_share = lookup(user_input_symbol)

        # Ensure symbol was submitted
        if not user_input_symbol:
            return apology("Missing symbol", 400)

        if not shares_quantity:
            return apology("Missing shares", 400)

        if not shares_quantity.isdigit():
            return apology("Please enter a number", 400)

        if float(shares_quantity) < 0:
            return apology("Positive integer required", 400)

        if not valid_share:
            return apology("Invalid symbol", 400)
        else:
            symbol = valid_share["symbol"]
            share_price = float(valid_share["price"])

            get_user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

            user_available_cash = float(get_user_cash[0]["cash"])
            purchase_value = float(shares_quantity) * share_price

            if user_available_cash >= purchase_value:
                user_available_cash = user_available_cash - purchase_value

                # Add transaction information to the transactions table
                if user_id and symbol and shares_quantity and share_price and purchase_value:
                    purchase_value = f"%.2f" % purchase_value
                    user_available_cash = f"%.2f" % user_available_cash
                    share_price = f"%.2f" % share_price

                    # Add bought stock to the portfolio table
                    added_stock = db.execute("INSERT INTO portfolio (Symbol, Shares, User) VALUES (?, ?, ?) ON "
                                             "CONFLICT(Symbol, User) DO UPDATE SET Shares = Shares + "
                                             "excluded.Shares", symbol, shares_quantity, user_id)

                    added_transaction = db.execute("INSERT INTO transactions (User, Stock, Amount, Price, Total, "
                                                   "Type) VALUES (?, ?, ?, ?, ?, ?)", user_id, symbol,
                                                   shares_quantity, share_price, purchase_value, 'buy')

                    # Edit user cash column in users table
                    updated_user_cash = db.execute("UPDATE users SET cash = ? WHERE id = ?",
                                                   user_available_cash, user_id)

                    if added_stock and added_transaction and updated_user_cash:
                        flash("Bought!")
                else:
                    return apology("Something went wrong", 400)
            else:
                return apology("Not enough money to buy shares", 400)

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    if request.method == "GET":
        user_transactions = db.execute("SELECT * FROM transactions WHERE User = ?", user_id)

        if len(user_transactions) > 0:
            for transaction in user_transactions:
                transaction['Price'] = f"%.2f" % transaction['Price']
                transaction['Price'] = usd(float(transaction['Price']))
                if transaction['Type'] == 'sell':
                    transaction['Amount'] = '-' + str(transaction['Amount'])
        return render_template("history.html", transactions=user_transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"], request.form.get("password")
        ):
            return apology("Invalid username and/or password", 403)

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
    """Get stock quote"""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Ensure symbol was submitted
        if not symbol:
            return apology("Missing symbol", 400)

        valid_symbol = lookup(symbol)

        if not valid_symbol:
            return apology("Invalid symbol", 400)

        valid_symbol['price'] = usd(valid_symbol['price'])

        return render_template("quoted.html", stock=valid_symbol)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conf_password = request.form.get("confirmation")

        name_exists = db.execute("SELECT username FROM users WHERE username = ?", username)

        # Ensure username was submitted
        if not username:
            return apology("Must provide username", 400)

        # Ensure username is not taken
        elif name_exists:
            return apology("Must provide unique username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("Must provide password", 400)

        # Ensure password was confirmed
        elif not conf_password:
            return apology("Must confirm password", 400)

        # Ensure confirm password matches password
        elif password != conf_password:
            return apology("Must match password", 400)

        # Hash password
        hash = generate_password_hash(password, method='pbkdf2', salt_length=16)

        # Insert username into database
        data = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    # Get user owned stocks
    if request.method == "GET":
        user_stocks_to_show = db.execute("SELECT Symbol FROM portfolio WHERE User = ? GROUP BY Symbol",
                                         user_id)

        if len(user_stocks_to_show) >= 1:
            return render_template("sell.html", user_stocks_to_show=user_stocks_to_show)

    # Sell stocks
    if request.method == "POST":
        user_selected_symbol = request.form.get("symbol")
        user_selected_stock_quantity = request.form.get("shares")
        user_selected_stock_quantity = int(user_selected_stock_quantity)

        valid_symbol = lookup(user_selected_symbol)
        symbol = valid_symbol['symbol']
        stock_price = valid_symbol['price']

        if not user_selected_symbol:
            return apology("Missing symbol", 400)

        if not user_selected_stock_quantity:
            return apology("Missing shares", 400)

        # Get user portfolio data
        user_portfolio = db.execute("SELECT Symbol, Shares FROM portfolio WHERE User = ? AND Symbol = ?", user_id,
                                    symbol)

        stock_quantity = int(user_portfolio[0]['Shares'])

        if user_selected_stock_quantity > stock_quantity:
            return apology("Too many shares", 400)
        else:
            # Update user's portfolio
            updated_stock_quantity = stock_quantity - user_selected_stock_quantity

            updated_portfolio_data = db.execute("UPDATE portfolio SET Shares = ? WHERE Symbol = ?",
                                                updated_stock_quantity, symbol)

            if updated_stock_quantity < 1:
                deleted_stock_from_portfolio = db.execute("DELETE FROM portfolio WHERE Symbol = ?", symbol)

            transaction_total_amount = int(user_selected_stock_quantity) * float(stock_price)

            # Add the transaction to transactions table
            added_transaction = db.execute(
                "INSERT INTO transactions (User, Stock, Amount, Price, Total, Type) VALUES (?, ?, ?, ?, ?, ?)", user_id,
                symbol, user_selected_stock_quantity, stock_price, transaction_total_amount, 'sell')

            # Update user's cash
            user_available_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
            user_available_cash_amount = float(user_available_cash[0]['cash'])

            updated_cash = user_available_cash_amount + transaction_total_amount
            updated_user_cash = db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

            # Show message
            if updated_portfolio_data and added_transaction and updated_user_cash:
                flash('Sold')

            return redirect("/")
    else:
        return render_template("sell.html")
