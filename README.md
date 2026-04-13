# BookWorm — AI Audio & Document Analyzer

A Flask web app that processes audio recordings and PDF documents using Gemini AI. Upload a WAV file to get a transcription and sentiment analysis, or upload a PDF to extract insights — with text-to-speech playback of AI responses.

---

## What it does

BookWorm accepts two types of input:

**Audio (WAV)**
- Transcribes speech using Gemini's multimodal API
- Analyzes sentiment (Positive / Negative / Neutral)
- Synthesizes the response as audio using Google Text-to-Speech

**Documents (PDF)**
- Extracts and analyzes content using Gemini
- Returns key insights or answers to your prompts
- TTS playback for hands-free review

---

## Architecture

```
Browser → Flask (main.py)
              ├── .wav  → Gemini multimodal → transcription + sentiment
              │                                    ↓
              │                             Google TTS → .wav response
              └── .pdf  → Gemini → document analysis
                               ↓
                          uploads/  ← files stored locally
```

---

## Setup

### Prerequisites

- Python 3.10+
- Google AI Studio API key (Gemini access)
- Google Cloud project with Text-to-Speech API enabled
- Service account JSON with TTS permissions

### Install

```bash
git clone https://github.com/Prabhuteja799/BookWorm.git
cd BookWorm
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Configure

```bash
export GEMINI_API_KEY=your_gemini_key
export GOOGLE_APPLICATION_CREDENTIALS=path/to/service_account.json
```

### Run

```bash
python main.py
# → http://localhost:5000
```

---

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Flask (Python) |
| AI / Transcription | Google Gemini (`gemini-2.0-flash`) multimodal |
| Text-to-Speech | Google Cloud TTS (`en-US-Standard-C`) |
| File handling | Local filesystem, WAV + PDF |
| Frontend | Jinja2 templates |
| Deployment | Procfile (Heroku/Render compatible) |

---

## Future improvements

- Chunked processing for long audio files
- PDF page-range selection
- Persistent history with search
- Support for more languages via TTS voice configuration
