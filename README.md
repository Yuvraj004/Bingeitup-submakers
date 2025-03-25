# Subtitle Makers

Subtitle Makers is a project that allows you to extract subtitles from video files and translate them into multiple languages. The project uses Python and JavaScript, integrating various libraries to handle audio extraction, speech recognition, and translation.

## Features

- Convert video files to audio
- Split audio into chunks for processing
- Extract text from audio using speech recognition
- Translate extracted text into multiple languages (English, Spanish, Hindi, French)

## Technologies Used

- Python
- JavaScript
- Flask
- MoviePy
- Pydub
- SpeechRecognition
- Deep Translator
- MongoDB

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Yuvraj004/Bingeitup-submakers.git
    cd subtitle-makers
    ```

2. Set up a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Set up the MongoDB database:
    ```bash
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi
    data_uri = os.environ.get(MONGO_URI)
    client = MongoClient(database_url, server_api=ServerApi('1'))
    ```

## Usage

1. Start the Flask server:
    ```bash
    flask run
    or 
    python main.py
    ```

2. Open your browser and navigate to `http://localhost:5000/`.

3. Upload a video file and select the desired language for the subtitles.

4. The application will process the video, extract the audio, convert the audio to text, and translate the text into the selected language.

## Project Structure

```plaintext
subtitle-makers/
├── app/
│   ├── __init__.py
│   ├── audioTrans.py
│   ├── templates/
│   │   ├── public/
│   │   │   ├── index.html
│   │   │   ├── test.html
│   │   │   ├── spanish.html
│   │   │   ├── hindi.html
│   │   │   ├── french.html
│   │   │   ├── english.html
│   ├── vids/
│   ├── chunks/
│   ├── auds/
│   ├── database/
│   │   ├── database.db
├── requirements.txt
├── README.md
├── main.py
