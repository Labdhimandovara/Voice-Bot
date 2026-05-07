from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os
import glob
import json
import datetime

app = Flask(__name__)
LOG_FILE = "conversation_log.txt"
JSON_LOG_FILE = "conversation_log.json"

# ─────────────────────────────────────────────
#  CONVERSATION MEMORY (multi-turn)
# ─────────────────────────────────────────────
conversation_history = []

# ─────────────────────────────────────────────
#  RULE-BASED REPLY LOGIC (Hindi + Telugu mix)
# ─────────────────────────────────────────────
def bot_reply(user_text):
    text = user_text.lower().strip()

    # Greetings
    if any(w in text for w in ["namaste", "namaskar", "namaskaram", "hello", "hi", "hii", "hey"]):
        return "Namaste ji! Aapko kaise help chahiye? Meeru ela help cheyyagalanu?"

    # Name introduction
    if any(w in text for w in ["peru", "naam", "name", "naa peru", "mera naam", "my name"]):
        # Try to extract name
        words = text.split()
        for kw in ["peru", "naam", "name", "is", "am"]:
            if kw in words:
                idx = words.index(kw)
                if idx + 1 < len(words):
                    name = words[idx + 1].capitalize()
                    return f"Namaste {name} ji! Aapko kaise help chahiye? Meeru ela assist cheyyagalanu?"
        return "Mee peru cheppinanduku dhanyavaadaalu! Meeru ela help cheyyagalanu?"

    # Demo request
    if any(w in text for w in ["demo", "kavali", "chahiye", "show", "software demo"]):
        return "Sure! Meeku oka demo schedule chestanu. Mee convenient time cheppagalara? We will arrange it for you!"

    # Help
    if any(w in text for w in ["help", "sahaya", "sahayam", "madad", "assist"]):
        return "Bilkul! Hum aapki poori madad karenge. Meeru meeku anni vishayaallo help chestamu. Tell me what you need!"

    # How are you
    if any(w in text for w in ["kaise ho", "ela unnaru", "how are you", "kaisa", "kaisay"]):
        return "Main bilkul theek hoon, shukriya! Nenu chala bagunnanu. Aap batao, meeru ela help cheyyagalanu?"

    # Product / service inquiry
    if any(w in text for w in ["product", "service", "kya hai", "entundi", "about", "information", "info"]):
        return "Maa products chala baaguntayi! We offer software solutions, demos, and support. Meeru detailed information share chestamu. Demo book cheyyalante cheppandi!"

    # Price / cost
    if any(w in text for w in ["price", "cost", "charge", "dhara", "fee", "kitna"]):
        return "Pricing maa team tho discuss cheyyadam better avutundi. Oka demo schedule cheste, anni details explain chestamu!"

    # Thank you
    if any(w in text for w in ["thanks", "dhanyavaad", "shukriya", "thank you", "tq"]):
        return "Aapka swagat hai! Meeru eppudu help cheyyaadaniki ready ga unnamu. Inkemi help kavali?"

    # Bye / goodbye
    if any(w in text for w in ["bye", "goodbye", "alvida", "ciao", "ok bye"]):
        return "Dhanyavaadaalu maa tho maatladindi! Have a great day. Meeru eppudu help cheyyaadaniki ready ga unnamu!"

    # Time / date
    if any(w in text for w in ["time", "samayam", "date", "today"]):
        now = datetime.datetime.now()
        return f"Ippudu time {now.strftime('%I:%M %p')}, date {now.strftime('%d %B %Y')} undi."

    # Default fallback
    return "Sare, meeru cheppandi — enduku help kavali? Aap bata sakte hain, hum haazir hain!"


# ─────────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────────
def save_logs(user, bot):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # TXT log
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\nUser: {user}\nBot: {bot}\n\n")

    # JSON log
    entry = {"timestamp": timestamp, "user": user, "bot": bot}
    logs = []
    if os.path.exists(JSON_LOG_FILE):
        with open(JSON_LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    logs.append(entry)
    with open(JSON_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
#  CLEANUP OLD AUDIO FILES
# ─────────────────────────────────────────────
def cleanup_audio():
    files = sorted(glob.glob("static/tts_*.mp3"), key=os.path.getmtime)
    for f in files[:-5]:
        try:
            os.remove(f)
        except:
            pass


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    user_text = data.get("user_text", "").strip()

    if not user_text:
        return jsonify({"error": "No text received"}), 400

    # Multi-turn memory
    conversation_history.append({"role": "user", "content": user_text})
    if len(conversation_history) > 20:
        conversation_history.pop(0)

    bot_response = bot_reply(user_text)

    conversation_history.append({"role": "bot", "content": bot_response})
    save_logs(user_text, bot_response)

    # TTS — use Telugu for Telugu words, Hindi for Hindi
    # Detect language: if text has Telugu keywords, use te; else hi
    te_keywords = ["kavali", "chestanu", "unnaru", "bagunnanu", "meeru", "mee", "ela", "cheppandi"]
    lang = "te" if any(w in bot_response.lower() for w in te_keywords) else "hi"

    filename = f"tts_{datetime.datetime.now().timestamp()}.mp3"
    filepath = os.path.join("static", filename)

    try:
        tts = gTTS(bot_response, lang=lang, slow=False)
        tts.save(filepath)
        cleanup_audio()
        audio_url = f"/static/{filename}"
    except Exception as e:
        print(f"TTS Error: {e}")
        audio_url = None

    return jsonify({
        "bot_text": bot_response,
        "audio_url": audio_url,
        "lang": lang
    })


@app.route("/logs")
def get_logs():
    if os.path.exists(JSON_LOG_FILE):
        with open(JSON_LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
                return jsonify(logs)
            except:
                return jsonify([])
    return jsonify([])


@app.route("/clear_logs", methods=["POST"])
def clear_logs():
    for f in [LOG_FILE, JSON_LOG_FILE]:
        if os.path.exists(f):
            os.remove(f)
    conversation_history.clear()
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    app.run(port=5000, debug=True)
