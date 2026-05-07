# 🎤 VoiceBot – Hindi + Telugu Interactive Voice Assistant

VoiceBot is a simple yet powerful **voice-based chatbot** that allows users to interact using **Hindi and Telugu speech**.  
It converts speech → text → response → speech, creating a complete conversational experience in real time.

---

## 🚀 Live Demo

👉 https://voice-bot-c655.onrender.com  

*(Note: Free hosting may take ~30–50 seconds to wake up)*

---

## ✨ Features

- 🎙️ Voice input using browser Speech Recognition
- 🌐 Supports **Hindi + Telugu + Mixed language**
- 🤖 Rule-based intelligent chatbot responses
- 🔊 Text-to-Speech (TTS) using gTTS
- 💬 Modern chat-style UI
- 📋 Conversation logs (view + clear)
- 🧠 Multi-turn conversation memory
- 🧹 Automatic cleanup of old audio files

---

## 🛠️ Tech Stack

**Frontend**
- HTML5
- CSS3
- JavaScript (Vanilla)

**Backend**
- Python (Flask)

**APIs & Libraries**
- Web Speech API (Speech Recognition)
- gTTS (Google Text-to-Speech)

**Storage**
- JSON + TXT logs

---

## 📁 Project Structure

```bash
voice-bot/
│── app.py
│── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── (generated audio files)
```

---

## ⚙️ Installation & Setup (Local)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Labdhimandovara/Voice-Bot.git
cd Voice-Bot
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the App
```bash
python app.py
```

### 4️⃣ Open in Browser
```
http://localhost:5000
```

---

## 🌍 Deployment (Render)

This project is deployed using **Render (Free Hosting)**.

### Important Fix Required for Deployment

Update your `app.py` like this:

```python
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

### Steps:
1. Push code to GitHub  
2. Go to Render  
3. Create **New Web Service**  
4. Connect your repo  
5. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
6. Deploy 🚀

---

## 🎯 How It Works

1. User clicks 🎤 **Start Listening**
2. Speech → converted to text (Web Speech API)
3. Text sent to Flask backend (`/process`)
4. Bot generates response (rule-based logic)
5. Response → converted to speech (gTTS)
6. Audio + text returned to frontend
7. Bot speaks the response 🔊

---

## ⚠️ Notes

- Best supported in **Google Chrome**
- Microphone permission is required
- Free hosting may be slow (cold start delay)
- Logs are stored locally (JSON + TXT)

---

## 🌟 Future Improvements

- 🤖 Integrate AI (ChatGPT / NLP models)
- 🌍 Add more language support
- 🔐 User authentication system
- ☁️ Better cloud deployment (low latency)
- 📱 Mobile optimization

---

