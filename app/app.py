from database import PostgresDatabase

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def index():
    db = PostgresDatabase()
    stored_words = db.get_words()
    db.close()
    words = [x[2] for x in stored_words]
    return render_template("index.html", words=words)


@app.route("/add_word", methods=["POST"])
def create_word():
    word = request.form['word']

    db = PostgresDatabase()
    db.add_word(word)
    db.close()
    return redirect(url_for("index"))
