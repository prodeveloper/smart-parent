from capture.commands.capture_info_from_pdf import CaptureInfoFromPdf
from django.test import TestCase

class TestPdfExtraction(TestCase):
    """
    Test the PDF extraction functionality.
    """
    def test_extracts_text_from_pdf(self):
        """
        Test that the CaptureInfoFromPdf command correctly extracts text from a PDF file.

        This test:
        1. Creates a CaptureInfoFromPdf instance with a sample PDF file.
        2. Calls the _pull_all_text_from_pdf method to extract text.
        3. Checks if a specific text snippet is present in the extracted text.
        """
        command = CaptureInfoFromPdf(file_path="sample_pdfs/sample.pdf")
        command.executed = True
        command._pull_all_text_from_pdf()
        text_in_pdf = """
    ed to grow. They will take measurements each week and observe how the beans grow. Pu
    """.strip()
        assert text_in_pdf in command.pdf_text