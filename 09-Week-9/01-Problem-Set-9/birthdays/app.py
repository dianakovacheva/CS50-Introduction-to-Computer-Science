import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))

        if not name:
            return redirect("/")

        if not month or month < 1 or month > 12:
            print(f"### {month} is not in the range. ###")
            return redirect("/")

        if not day or day < 1 or day > 31:
            print(f"### {day} is not in the range. ###")
            return redirect("/")

        data = db.execute(
            "INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        data = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", data=data)


@app.route("/", methods=["DELETE"])
def delete():
    if request.method == "DELETE":
       recordId = request.args.get("id")

       db.execute(f"DELETE FROM birthdays WHERE id = {recordId}")

       resp = jsonify(success=True)
       resp.status_code = 200
       return resp

