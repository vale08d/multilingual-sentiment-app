from flask import Flask, request, jsonify
from textblob import TextBlob
from langdetect import detect, LangDetectException

app = Flask(__name__)

# ── Sentiment word lists for Spanish and Italian ───────────────────────────────
# TextBlob is English-trained, so we use lightweight word-score dictionaries

SPANISH_POSITIVE = {
    "bueno", "buena", "excelente", "fantástico", "fantástica", "maravilloso",
    "maravillosa", "increíble", "perfecto", "perfecta", "feliz", "alegre",
    "amor", "amar", "encanta", "encanto", "genial", "estupendo", "estupenda",
    "brillante", "positivo", "positiva", "éxito", "exitoso", "bonito",
    "bonita", "hermoso", "hermosa", "delicioso", "deliciosa", "rico", "rica",
    "bien", "mejor", "fácil", "agradable", "divertido", "divertida",
    "emocionante", "interesante", "útil", "valioso", "valiosa", "gracias"
}

SPANISH_NEGATIVE = {
    "malo", "mala", "terrible", "horrible", "pésimo", "pésima", "triste",
    "odio", "odiar", "aburrido", "aburrida", "frustrante", "frustrado",
    "frustrada", "difícil", "problema", "error", "fallo", "fallido",
    "fallida", "negativo", "negativa", "peor", "desastre", "inútil",
    "molesto", "molesta", "enojado", "enojada", "furioso", "furiosa",
    "decepcionante", "decepcionado", "decepcionada", "doloroso", "dolorosa",
    "daño", "peligroso", "peligrosa", "sucio", "sucia", "feo", "fea"
}

ITALIAN_POSITIVE = {
    "buono", "buona", "ottimo", "ottima", "eccellente", "fantastico",
    "fantastica", "meraviglioso", "meravigliosa", "incredibile", "perfetto",
    "perfetta", "felice", "allegro", "allegra", "amore", "amare", "adoro",
    "adorare", "geniale", "stupendo", "stupenda", "brillante", "positivo",
    "positiva", "successo", "bello", "bella", "delizioso", "deliziosa",
    "buonissimo", "buonissima", "bene", "meglio", "facile", "piacevole",
    "divertente", "emozionante", "interessante", "utile", "prezioso",
    "preziosa", "grazie", "bravo", "brava", "magnifico", "magnifica"
}

ITALIAN_NEGATIVE = {
    "cattivo", "cattiva", "terribile", "orribile", "pessimo", "pessima",
    "triste", "odio", "odiare", "noioso", "noiosa", "frustrante",
    "frustrato", "frustrata", "difficile", "problema", "errore", "brutto",
    "brutta", "negativo", "negativa", "peggio", "disastro", "inutile",
    "fastidioso", "fastidiosa", "arrabbiato", "arrabbiata", "furioso",
    "furiosa", "deludente", "deluso", "delusa", "doloroso", "dolorosa",
    "pericoloso", "pericolosa", "sporco", "sporca", "sbagliato", "sbagliata"
}


def word_based_sentiment(text, positive_set, negative_set):
    """Score sentiment by counting positive vs negative words."""
    words = text.lower().split()
    pos_count = sum(1 for w in words if w.strip(".,!?;:\"'") in positive_set)
    neg_count = sum(1 for w in words if w.strip(".,!?;:\"'") in negative_set)

    total = pos_count + neg_count
    if total == 0:
        return 0.0, "neutral"

    polarity = round((pos_count - neg_count) / total, 3)

    if polarity > 0:
        return polarity, "positive"
    elif polarity < 0:
        return polarity, "negative"
    else:
        return 0.0, "neutral"


def detect_language(text):
    """Detect language and return a human-readable name and code."""
    try:
        code = detect(text)
        language_map = {
            "en": "english",
            "it": "italian",
            "es": "spanish"
        }
        return language_map.get(code, "unsupported"), code
    except LangDetectException:
        return "unknown", "unknown"


def analyze_sentiment(text, lang_code):
    """Route to the correct sentiment analyzer based on language."""
    if lang_code == "en":
        blob = TextBlob(text)
        polarity = round(blob.sentiment.polarity, 3)
        if polarity > 0.1:
            label = "positive"
        elif polarity < -0.1:
            label = "negative"
        else:
            label = "neutral"
        return polarity, label
    elif lang_code == "es":
        return word_based_sentiment(text, SPANISH_POSITIVE, SPANISH_NEGATIVE)
    elif lang_code == "it":
        return word_based_sentiment(text, ITALIAN_POSITIVE, ITALIAN_NEGATIVE)

    return 0.0, "neutral"


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "Multilingual Sentiment Analysis API",
        "author": "Valentina Diana",
        "version": "1.1",
        "supported_languages": ["english", "spanish", "italian"],
        "usage": {
            "endpoint": "/analyze",
            "method": "POST",
            "body": {"text": "Your text here"},
            "examples": [
                {"text": "I love coding, it makes me very happy!"},
                {"text": "Questa pizza è assolutamente deliziosa!"},
                {"text": "Este trabajo es muy aburrido y frustrante."}
            ]
        },
        "github": "https://github.com/vale08d",
        "portfolio": "https://valentinadianaportfolio.netlify.app"
    })


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Field 'text' is required and cannot be empty."}), 400

    if len(text) > 2000:
        return jsonify({"error": "Text must be 2000 characters or fewer."}), 400

    language_name, lang_code = detect_language(text)

    if language_name not in ("english", "italian", "spanish"):
        return jsonify({
            "error": "Unsupported language. This API supports English, Spanish, and Italian.",
            "detected_language_code": lang_code,
            "text": text
        }), 422

    polarity, sentiment_label = analyze_sentiment(text, lang_code)

    return jsonify({
        "text": text,
        "language": language_name,
        "sentiment": sentiment_label,
        "polarity": polarity,
        "note": "Polarity ranges from -1.0 (very negative) to 1.0 (very positive)"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=False)
