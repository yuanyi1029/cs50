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
db = SQL("sqlite:///movies.db")

# Create users, movies and reviews table
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL,\
            hash TEXT NOT NULL)");
db.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, title TEXT NOT NULL,\
            type TEXT NOT NULL, ratings INTEGER NOT NULL, avg_rating REAL NOT NULL)");
db.execute("CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id NUMERIC NOT NULL,\
            movie_id NUMERIC NOT NULL, rating INTEGER NOT NULL, review TEXT NOT NULL, time TEXT NOT NULL,\
            FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (movie_id) REFERENCES movies(id))");


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
    """Show history of user reviews"""
    return reviews()


@app.route("/write", methods=["GET", "POST"])
@login_required
def write():
    """Write a movie review"""
    if request.method == "POST":
        title = request.form.get("title")
        type = request.form.get("type")
        rating = int(request.form.get("rating"))
        review = request.form.get("review")
        date = strftime('%Y-%m-%d %H:%M:%S')

        if not title or not type or not rating or not review:
            return apology("Missing Fields")

        # Check database for the same value
        rows = db.execute("SELECT * FROM movies WHERE title=? AND type=?", title, type)

        # Update movies database
        if len(rows) == 0:
            db.execute("INSERT INTO movies (title, type, ratings, avg_rating) VALUES (?,?,?,?)", title, type, 1, rating)

        else:
            old_ratings = rows[0]["ratings"]
            old_avg_rating = rows[0]["avg_rating"]

            db.execute("UPDATE movies SET ratings=?, avg_rating=? WHERE title=? AND type=?", old_ratings + 1, ((old_avg_rating * old_ratings) + rating) / (old_ratings + 1), title, type)

        # Update reviews database
        user_id = session["user_id"]
        movie_id = db.execute("SELECT * FROM movies WHERE title=? AND type=?", title, type)[0]["id"]
        db.execute("INSERT INTO reviews (user_id, movie_id, rating, review, time) VALUES (?,?,?,?,?)", user_id, movie_id, rating, review, date)

        flash("Success! Your Review has been Written!")
        return redirect("/")

    else:
        title = None
        return render_template("write.html", title=title)


@app.route("/reviews")
@login_required
def reviews():
    """Show history of user reviews"""
    id_to_movie = dict()

    rows = db.execute("SELECT * FROM reviews WHERE user_id=?", session["user_id"])
    movie_rows = db.execute("SELECT * FROM movies")

    for i in range(len(movie_rows)):
        id_to_movie[movie_rows[i]["id"]] = [movie_rows[i]["title"], movie_rows[i]["type"]]

    return render_template("reviews.html", rows=rows, dict=id_to_movie)


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


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Search For a movie"""
    if request.method == "POST":
        word = request.form.get("title")
        if not word:
            return apology("Missing Fields")

        word_list = word.rstrip().lstrip().lower().split(" ")
        row_list = []

        for word in word_list:
            rows = db.execute("SELECT * FROM movies WHERE title LIKE ?", '%' + word + '%')
            for row in rows:
                try:
                    row_list.append(row)
                except:
                    break

        # Remove repeated rows from row_list because the databse query might return duplicate rows
        new_row_list = []
        if len(row_list) != 0:
            seen = set()

            for row in row_list:
                temp = tuple(row.items())
                if temp not in seen:
                    seen.add(temp)
                    new_row_list.append(row)

        return render_template("searched.html", row_list=new_row_list)

    else:
        return render_template("search.html")


@app.route("/searched", methods=["GET", "POST"])
@login_required
def searched():
    if request.method == "POST":
        view_title = request.form.get("view")
        write_title = request.form.get("write")

        if not view_title:
            return render_template("write.html", title=write_title)
        elif not write_title:
            movie_id = db.execute("SELECT id FROM movies WHERE title=?", view_title)[0]["id"]
            rows = db.execute("SELECT * FROM reviews WHERE movie_id=?", movie_id)

            id_to_username = dict()
            user_rows = db.execute("SELECT * FROM users")
            for i in range(len(user_rows)):
                id_to_username[user_rows[i]["id"]] = user_rows[i]["username"]
            print(id_to_username)

            return render_template("view.html", title=view_title, rows=rows, dict=id_to_username)

    else:
        return render_template("search.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        rows = db.execute("SELECT * FROM users WHERE username=?", username)

        if not username or not password or not confirmation:
            return apology("Missing Fields")
        if password != confirmation:
            return apology("Passwords do not match")
        if len(rows) != 0:
            return apology("Account already exists")

        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, generate_password_hash(password))

        id = db.execute("SELECT * FROM users WHERE username=?", username)[0]["id"]
        session["user_id"] = id

        flash("Congratulations! Account Registration is Successful!")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/change", methods=["GET", "POST"])
def change():
    """User account password change"""
    # Redirect user to login form
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT * FROM users WHERE username = ?", name)

        if not name or not password or not confirmation:
            return apology("Missing Fields")
        if password != confirmation:
            return apology("Passwords do not match")
        if len(rows) == 0:
            return apology("Account does not exist")

        db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(password), rows[0]["id"])
        flash(f"Password for '{name}' has been changed!")
        return render_template("login.html")

    else:
        return render_template("change.html")