from PyPDF2 import PdfReader
from docx import Document
import io
from ai_agent.yandex_gpt import generate_theme_blocks


# path = "../files/new_document.pdf"


def read_pdf(bytes_):
    text = str()
    reader = PdfReader(bytes_)

    for page in reader.pages:
        text += page.extract_text()
    return text


def read_docx(file_stream: io.BytesIO):
    doc = Document(file_stream)
    text = str()
    for para in doc.paragraphs:
        text += para.text
    return text
