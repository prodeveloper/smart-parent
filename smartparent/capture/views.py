from django.shortcuts import render
from django.http import HttpResponse, Http404
from hashlib import md5
from capture.commands.capture_info import CaptureInfo
from capture.data_types.uploaded import UploadedContent
import asyncio

def index(request):
    return render(request, 'capture/index.html')

def process_text_info(request):
    text = request.POST['text']
    content_id = md5(text.encode('utf-8')).hexdigest()
    capture_info = CaptureInfo(uploaded_content=UploadedContent(
        content_id=content_id, 
        content=text)
        )
    asyncio.run(capture_info.execute())
    return HttpResponse(capture_info.parsed_events)
# Create your views here.
