from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from gtts import gTTS
import io
import os

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    voice: dict = None

@router.post("/speak")
async def text_to_speech(request: TTSRequest):
    """
    Converts text to speech with voice parameters
    """
    try:
        # Use gTTS for text-to-speech
        # Note: gTTS doesn't support pitch/speed directly, but we can use pyttsx3 as fallback
        tts = gTTS(text=request.text, lang='en', slow=False)
        
        # Create in-memory audio file
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=speech.mp3"}
        )
    except Exception as e:
        # Fallback to pyttsx3 if gTTS fails
        import pyttsx3
        engine = pyttsx3.init()
        
        if request.voice:
            if "pitch" in request.voice:
                engine.setProperty('rate', int(150 * (request.voice.get("speed", 1.0))))
            if "speed" in request.voice:
                engine.setProperty('rate', int(150 * request.voice["speed"]))
        
        # Save to temporary file
        temp_file = "/tmp/speech.wav"
        engine.save_to_file(request.text, temp_file)
        engine.runAndWait()
        
        with open(temp_file, "rb") as f:
            audio_data = f.read()
        
        os.remove(temp_file)
        
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=speech.wav"}
        )

