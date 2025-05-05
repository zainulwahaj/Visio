import os
from dotenv import load_dotenv

load_dotenv()  # if you ever add .env later

# Where to save uploads
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
