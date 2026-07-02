from pydantic import BaseModel
from typing import List, Optional


class ParsedDocument(BaseModel):
    text: str
    pages: int
    characters: int
    document_type: str


class SensitiveFinding(BaseModel):
    type: str
    value: str
    confidence: float
    page: Optional[int] = None


class RiskAnalysis(BaseModel):
    score: int
    level: str


class UploadResponse(BaseModel):
    success: bool
    message: str
    document_id: str
    filename: str