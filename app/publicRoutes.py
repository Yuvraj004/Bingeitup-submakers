import os
from app import app
from app.audioTrans import textExtractor
from deep_translator import GoogleTranslator

# # Create a SQLAlchemy Engine:
app.config['UPLOAD_FOLDER'] = "app/vids/"
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')

import os
from app import app
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for,flash, send_from_directory
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session

Base = declarative_base()

class Details(Base):
    __tablename__ = 'details'
    id = Column(Integer, primary_key=True)
    email = Column(String(41), nullable=False)
    vidName = Column(String(200), nullable=False)

    def __repr__(self):
        return f"{self.id}-{self.vidName}"

# Create a SQLAlchemy Engine:
# engine = create_engine('sqlite:///app/database/database.db', echo=True)
# Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()

# database connection
database_url = os.environ.get('DATABASE_URL')
if database_url : 
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://","postgresql://", 1)
    engine = create_engine(database_url, echo=True)
else:
    # Fallback to SQLite for local development
    engine = create_engine('sqlite:///app/database/database.db', echo=True)

Base.metadata.create_all(engine)

# The Session should be created inside a request, not globally.
# We'll create a function to get a session.
def get_db_session() -> Session:
    return sessionmaker(bind=engine)()

@app.route("/")
@app.route("/index")
def index():
    return render_template("public/index.html")

# @app.route("/test", methods=["GET", "POST"])
# def langspecify():
#     if request.method == "POST":
#         lang = request.form.get("dropdown")
#         print(str(lang))
#         if str(lang) == "Spanish":
#             return redirect(url_for("spanish"))
#         elif str(lang) == "Hindi":
#             return redirect(url_for("hindi"))
#         elif str(lang) == "French":
#             return redirect(url_for("french"))
#         elif str(lang) == "English":
#             return redirect(url_for("english"))
#         return redirect(request.url)

#     return render_template("public/test.html")


@app.route("/test", methods=["GET", "POST"])
def langspecify() -> str:
    if request.method == "POST":
        lang = request.form.get("dropdown")
        print(str(lang))
        if str(lang) == "Spanish":
            return redirect(url_for("find", lang="spanish"))
        elif str(lang) == "Hindi":
            return redirect(url_for("find", lang="hindi"))
        elif str(lang) == "French":
            return redirect(url_for("find", lang="french"))
        elif str(lang) == "English":
            return redirect(url_for("find", lang="english"))
        return redirect(request.url)  # Or perhaps render_template("public/test.html")

    return render_template("public/test.html")

@app.route("/<lang>", methods=["GET", "POST"])
def find(lang: str) -> str:
    if request.method == "POST":
        em = request.form.get("email")
        file = request.files['file']
        filename = secure_filename(file.filename)  # type: ignore
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        session = get_db_session()
        try:
            det = Details(email=em, vidName=file_path)
            session.add(det)
            session.commit()
            flash("File uploaded and details saved successfully!", "success") # Use flash messages!
        except Exception as e:
            session.rollback()
            flash(f"An error occurred: {e}", "error") # And error messages
            print(f"Error adding to database: {e}") # Log the error, too
            return render_template(f"public/{lang}.html")  # Stay on the same page
        finally:
            session.close()

        try:
           subs = textExtractor(filename)
        except Exception as e:
            flash(f"An error occured during text extraction: {e}", "error")
            return render_template(f"public/{lang}.html")
        
        target_lang_code: str = ""
        if lang == 'spanish':
            target_lang_code = 'es'
        elif lang == 'hindi':
            target_lang_code = 'hi'
        elif lang == 'french':
            target_lang_code = 'fr'
        elif lang == 'english':
            target_lang_code = 'en'
        else:  #Important to handle unexpected input.
             flash("Invalid Language Selection.", "error")
             return render_template("public/test.html")

        try:
            translated_subs = GoogleTranslator(source="auto", target=target_lang_code).translate(subs)
            return render_template(f"public/{lang}.html", subs=translated_subs)
        except Exception as e:
            flash(f"Translation error: {e}", "error")
            return render_template(f"public/{lang}.html", subs=subs) # Show original subs on error

    return render_template(f"public/{lang}.html")




@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')


