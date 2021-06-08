import os

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# TODO error handling
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]
db = SQLAlchemy(app)


class Language(db.Model):
    id = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Language %r>' % self.id


# TODO unique (lang, word)
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), unique=False, nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=False)

    def __repr__(self):
        return '<Word %r>' % self.word


class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=False)
    text = db.Column(db.String(250), nullable=False)


db.create_all() 
db.session.commit()

# TODO move crud to own module
def add_language(code: str, name: str, session) -> str:
    language = Language(id=code.lower(), name=name.lower())
    session.add(language)
    session.commit()
    return language.id


def add_word(text: str) -> int:
    word = Word(word=text, language_id=9)
    db.session.add(word)
    db.session.commit()
    return word.id


def add_sentence(text: str, language_id: int) -> int:
    sentence = Sentence(text=text, language_id=language_id)
    db.session.add(sentence)
    db.session.commit() 
    return sentence.id


add_language(code="DE", name="German", session=db.session)
add_language(code="FR", name="French", session=db.session)


add_sentence(text="Das habe ich schon gesagt.", language_id=1)


@app.route('/')
def index():
    words = Word.query.all()
    languages = Language.query.all()
    sentences = Sentence.query.all()
    return render_template("index.html", words=words, languages=languages, sentences=sentences)


@app.route("/add_word", methods=["POST"])
def create_word():
    word_text = request.form['word']
    add_word(word_text)
    return redirect(url_for("index"))


@app.route("/flashcards-demo")
def flashcards_demo():
    answer = "Die Katze ist schwarz."
    answer_hinted = "D.. K.... i.. s......"
    question = "The cat is black"
    return render_template("flashcards_demo.html", question=question, answer=answer)
