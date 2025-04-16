from flask import Flask, render_template, request, redirect, send_file, send_from_directory, flash, session
from datetime import datetime
import os
import google.generativeai as genai
from google.cloud import texttospeech

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Flask
app = Flask(__name__)
app.secret_key = 'your-secret-key'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allow .wav and .pdf files

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_files():
    return sorted([f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)], reverse=True)

# Initialize TTS Client
tts_client = texttospeech.TextToSpeechClient()

def synthesize_answer(text, out_path):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Standard-C")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    with open(out_path, 'wb') as out:
        out.write(response.audio_content)

# Analyze using Gemini API (transcribe + answer based on PDF)
def analyze_audio_llm(pdf_path, audio_path):
    model = genai.GenerativeModel("models/gemini-2.5-pro-preview-03-25")

    pdf_file = genai.upload_file(pdf_path)
    audio_file = genai.upload_file(audio_path)
    prompt = """
        You are an intelligent assistant. A user has uploaded a book as a PDF and asked a question using an audio recording.
        Please answer the user's question based solely on the PDF content.
        Make your response concise, clear, and easy to read aloud. Avoid complex formatting, symbols, or lists. 
        Use full sentences and conversational language.
        Your answer should sound natural when spoken by a text-to-speech system.
        """


    contents = [
        prompt,
        pdf_file,
        audio_file
    ]
    response = model.generate_content(contents)
    return response.text

# Routes
@app.route('/')
def index():
    answer = session.pop('last_answer', None)
    audio_file = session.pop('last_audio', None)
    pdf_name = session.get('pdf_name') 
    return render_template('index.html', answer=answer, audio_file=audio_file, pdf_name=pdf_name)

@app.route('/ask', methods=['POST'])
def ask():
    audio = request.files.get('audio_data')
    pdf = request.files.get('pdf_file')

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    audio_filename = f"{timestamp}.wav"
    response_audio_filename = f"{timestamp}_response.wav"
    audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
    response_audio_path = os.path.join(UPLOAD_FOLDER, response_audio_filename)

    audio.save(audio_path)

    if pdf:
        pdf_filename = f"{timestamp}.pdf"
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
        pdf.save(pdf_path)
        session['pdf_path'] = pdf_path
        session['pdf_name'] = pdf.filename  

    else:
        pdf_path = session.get('pdf_path')

    if not pdf_path:
        flash("No PDF uploaded yet.")
        return redirect('/')

    llm_answer = analyze_audio_llm(pdf_path, audio_path)
    synthesize_answer(llm_answer, response_audio_path)

    session['last_answer'] = llm_answer
    session['last_audio'] = response_audio_filename
    return redirect('/')

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
