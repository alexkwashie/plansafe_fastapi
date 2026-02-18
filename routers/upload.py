from fastapi import APIRouter, Depends, File, UploadFile
from dependencies.auth_token import get_current_user
from db.storage import upload_file


router = APIRouter(
    prefix='/api/v1',
    tags=['uploads']
)


@router.post('/upload')
async def upload(file: UploadFile = File(...), folder: str = "notes", user=Depends(get_current_user)):
    """Upload a file to Supabase Storage. Returns the public URL."""
    url = upload_file(file, folder)
    return {"url": url}
