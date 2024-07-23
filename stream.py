import streamlit as st
from commands.capture_info import CaptureInfo
from data_types.uploaded import UploadedContent
import asyncio
from hashlib import md5

st.write("Lets extract important information from your text")
# Allow user to upload a PDF file
st_text = st.text_area("Enter your text here")

if st_text:
    st.write("Extracting information from your text")
    content_id = md5(st_text.encode('utf-8')).hexdigest()
    capture_info = CaptureInfo(UploadedContent(
        content_id=content_id, 
        content=st_text)
        )
    asyncio.run(capture_info.execute())
    st.write(capture_info.parsed_events)