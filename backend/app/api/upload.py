from pathlib import Path
import shutil
import uuid

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.services.parser import DocumentParser 

from app.config import UPLOAD_DIR

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

# Allowed document types
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".csv"}

# 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document and save it to disk.

    Supported formats:
    - PDF
    - TXT
    - CSV
    """

    # Ensure upload directory exists
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Validate filename
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing.",
        )

    # Validate extension
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # -----------------------------
    # Validate file size
    # -----------------------------
    file.file.seek(0, 2)  # Move to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset pointer

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of {MAX_FILE_SIZE // (1024 * 1024)} MB.",
        )

    # Generate unique document ID
    document_id = str(uuid.uuid4())

    stored_filename = f"{document_id}{extension}"

    file_path = UPLOAD_DIR / stored_filename

    try:
        # Save file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        parsed_document = DocumentParser.extract_text(file_path)

    except Exception as e:
        # Remove partially written file if it exists
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file. {str(e)}",
        )

    finally:
        file.file.close()

    return {
        "success": True,
        "message": "File uploaded and parsed successfully.",
        "data": {
            "document_id": document_id,
            "original_filename": file.filename,
            "stored_filename": stored_filename,
            "file_size_bytes": file_size,
            "file_type": extension,
            "parsed_document": parsed_document.model_dump(), 
        },
    }