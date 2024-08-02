from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from hashlib import md5
from capture.commands.capture_info import CaptureInfo
from capture.commands.capture_info_from_pdf import CaptureInfoFromPdf
from capture.data_types.uploaded import UploadedContent
import asyncio
import tempfile
from capture.models import CapturedEvent
from capture.events.capture_processed import CaptureProcessedEvent

@login_required
def index(request):
    return render(request, 'capture/index.html')

@login_required
def event_list(request):
    events = CapturedEvent.objects.filter(owner=request.user)
    return render(request, 'capture/event_list.html', {'events': events})

@login_required
def event_edit(request, event_id):
    event = CapturedEvent.objects.get(id=event_id)
    return render(request, 'capture/event_edit.html', {'event': event})

@login_required
def process_text_info(request):
    text = request.POST['text']
    content_id = md5(text.encode('utf-8')).hexdigest()
    capture_info = CaptureInfo(uploaded_content=UploadedContent(
        content_id=content_id, 
        content=text)
        )
    asyncio.run(capture_info.execute())
    capture_processed_event = CaptureProcessedEvent(capture_info=capture_info, user=request.user)
    asyncio.run(capture_processed_event.broadcast())
    events = capture_info.parsed_events
    return render(request, 'capture/event_details.html', {'events': events})


@login_required
def process_pdf_upload(request):
    """
    Process a PDF file upload and return the events to the user
    """
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            for chunk in pdf_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        capture_info_from_pdf = CaptureInfoFromPdf(file_path=temp_file_path)
        asyncio.run(capture_info_from_pdf.execute())
        capture_processed_event = CaptureProcessedEvent(
            capture_info=capture_info_from_pdf.captured_info,
            user=request.user)
        capture_processed_event.broadcast()
        return render(request, 'capture/event_details.html', {'events': capture_info_from_pdf.parsed_events})
    else:
        return HttpResponse("No file uploaded")