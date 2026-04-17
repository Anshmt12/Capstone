"""Document parser for PDFs and scanned images using PyMuPDF + Tesseract."""
import logging
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings

logger = logging.getLogger(__name__)


class DocumentParser:
    """Parse PDFs and images, extract text with OCR fallback."""

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def parse_pdf(self, file_path: str) -> list[dict]:
        """Extract text from PDF, using OCR for scanned pages."""
        doc = fitz.open(file_path)
        pages = []
        for page_num, page in enumerate(doc):
            text = page.get_text("text").strip()
            # If very little text extracted, try OCR
            if len(text) < 50:
                text = self._ocr_page(page)
            if text:
                pages.append({
                    "text": text,
                    "page": page_num + 1,
                    "source": Path(file_path).name,
                })
        doc.close()
        logger.info(f"Extracted {len(pages)} pages from {file_path}")
        return pages

    def _ocr_page(self, page) -> str:
        """OCR a single PDF page using Tesseract."""
        try:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(img, lang="eng")
            return text.strip()
        except Exception as e:
            logger.warning(f"OCR failed: {e}")
            return ""

    def parse_image(self, file_path: str) -> str:
        """Extract text from an image using Tesseract OCR."""
        img = Image.open(file_path)
        return pytesseract.image_to_string(img, lang="eng").strip()

    def chunk_text(self, text: str, metadata: dict = None) -> list[dict]:
        """Split text into chunks with metadata."""
        chunks = self.splitter.split_text(text)
        return [
            {"text": chunk, "metadata": {**(metadata or {}), "chunk_index": i}}
            for i, chunk in enumerate(chunks)
        ]

    def parse_and_chunk(self, file_path: str) -> list[dict]:
        """Parse a file and return chunks with metadata."""
        path = Path(file_path)
        if path.suffix.lower() == ".pdf":
            pages = self.parse_pdf(file_path)
            all_chunks = []
            for page_data in pages:
                chunks = self.chunk_text(
                    page_data["text"],
                    {"source": page_data["source"], "page": page_data["page"]},
                )
                all_chunks.extend(chunks)
            return all_chunks
        elif path.suffix.lower() in (".png", ".jpg", ".jpeg", ".tiff", ".bmp"):
            text = self.parse_image(file_path)
            return self.chunk_text(text, {"source": path.name})
        else:
            # Plain text
            text = path.read_text(encoding="utf-8", errors="ignore")
            return self.chunk_text(text, {"source": path.name})
