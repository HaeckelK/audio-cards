import os

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# TODO error handling
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]
db = SQLAlchemy(app)


# TODO unique (lang, word)
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Word %r>' % self.word

db.create_all()
db.session.commit()


@app.route('/')
def index():
    words = Word.query.all()
    return render_template("index.html", words=words)


@app.route("/add_word", methods=["POST"])
def create_word():
    word_text = request.form['word']
    word = Word(word=word_text)
    db.session.add(word)
    db.session.commit()
    return redirect(url_for("index"))
