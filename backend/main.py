from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil, os

from config import UPLOAD_DIR
from file_index import add_file, get_file, list_files
from file_index import FileInfo

app = FastAPI(title="VisioBrain (No-DB) Backend")

@app.post("/upload/", response_model=FileInfo)
async def upload_file(file: UploadFile = File(...)):
    # only allow PDF/DOCX
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only .pdf or .docx allowed")
    # save to disk
    dest_name = f"{file.filename}"
    dest_path = os.path.join(UPLOAD_DIR, dest_name)
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # add to in-memory index
    info = add_file(filename=file.filename, filepath=dest_path, content_type=file.content_type)
    return info

@app.get("/files/", response_model=list[FileInfo])
def files_list():
    return list_files()

@app.get("/files/{file_id}", response_model=FileInfo)
def file_detail(file_id: str):
    info = get_file(file_id)
    if not info:
        raise HTTPException(status_code=404, detail="File not found")
    return info

@app.get("/download/{file_id}")
def download_file(file_id: str):
    info = get_file(file_id)
    if not info:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=info.filepath, filename=info.filename)

@app.post("/process/{file_id}")
def process_file(file_id: str):
    """
    Stub for later:
      - read text from info.filepath
      - call summarizer & diagram generator
    """
    info = get_file(file_id)
    if not info:
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": f"Processing would run on `{info.filename}` here."}

@app.get("/")
def root():
    return {"message": "VisioBrain No-DB Backend is alive 🚀"}
