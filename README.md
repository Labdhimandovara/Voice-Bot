# 🎤 VoiceBot – Hindi + Telugu Interactive Assistant

A simple and interactive **voice-based chatbot** built using **Flask, HTML, CSS, and JavaScript**.
This bot supports **Hindi + Telugu speech interaction**, responds intelligently, and even **speaks back using Text-to-Speech (TTS)**.

---

## 🚀 Features

* 🎙️ Voice input using browser Speech Recognition
* 🗣️ Multilingual support (Hindi + Telugu + Mixed)
* 🤖 Rule-based intelligent responses
* 🔊 Text-to-Speech (TTS) using gTTS
* 💬 Chat UI with real-time interaction
* 📋 Conversation logs (view + clear)
* 🧠 Multi-turn conversation memory
* 🧹 Auto cleanup of old audio files

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python (Flask)
* **Speech Recognition:** Web Speech API
* **Text-to-Speech:** gTTS
* **Storage:** JSON + TXT logs

---

## 📁 Project Structure

```
voice-bot/
│── app.py
│── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/Labdhimandovara/Voice-Bot.git
cd Voice-Bot
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Run the application

```
python app.py
```

### 4️⃣ Open in browser

```
http://localhost:5000
```

---

## 🎯 How it Works

1. User clicks 🎤 **Start Listening**
2. Speech is converted to text using browser API
3. Text is sent to Flask backend (`/process`)
4. Bot generates a response (rule-based logic)
5. Response is converted to speech (gTTS)
6. Audio + text is sent back and played

---

## 📸 UI Preview

* Clean chat interface
* Voice interaction controls
* Conversation logs viewer

---

## ⚠️ Notes

* Works best on **Google Chrome** (Speech Recognition support)
* Avoid uploading sensitive user data in logs
* `.gitignore` is used to ignore audio + log files

---

## 🌟 Future Improvements

* Add AI/ML-based NLP responses
* Support more languages
* Deploy on cloud (Render / Railway)
* Add user authentication

