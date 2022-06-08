import os
from app import app
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func  # what is this even doing?
from app.audioTrans import textExtractor

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join("database", 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "app/vids/"

db = SQLAlchemy(app)


class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(41), nullable=False)
    vidName = db.Column(db.String(200), nullable=False)

    def __repr(self) -> str:
        return f"{self.id}-{self.vidName}"


db.create_all()


@app.route("/")
@app.route("/home")
def home():
    return render_template("public/home.html")


@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        em = request.form.get("email")
        file = request.files['file']
        print(file)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        det = Details(email=em, vidName=os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        db.session.add(det)
        db.session.commit()
        print("Added successfully")

        # here filename has extension mp4 or whatever but not wav.
        subs = textExtractor(filename)
        print(subs)
        return redirect(request.url)

    return render_template("public/test.html")
