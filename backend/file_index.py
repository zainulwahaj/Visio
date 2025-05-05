from typing import Dict
from pydantic import BaseModel
import uuid

class FileInfo(BaseModel):
    id: str
    filename: str
    filepath: str
    content_type: str

# id → FileInfo
INDEX: Dict[str, FileInfo] = {}

def add_file(filename: str, filepath: str, content_type: str) -> FileInfo:
    file_id = str(uuid.uuid4())
    info = FileInfo(id=file_id, filename=filename, filepath=filepath, content_type=content_type)
    INDEX[file_id] = info
    return info

def get_file(file_id: str) -> FileInfo | None:
    return INDEX.get(file_id)

def list_files() -> list[FileInfo]:
    return list(INDEX.values())
