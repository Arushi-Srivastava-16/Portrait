from fastapi import APIRouter
from pydantic import BaseModel
import sys
import os
# Add backend directory to path for imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
from models.conversation_engine import ConversationEngine

router = APIRouter()

# Initialize conversation engine
portraits_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "portraits.json")
conversation_engine = ConversationEngine(portraits_path=portraits_path)

class ChatRequest(BaseModel):
    detected_object: str
    visitor_name: str = "stranger"

@router.post("/chat")
async def generate_conversation(request: ChatRequest):
    """
    Generates multi-turn conversation between portraits
    """
    conversation = conversation_engine.generate_dialogue(
        trigger_object=request.detected_object,
        visitor_name=request.visitor_name
    )
    
    return {
        "turns": conversation,  # List of {portrait, text, voice_params}
        "total_turns": len(conversation)
    }

