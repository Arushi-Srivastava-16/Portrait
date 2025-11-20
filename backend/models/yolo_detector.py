from ultralytics import YOLO
import numpy as np
import torch
import os

# Fix for PyTorch 2.6+ security: monkey-patch torch.load before importing YOLO
_original_torch_load = torch.load

def _patched_torch_load(*args, **kwargs):
    """Patched torch.load that allows loading YOLO models"""
    # Set weights_only=False for YOLO model files
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)

# Apply the patch
torch.load = _patched_torch_load

# Also add safe globals for common PyTorch classes
try:
    import torch.nn.modules.container
    torch.serialization.add_safe_globals([
        torch.nn.modules.container.Sequential,
    ])
    # Try to add ultralytics classes if available
    try:
        import ultralytics.nn.tasks
        torch.serialization.add_safe_globals([
            ultralytics.nn.tasks.DetectionModel,
        ])
    except:
        pass
except Exception as e:
    pass

class YOLODetector:
    def __init__(self, model_path):
        # Load model - if local file fails, YOLO will download it
        try:
            self.model = YOLO(model_path)
        except Exception as e:
            # If loading fails, try with default model name (will download)
            print(f"Warning: Could not load {model_path}, using default yolov8n.pt")
            try:
                self.model = YOLO("yolov8n.pt")
            except Exception as e2:
                # Last resort: try downloading fresh model
                print(f"Error loading model: {e2}")
                raise
        # Map COCO class names to our magical object names
        # COCO classes: book=73, cell phone=77, glasses/sunglasses not in COCO, 
        # wand not in COCO, pet could be cat=15 or dog=16
        self.coco_to_magical = {
            'book': 'book',
            'cell phone': 'phone',
            'laptop': 'phone',  # Sometimes phones detected as laptops
            'cat': 'pet',
            'dog': 'pet',
            'bird': 'pet',
            # For glasses, we'll look for 'handbag' or other items that might be detected
            # Note: COCO doesn't have glasses, so we'll accept any object for now
        }
        # Our target magical objects
        self.magical_objects = ['book', 'glasses', 'wand', 'phone', 'pet']
        
    def detect(self, image):
        """
        Run YOLO detection on image using pre-trained COCO model
        Returns: dict with objects, confidences, boxes
        """
        results = self.model(image)[0]
        
        detected_objects = []
        confidences = []
        boxes = []
        
        for box in results.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            
            if confidence > 0.5:  # Threshold
                # Get COCO class name
                coco_class_name = results.names[class_id].lower()
                
                # Map to magical object if possible
                magical_object = None
                if coco_class_name in self.coco_to_magical:
                    magical_object = self.coco_to_magical[coco_class_name]
                elif coco_class_name in self.magical_objects:
                    magical_object = coco_class_name
                else:
                    # Accept any detected object as a potential magical object
                    magical_object = coco_class_name  # Use COCO name as fallback
                
                if magical_object:
                    detected_objects.append(magical_object)
                    confidences.append(confidence)
                    boxes.append(box.xyxy[0].tolist())
        
        return {
            "objects": detected_objects,
            "confidences": confidences,
            "boxes": boxes
        }

