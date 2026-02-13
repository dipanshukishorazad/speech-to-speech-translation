import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import playsound

def listen_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ बोलिए...")
        audio = recognizer.listen(source , phrase_time_limit=10)

    try:
        text = recognizer.recognize_google(audio, language='hi-IN')  # हिन्दी से इनपुट
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
    tts = gTTS(text=text, lang=lang)
    filename = "output.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

if __name__ == "__main__":
    while True:
        print("\n🎬 नया अनुवाद:")
        input_text = listen_microphone()
        if input_text:
            translated = translate_text(input_text, target_lang='en')  # हिन्दी → अंग्रेज़ी
            speak_text(translated, lang='en')
