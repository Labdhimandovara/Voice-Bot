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

    # Greetings — English + Devanagari
    if any(w in text for w in ["namaste", "namaskar", "hello", "hi", "hey",
                                "नमस्ते", "नमस्कार", "हेलो", "हाय"]):
        return "Namaste ji! Aapko kaise help chahiye? Meeru ela help cheyyagalanu?"

    # Name — English + Devanagari
    if any(w in text for w in ["mera naam", "my name", "naa peru", "naam",
                                "मेरा नाम", "नाम", "peru"]):
        words = text.split()
        for kw in ["naam", "name", "peru", "is", "am", "नाम", "हूं", "हूँ"]:
            if kw in words:
                idx = words.index(kw)
                if idx + 1 < len(words):
                    name = words[idx + 1].capitalize()
                    return f"Namaste {name} ji! Bahut achha naam hai. Meeru ela assist cheyyagalanu?"
        return "Mee peru cheppinanduku dhanyavaadaalu! Meeru ela help cheyyagalanu?"

    # Demo
    if any(w in text for w in ["demo", "kavali", "dikhao", "show",
                                "डेमो", "दिखाओ", "चाहिए"]):
        return "Sure! Meeku oka demo schedule chestanu. Mee convenient time cheppagalara?"

    # Help
    if any(w in text for w in ["help", "madad", "sahaya", "problem",
                                "मदद", "सहायता", "हेल्प", "प्रॉब्लम"]):
        return "Bilkul! Hum aapki poori madad karenge. Meeru meeku help chestamu. Kya problem hai?"

    # How are you
    if any(w in text for w in ["kaise ho", "how are you", "ela unnaru",
                                "कैसे हो", "कैसे हैं", "theek ho"]):
        return "Main bilkul theek hoon! Nenu chala bagunnanu. Meeru ela help cheyyagalanu?"

    # Price
    if any(w in text for w in ["price", "cost", "fee", "kitna", "paisa",
                                "कीमत", "पैसा", "चार्ज", "कितना"]):
        return "Pricing ke liye maa team se baat karein. Demo schedule cheste sab details milenge!"

    # Thanks
    if any(w in text for w in ["thanks", "thank you", "shukriya", "dhanyavaad",
                                "धन्यवाद", "शुक्रिया", "bahut achha", "बहुत अच्छा"]):
        return "Aapka swagat hai! Meeru eppudu ready ga untamu. Inkemi kavali?"

    # Bye
    if any(w in text for w in ["bye", "goodbye", "alvida", "baad mein",
                                "अलविदा", "बाय", "फिर मिलेंगे"]):
        return "Dhanyavaadaalu! Have a great day. Meeru eppudu ready ga untamu!"

    # Time/date
    if any(w in text for w in ["time", "date", "today", "samayam",
                                "टाइम", "समय", "तारीख", "आज"]):
        now = datetime.datetime.now()
        return f"Ippudu time {now.strftime('%I:%M %p')}, date {now.strftime('%d %B %Y')} undi."

    # Appointment
    if any(w in text for w in ["appointment", "book", "meeting", "schedule", "milna",
                                "अपॉइंटमेंट", "मीटिंग", "बुक"]):
        return "Zaroor! Mee appointment book chestamu. Mee preferred date and time cheppandi!"

    # Fallback — rotates
    fallbacks = [
        "Sare, meeru cheppandi — enduku help kavali? Hum haazir hain!",
        "Kya aap thoda aur detail mein bata sakte hain? Meeru better help cheyyagalamu!",
        "Samajh nahi aaya. Demo kavali? Ya kuch aur poochna hai?",
        "Aapka sawaal clearly nahi aaya. Dobara bol sakte hain?"
    ]
    return fallbacks[len(conversation_history) % len(fallbacks)]
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
