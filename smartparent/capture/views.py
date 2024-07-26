from django.shortcuts import render
from django.http import HttpResponse, Http404

def index(request):
    return HttpResponse("Hello, world. You're at the capture index.")
# Create your views here.
