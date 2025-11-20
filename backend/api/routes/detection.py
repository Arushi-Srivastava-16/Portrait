from fastapi import APIRouter, File, UploadFile
import sys
import os
# Add backend directory to path for imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
from models.yolo_detector import YOLODetector
import numpy as np
from PIL import Image
import io
import os

router = APIRouter()

# Lazy-load detector to avoid import-time issues
detector = None

def get_detector():
    global detector
    if detector is None:
        # Initialize detector with pre-trained yolov8n.pt from main Wall folder
        # Get the path to the main Wall directory (two levels up from backend/api/routes)
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        wall_dir = os.path.dirname(backend_dir)  # Go up one more level to Wall folder
        model_path = os.path.join(wall_dir, "yolov8n.pt")
        
        # Fallback to default if file doesn't exist (ultralytics will download it)
        if not os.path.exists(model_path):
            model_path = "yolov8n.pt"
        
        detector = YOLODetector(model_path=model_path)
    return detector

@router.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    """
    Receives image from camera, returns detected objects
    """
    try:
        print(f"📸 Received image from: {file.filename}")
        # Read image
        contents = await file.read()
        print(f"📦 Image size: {len(contents)} bytes")
        image = Image.open(io.BytesIO(contents))
        print(f"🖼️ Image dimensions: {image.size}")
        
        # Run detection
        detector_instance = get_detector()
        results = detector_instance.detect(image)
        
        print(f"📤 Returning {len(results['objects'])} objects: {results['objects']}")
        
        return {
            "objects": results["objects"],  # ["book", "glasses"]
            "confidences": results["confidences"],
            "boxes": results["boxes"]
        }
    except Exception as e:
        print(f"❌ Error in detection endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise

