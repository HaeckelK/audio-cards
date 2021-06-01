from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


WORDS = set(["one", "two", "three"])


@app.route('/')
def index():
    words = WORDS
    return render_template("index.html", words=words)


@app.route("/add_word", methods=["POST"])
def create_word():
    word = request.form['word']
    WORDS.add(word)
    return redirect(url_for("index"))
