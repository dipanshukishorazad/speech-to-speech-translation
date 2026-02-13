from flask import Flask, render_template, request
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from pathlib import Path

app = Flask(__name__)

def listen_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ बोलिए...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='hi-IN')
        print("📝 आपने कहा:", text)
        return text
    except sr.UnknownValueError:
        print("❌ आवाज़ समझ नहीं आई")
        return ""
    except sr.RequestError as e:
        print(f"⚠️ Error: {e}")
        return ""

def translate_text(text, target_lang="en"):
    translator = Translator()
    result = translator.translate(text, dest=target_lang)
    print(f"🌐 अनुवाद ({target_lang}):", result.text)
    return result.text

def speak_text(text, lang="en"):
    Path("static").mkdir(exist_ok=True)
    filename = "static/output.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return filename

@app.route("/", methods=["GET", "POST"])
def index():
    original = ""
    translated = ""
    audio_file = ""

    if request.method == "POST":
        original = listen_microphone()
        if original:
            translated = translate_text(original)
            audio_file = speak_text(translated)

    #return render_template("index.html", original=original, translated=translated, audio_file=audio_file)
    return render_template("index.html", original=original, translated=translated, audio_file=audio_file, is_listening=True if request.method == "POST" else False)


if __name__ == "__main__":
    app.run(debug=True)
