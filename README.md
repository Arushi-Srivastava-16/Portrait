# 🪄 Magical Portraits

An interactive AI-powered portrait gallery that responds to objects detected by your camera. Portraits come to life and have conversations when they see magical objects!

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (optional)

### Installation

1. **Clone or navigate to the project directory**
```bash
cd /Users/arushisrivastava/Desktop/Wall
```

2. **Setup Backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Setup Frontend**
```bash
cd ../frontend
npm install
```

4. **Train Model (Optional)**
   - Open `training/Part1_Train_Detector.ipynb` in Google Colab or Jupyter
   - Follow the cells to train your YOLO model
   - Download `trained_model.pt` to `backend/data/`

5. **Run the Application**

**Option A: Using Docker**
```bash
docker-compose up
```

**Option B: Manual**
```bash
# Terminal 1 - Backend
cd backend
uvicorn api.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

6. **Visit http://localhost:3000**

## 📁 Project Structure

```
Wall/
├── backend/
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   │       ├── detection.py
│   │       ├── conversation.py
│   │       └── tts.py
│   ├── models/
│   │   ├── yolo_detector.py
│   │   └── conversation_engine.py
│   ├── data/
│   │   ├── portraits.json
│   │   └── trained_model.pt (after training)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── CameraFeed.jsx
│   │       ├── PortraitGallery.jsx
│   │       ├── Portrait.jsx
│   │       └── ConversationLog.jsx
│   └── package.json
├── training/
│   └── Part1_Train_Detector.ipynb
└── docker-compose.yml
```

## 🎯 Features

- **Real-time Object Detection**: Uses YOLOv8 to detect objects from camera feed
- **Interactive Portraits**: 5 unique portraits with distinct personalities
- **Multi-turn Conversations**: Portraits engage in 4-turn dialogues about detected objects
- **Text-to-Speech**: Each portrait has a unique voice
- **Beautiful UI**: Modern, magical-themed interface

## 🛠️ Development

### Backend API Endpoints

- `GET /` - Health check
- `POST /api/detect` - Detect objects in uploaded image
- `POST /api/chat` - Generate conversation about detected object
- `POST /api/speak` - Convert text to speech

### Adding New Portraits

Edit `backend/data/portraits.json` to add new portraits with their personalities and voice parameters.

## 📚 Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

## 🆘 Troubleshooting

**Camera not working**: Ensure you're using HTTPS or localhost (browser security requirements)

**Model not detecting**: Lower confidence threshold in `backend/models/yolo_detector.py` (try 0.3)

**TTS not playing**: Check browser console, ensure audio permissions are granted

**Slow detection**: Increase detection interval in `CameraFeed.jsx` (try 3-5 seconds)

## 📝 License

MIT License - Feel free to use and modify!

---

**Ready to bring portraits to life? Start the app and show them an object! 🪄✨**

