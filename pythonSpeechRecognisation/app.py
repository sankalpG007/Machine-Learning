from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize_speech():
    lang_code = request.json.get('language', 'en-IN')
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language=lang_code)
            return jsonify({'result': text})
        except sr.UnknownValueError:
            return jsonify({'result': "❌ Could not understand audio"})
        except sr.RequestError:
            return jsonify({'result': "⚠️ Error connecting to recognition service"})

if __name__ == '__main__':
    app.run(debug=True)
