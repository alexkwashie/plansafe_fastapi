from fastapi import HTTPException, UploadFile
from db.supabase_client import supabase
import uuid


BUCKET_NAME = "documents"


def upload_file(file: UploadFile, folder: str = "notes") -> str:
    """Upload a file to Supabase Storage and return the public URL."""
    try:
        file_ext = file.filename.split(".")[-1] if file.filename and "." in file.filename else "bin"
        file_path = f"{folder}/{uuid.uuid4()}.{file_ext}"

        file_bytes = file.file.read()

        supabase.storage.from_(BUCKET_NAME).upload(
            path=file_path,
            file=file_bytes,
            file_options={"content-type": file.content_type or "application/octet-stream"},
        )

        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)
        return public_url

    except Exception as error:
        print(f"======= Upload error: {error}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(error)}")
