# Multilingual Sentiment Analysis API

> A REST API that detects language and analyzes sentiment in **English, Spanish, and Italian** — built with Flask and deployed on PythonAnywhere.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Deployed](https://img.shields.io/badge/Live-vale08.pythonanywhere.com-brightgreen?style=flat)
![Languages](https://img.shields.io/badge/Languages-EN%20%7C%20ES%20%7C%20IT-blue?style=flat)

---

## Live API

**Base URL:** `https://vale08.pythonanywhere.com`

Try it right now:
```bash
curl -X POST https://vale08.pythonanywhere.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Questa pizza è assolutamente deliziosa!"}'
```

---

## What This Does:

Accepts a text string via POST request, automatically detects whether it's English, Spanish, or Italian, runs sentiment analysis, and returns a structured JSON response with:

- Detected **language**
- Sentiment **label** (positive / negative / neutral)
- **Polarity score** from -1.0 (very negative) to 1.0 (very positive)

---

## Tech Stack:

| Tool | Purpose |
|------|---------|
| Python 3.10 | Core language |
| Flask | REST API framework |
| TextBlob | English sentiment analysis |
| langdetect | Language detection (supports 50+ languages) |
| Custom word lists | Spanish & Italian sentiment scoring |
| PythonAnywhere | Free cloud deployment |

---

## API Endpoints:

### `GET /`
Returns API info and usage instructions.

**Response:**
```json
{
  "name": "Multilingual Sentiment Analysis API",
  "author": "Valentina Diana",
  "version": "1.1",
  "supported_languages": ["english", "spanish", "italian"]
}
```

---

### `POST /analyze`
Analyzes the sentiment of the provided text.

**Request body:**
```json
{ "text": "Your text here" }
```

**Response:**
```json
{
  "text": "I love coding, it makes me very happy!",
  "language": "english",
  "sentiment": "positive",
  "polarity": 0.75,
  "note": "Polarity ranges from -1.0 (very negative) to 1.0 (very positive)"
}
```

**Error responses:**
- `400` — missing or invalid JSON body
- `422` — unsupported language detected

---

### `GET /health`
Health check endpoint.

```json
{ "status": "ok" }
```

---

## Example Responses:

**English — Positive**
```bash
curl -X POST https://vale08.pythonanywhere.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love coding, it makes me very happy!"}'

# → { "language": "english", "sentiment": "positive", "polarity": 0.75 }
```

**Italian — Positive**
```bash
curl -X POST https://vale08.pythonanywhere.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Questa pizza è assolutamente deliziosa!"}'

# → { "language": "italian", "sentiment": "positive", "polarity": 1.0 }
```

**Spanish — Negative**
```bash
curl -X POST https://vale08.pythonanywhere.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Este trabajo es muy aburrido y frustrante."}'

# → { "language": "spanish", "sentiment": "negative", "polarity": -1.0 }
```

---

## Run Locally:

```bash
# Clone the repo
git clone https://github.com/vale08d/multilingual-sentiment-api.git
cd multilingual-sentiment-api

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The API will be available at `http://localhost:5000`.

---

## Design Decisions

**Why custom word lists for Spanish and Italian?**
TextBlob's sentiment analyzer was trained on English text. Applying it directly to Spanish or Italian returns 0.0 polarity for almost all input, the model simply has no signal. Rather than adding a heavy multilingual NLP library (which would exceed free hosting memory limits), I built lightweight positive/negative word dictionaries for each language.

**Why langdetect?**
It supports 50+ languages and is lightweight. For this use case, distinguishing between three languages and rejecting others, it's accurate and fast.
