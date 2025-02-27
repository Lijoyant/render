from fastapi import FastAPI, UploadFile, File
import requests
import io
import os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

# Load API key from environment variable
AI_API_URL = "https://api-inference.huggingface.co/models/your-model"
HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

@app.get("/")
def home():
    return {"message": "Room Designing AI is running!"}

@app.post("/generate-design/")
async def generate_design(file: UploadFile = File(...)):
    try:
        # Read uploaded image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Send image to external AI API for processing
        response = requests.post(AI_API_URL, headers=HEADERS, files={"file": image_bytes})

        if response.status_code == 200:
            # Return generated image
            return {"message": "Design generated!", "image_url": response.json()}
        else:
            return {"error": "AI generation failed", "details": response.text}

    except Exception as e:
        return {"error": str(e)}

