from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
from tempfile import NamedTemporaryFile
from typing import Dict

app = FastAPI()

# Allow any origin for API (so Flutter/web/mobile can call it):
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/verify-face/")
async def verify_face(img1: UploadFile = File(...), img2: UploadFile = File(...)) -> Dict:
    try:
        with NamedTemporaryFile(delete=False, suffix=".jpg") as f1, NamedTemporaryFile(delete=False, suffix=".jpg") as f2:
            # Save both uploaded images to temp .jpg files
            f1.write(await img1.read())
            f2.write(await img2.read())
            f1.close(); f2.close()
            result = DeepFace.verify(f1.name, f2.name, enforce_detection=True, model_name='VGG-Face')
            # DeepFace standard: distance <0.4 = strong match, 'verified'=True/False
            return {
                "match": bool(result["verified"]),
                "confidence": float(1.0 - result["distance"]),  # Higher = more confidence
                "message": "Matched" if result["verified"] else "Not matched"
            }
    except Exception as e:
        return {"match": False, "message": str(e)}

@app.get("/")
async def root():
    return {"status": "Face API working!"}