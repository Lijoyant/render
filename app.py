from fastapi import FastAPI, UploadFile, File
import requests
import io
import os
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Check if the variable is loaded
print("GOOGLE_APPLICATION_CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# Now load credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))



load_dotenv()  # Load environment variables from .env file

app = FastAPI()

# Load API key from environment variable
AI_API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

@app.get("/")
def home():
    return {"message": "Room Designing AI is running!"}

@app.post("/generate-design/")
async def generate_design(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        response = requests.post(AI_API_URL, headers=HEADERS, files={"image": image_bytes})

        if response.status_code == 200:
            # Save AI-generated image
            output_path = "generated_design.png"
            generated_image = Image.open(io.BytesIO(response.content))
            generated_image.save(output_path)

            # Upload to Google Drive
            drive_url = upload_to_drive(output_path)

            return {"message": "Design generated!", "image_url": drive_url}
        else:
            return {"error": "AI generation failed", "details": response.text}

    except Exception as e:
        return {"error": str(e)}

def upload_to_drive(image_path):
    """Uploads an image to Google Drive and returns the file URL."""
    file_metadata = {"name": os.path.basename(image_path), "mimeType": "image/png"}
    media = MediaFileUpload(image_path, mimetype="image/png")
    
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    
    return f"https://drive.google.com/uc?id={file.get('id')}"

