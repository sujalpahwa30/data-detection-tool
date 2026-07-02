from pathlib import Path

import pandas as pd
from pypdf import PdfReader

from app.models.schemas import ParsedDocument


class DocumentParser:
    """
    Handles text extraction for supported document types.
    """

    @staticmethod
    def extract_text(file_path: Path) -> ParsedDocument:
        extension = file_path.suffix.lower()

        parsers = {
            ".pdf": DocumentParser._parse_pdf,
            ".txt": DocumentParser._parse_txt,
            ".csv": DocumentParser._parse_csv,
        }

        parser = parsers.get(extension)

        if parser is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return parser(file_path)

    @staticmethod
    def _parse_pdf(file_path: Path) -> ParsedDocument:
        reader = PdfReader(file_path)

        extracted_text = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text)

        text = "\n".join(extracted_text).strip()

        if not text:
            raise ValueError("No extractable text found in PDF.")

        return ParsedDocument(
            text=text,
            pages=len(reader.pages),
            characters=len(text),
            document_type="pdf",
        )

    @staticmethod
    def _parse_txt(file_path: Path) -> ParsedDocument:
        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).strip()

        if not text:
            raise ValueError("Text file is empty.")

        return ParsedDocument(
            text=text,
            pages=1,
            characters=len(text),
            document_type="txt",
        )

    @staticmethod
    def _parse_csv(file_path: Path) -> ParsedDocument:
        df = pd.read_csv(file_path)

        text = df.to_string(index=False).strip()

        if not text:
            raise ValueError("CSV file is empty.")

        return ParsedDocument(
            text=text,
            pages=1,
            characters=len(text),
            document_type="csv",
        )