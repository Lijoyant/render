from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Load AI model in CPU mode
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
pipe.to("cpu")  # Ensure it runs on CPU

def upload_to_drive(image_path):
    """Uploads the generated image to Google Drive."""
    credentials, _ = google.auth.default()
    service = build("drive", "v3", credentials=credentials)

    file_metadata = {"name": "output.png", "mimeType": "image/png"}
    media = MediaIoBaseUpload(io.BytesIO(open(image_path, "rb").read()), mimetype="image/png")
    
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return f"https://drive.google.com/uc?id={file.get('id')}"

def generate_design():
    """Generates an AI-based house design."""
    result = pipe("Modern house exterior, high resolution").images[0]
    
    output_path = "output.png"
    result.save(output_path)
    
    # Upload image to Google Drive
    drive_url = upload_to_drive(output_path)
    
    return {"status": "completed", "image_url": drive_url}
