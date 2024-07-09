# import os
from app import app
from app.audioTrans import textExtractor
from deep_translator import GoogleTranslator

# # Create a SQLAlchemy Engine:
app.config['UPLOAD_FOLDER'] = "app/vids/"

import os
from app import app
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Details(Base):
    __tablename__ = 'details'
    id = Column(Integer, primary_key=True)
    email = Column(String(41), nullable=False)
    vidName = Column(String(200), nullable=False)

    def __repr__(self):
        return f"{self.id}-{self.vidName}"

# Create a SQLAlchemy Engine:
engine = create_engine('sqlite:///app/database/database.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route("/")
@app.route("/index")
def index():
    return render_template("public/index.html")

@app.route("/test", methods=["GET", "POST"])
def langspecify():
    if request.method == "POST":
        lang = request.form.get("dropdown")
        print(str(lang))
        if str(lang) == "Spanish":
            return redirect(url_for("spanish"))
        elif str(lang) == "Hindi":
            return redirect(url_for("hindi"))
        elif str(lang) == "French":
            return redirect(url_for("french"))
        elif str(lang) == "English":
            return redirect(url_for("english"))
        return redirect(request.url)

    return render_template("public/test.html")

@app.route("/spanish", methods=["GET", "POST"])
def find():
    if request.method == "POST":
        em = request.form.get("email")
        file = request.files['file']
        # print(file)
        filename = secure_filename(file.filename) # type: ignore
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        det = Details(email=em, vidName=os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        session.add(det)
        session.commit()
        print("Added successfully")

        # here filename has extension mp4 or whatever but not wav.
        subs = textExtractor(filename)
        print(subs)
        espLang = GoogleTranslator(source="auto", target="es").translate(subs)
        return render_template("public/spanish.html", subs=espLang)

    return render_template("public/spanish.html")

@app.route('/spanish')
def spanish():
    return render_template("public/spanish.html")

@app.route("/hindi", methods=["GET", "POST"])
def findHindi():
    if request.method == "POST":
        em = request.form.get("email")
        file = request.files['file']
        print(file)
        filename = secure_filename(file.filename) # type: ignore
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        det = Details(email=em, vidName=os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        session.add(det)
        session.commit()
        print("Added successfully")

        # here filename has extension mp4 or whatever but not wav.
        subs = textExtractor(filename)
        print(subs)
        hiLang = GoogleTranslator(source="auto", target="hi").translate(subs)
        return render_template("public/hindi.html", subs=hiLang)

    return render_template("public/hindi.html")

@app.route('/hindi')
def hindi():
    return render_template("public/hindi.html")

#FOR FRENCH

@app.route("/french", methods=["GET", "POST"])
def findFrench():
    if request.method == "POST":
        em = request.form.get("email")
        file = request.files['file']
        print(file)
        filename = secure_filename(file.filename) # type: ignore
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        det = Details(email=em, vidName=os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        session.add(det)
        session.commit()
        print("Added successfully")

        # here filename has extension mp4 or whatever but not wav.
        subs = textExtractor(filename)
        print(subs)
        hiLang = GoogleTranslator(source="auto", target="fr").translate(subs)
        return render_template("public/french.html", subs=hiLang)

    return render_template("public/french.html")

@app.route('/french')
def french():
    return render_template("public/french.html")

#FOR ENGLISH
@app.route("/english", methods=["GET", "POST"])
def findEnglish():
    if request.method == "POST":
        em = request.form.get("email")
        file = request.files['file']
        print(file)
        filename = secure_filename(file.filename) # type: ignore
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        det = Details(email=em, vidName=os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        session.add(det)
        session.commit()
        print("Added successfully")

        # here filename has extension mp4 or whatever but not wav.
        subs = textExtractor(filename)
        print(subs)
        hiLang = GoogleTranslator(source="auto", target="en").translate(subs)
        return render_template("public/english.html", subs=hiLang)

    return render_template("public/english.html")

@app.route('/english')
def english():
    return render_template("public/english.html")

