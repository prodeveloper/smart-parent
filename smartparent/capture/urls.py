from django.urls import path

from . import views
app_name = 'capture'

urlpatterns = [
    path("", views.index, name="index"),
    path("process_text_info/", views.process_text_info, name="process_text_info"),
    path("process_pdf_upload/", views.process_pdf_upload, name="process_pdf_upload"),
]