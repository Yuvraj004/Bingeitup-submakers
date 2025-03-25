import os
import sys
import pymongo

from app import app
from app.audioTrans import textExtractor
from deep_translator import GoogleTranslator

from app import app
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for,flash, send_from_directory
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# app configurations
app.config['UPLOAD_FOLDER'] = "app/vids/"
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')



# database connection
database_url = os.environ.get('DATABASE_URL')

if(database_url ==""):
    print("database cant be reached")
    sys.exit(1)

try:
# Create a new client and connect to the server
    client = MongoClient(database_url, server_api=ServerApi('1'))
    
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)
    
# use a database named "SubtitlesDB"
db = client.SubtitlesDB

# use a collection named "details"
my_collection = db["details"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


#class details
class Details:
    def __init__(self,vidName:str,email:str="default@gmail.com"):
        self.email=email
        self.vidName=vidName
        
    def to_dict(self):
        return {
            "email":self.email,
            "vidName":self.vidName
        }


#flask Routes

@app.route("/")
@app.route("/index")
def index():
    return render_template("public/index.html")


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

        try:
            videoDetails = Details(email=em, vidName=file_path)
            my_collection.insert_one(videoDetails.to_dict())
            flash("File uploaded and details saved successfully!", "success") # Use flash messages!
        except Exception as e :
            
            flash(f"An error occurred: {e}", "error") # And error messages
            print(f"Error adding to database: {e}") # Log the error, too
            return render_template(f"public/{lang}.html")  # Stay on the same page


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


