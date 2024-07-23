import streamlit as st
from commands.capture_info import CaptureInfo
from commands.capture_info_from_pdf import CaptureInfoFromPdf
from data_types.uploaded import UploadedContent
import asyncio
from hashlib import md5
import tempfile

path_to_take = st.query_params.get("q")
if path_to_take == None:
    st.write("Please provide a path to take")
elif path_to_take=="text":
    st.write("Lets extract important information from your text")
    # Allow user to upload a PDF file
    st_text = st.text_area("Enter your text here")

    if st_text:
        st.write("Extracting information from your text")
        content_id = md5(st_text.encode('utf-8')).hexdigest()
        capture_info = CaptureInfo(uploaded_content=UploadedContent(
            content_id=content_id, 
            content=st_text)
            )
        asyncio.run(capture_info.execute())
        st.write(capture_info.parsed_events)
elif path_to_take=="pdf":
    st.write("Lets extract important information from your PDF")
    
    # Allow user to upload a PDF file
    st_pdf = st.file_uploader("Upload your PDF here")
    if st_pdf:
        st.write("Extracting information from your PDF")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(st_pdf.read())
            temp_file_path = temp_file.name
            capture_info = CaptureInfoFromPdf(file_path=temp_file_path)
            asyncio.run(capture_info.execute())
            st.write(capture_info.parsed_events)

