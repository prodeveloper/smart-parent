from commands.capture_info_from_pdf import CaptureInfoFromPdf
import asyncio
import pytest
from commands.log_item import LogItem

@pytest.mark.asyncio
async def test_extracts_text_from_pdf():
    command = CaptureInfoFromPdf(file_path="sample_pdfs/sample.pdf")
    command.executed = True
    command._pull_all_text_from_pdf()
    text_in_pdf = """
ed to grow. They will take measurements each week and observe how the beans grow. Pu
""".strip()
    assert text_in_pdf in command.pdf_text