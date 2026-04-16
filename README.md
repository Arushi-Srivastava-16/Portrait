<div align="center">

# 🖼️ Wall of Whispering Frames

**An AI-powered interactive portrait gallery that sees what your camera sees — and responds.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange?style=flat-square)](https://ultralytics.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=flat-square&logo=openai)](https://openai.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18%2B-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[**Demo**](#-quick-start) · [**Architecture**](#%EF%B8%8F-architecture) · [**Features**](#-features) · [**Installation**](#-installation)

</div>

---

## 🧠 What is this?

**Wall of Whispering Frames** is a computer vision + generative AI installation. Point your camera at any everyday object — a book, a key, a flower — and five AI-powered oil portraits come to life, each reacting in character. A Victorian noblewoman might speculate on what the object reveals about your personality. A Renaissance merchant might assess its trade value.

> **Core insight:** Every object tells a story. These portraits are the narrators.

### How it works

1. Your camera feed is streamed to the backend
2. **YOLOv8** detects objects in real time (80-class COCO model, <50ms inference)
3. The detected object + each portrait's personality prompt is sent to **OpenAI GPT-4**
4. GPT-4 generates a 4-turn dialogue in the portrait's voice
5. **Text-to-Speech** gives each portrait a distinct voice
6. The **React** gallery renders the live conversation alongside the portrait

---

## ✨ Features

| Feature | Detail |
|---|---|
| 🎯 **Real-Time Object Detection** | YOLOv8n — 80-class COCO, ~50ms per frame |
| 🤖 **GPT-4 Conversations** | Each portrait has a unique system prompt defining personality, era, speech patterns |
| 🗣️ **Multi-Voice TTS** | Each portrait speaks in a distinct browser voice |
| 🎭 **5 Unique Portraits** | Victorian noblewoman, Renaissance merchant, Eastern philosopher, Modern artist, Ancient warrior |
| 🔄 **4-Turn Dialogues** | Portraits engage across multiple rounds, never repeating |
| 🔌 **Template Fallback** | Works without an OpenAI API key — falls back to pre-written responses |
| 🐳 **Docker-Ready** | One-command startup with Docker Compose |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     React Frontend                       │
│         Camera Feed · Portrait Gallery · Chat Log        │
└────────────────────────┬────────────────────────────────┘
                         │ REST API (polling / fetch)
┌────────────────────────┴────────────────────────────────┐
│                   FastAPI Backend                        │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Detection   │  │ Conversation │  │     TTS       │  │
│  │  YOLOv8n    │  │  Engine      │  │   Engine      │  │
│  │  (CV model) │  │  GPT-4 API   │  │  (browser)    │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Request Flow

```
Camera Frame (JPEG)
      │
      ▼
POST /api/detect   →   YOLOv8 inference   →   [ {label, confidence} ]
                                                       │
      ┌────────────────────────────────────────────────┘
      │  detected_object + portrait_personality
      ▼
POST /api/chat   →   GPT-4 API   →   In-character dialogue (4 turns)
      │
      ▼
POST /api/speak  →   TTS response  →  Audio playback in browser
```

---

## 📊 Model Details

| Component | Model | Notes |
|---|---|---|
| Object Detection | `YOLOv8n` (Ultralytics) | COCO 80-class, ~6MB, CPU-friendly |
| Conversation | `gpt-4` via OpenAI API | System prompt per portrait, 4-turn context |
| Text-to-Speech | Browser Web Speech API | Per-portrait `SpeechSynthesisUtterance` config |

---

## 📂 Project Structure

```
Wall-of-Whispering-Frames/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI app + CORS
│   │   └── routes/
│   │       ├── detection.py     # POST /api/detect — YOLOv8 inference
│   │       ├── conversation.py  # POST /api/chat — GPT-4 dialogue
│   │       └── tts.py           # POST /api/speak — TTS config
│   ├── models/
│   │   ├── yolo_detector.py     # YOLOv8 wrapper, confidence threshold
│   │   └── conversation_engine.py  # Portrait persona prompts + GPT-4 calls
│   ├── data/
│   │   └── portraits.json       # Portrait metadata (name, era, personality, voice)
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.jsx              # Root — camera + gallery layout
│       └── components/
│           ├── CameraFeed.jsx   # getUserMedia + frame capture + POST /detect
│           ├── PortraitGallery.jsx  # Grid of 5 portrait cards
│           ├── Portrait.jsx     # Individual portrait + conversation display
│           └── ConversationLog.jsx  # Scrollable dialogue history
├── training/
│   └── Part1_Train_Detector.ipynb  # Optional: fine-tune YOLO on custom objects
└── docker-compose.yml
```

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10+ |
| Node.js | 18+ |
| OpenAI API Key | Optional (falls back to templates) |

### Option A — Docker (Recommended)

```bash
git clone https://github.com/Arushi-Srivastava-16/Portrait.git
cd Portrait
cp .env.example .env
# Add OPENAI_API_KEY=sk-... to .env (optional)
docker-compose up
```

Visit [http://localhost:3000](http://localhost:3000)

### Option B — Manual

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm start
```

---

## ⚙️ Configuration

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Optional | GPT-4 dialogue generation. Falls back to templates if not set. |

To add or modify portraits, edit `backend/data/portraits.json`:

```json
{
  "id": "6",
  "name": "The Alchemist",
  "era": "17th Century",
  "personality": "curious, cryptic, obsessed with transformation",
  "voice": { "pitch": 0.9, "rate": 0.85 }
}
```

---

## 🔌 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/detect` | POST | Send JPEG frame, receive detected objects `[{label, confidence}]` |
| `/api/chat` | POST | Send detected object + portrait ID, receive GPT-4 dialogue |
| `/api/speak` | POST | Send text, receive TTS voice configuration |
| `/` | GET | Health check |

---

## 🔬 Tech Stack

| Layer | Technology |
|---|---|
| **Object Detection** | Ultralytics YOLOv8n (`yolov8n.pt`) |
| **Conversation AI** | OpenAI GPT-4 API |
| **Backend** | FastAPI + Uvicorn |
| **Frontend** | React 18 |
| **TTS** | Web Speech API (browser-native) |
| **Containerization** | Docker + Docker Compose |

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| Camera not showing | Ensure you're on `localhost` or HTTPS (browser requires it for `getUserMedia`) |
| No objects detected | Lower the confidence threshold in `yolo_detector.py` (try `0.3`) |
| TTS not playing | Grant audio permissions in browser; check console for errors |
| Slow detection | Increase capture interval in `CameraFeed.jsx` (try `3000ms`) |

---

## 📄 License

MIT License — feel free to fork and bring your own portraits to life.

---

<div align="center">
  <sub>Built with YOLOv8 · OpenAI GPT-4 · FastAPI · React</sub>
</div>
