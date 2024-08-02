from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from hashlib import md5
from capture.commands.capture_info import CaptureInfo
from capture.commands.capture_info_from_pdf import CaptureInfoFromPdf
from capture.data_types.uploaded import UploadedContent
import asyncio
import tempfile
from capture.commands.enforce_limits import EnforceLimitsCommand

@login_required
def index(request):
    return render(request, 'capture/index.html')

@login_required
def process_text_info(request):
    text = request.POST['text']
    enforce_limits_command = EnforceLimitsCommand(text)
    enforce_limits_command.run()
    content_id = md5(text.encode('utf-8')).hexdigest()
    capture_info = CaptureInfo(uploaded_content=UploadedContent(
        content_id=content_id, 
        content=text)
        )
    asyncio.run(capture_info.execute())
    events = capture_info.parsed_events
    return render(request, 'capture/event_details.html', {'events': events})


@login_required
def process_pdf_upload(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            for chunk in pdf_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        enforce_limits_command = EnforceLimitsCommand(temp_file_path)
        enforce_limits_command.run()

        capture_info = CaptureInfoFromPdf(file_path=temp_file_path)
        asyncio.run(capture_info.execute())
        return render(request, 'capture/event_details.html', {'events': capture_info.parsed_events})
    else:
        return HttpResponse("No file uploaded")