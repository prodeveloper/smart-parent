from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_home():
    with open("html/home.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)



@app.get("/calendar", response_class=HTMLResponse)
def read_calendar():
    with open("html/calendar.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.get("/capture", response_class=HTMLResponse)
def read_capture_info():
    with open("html/capture_info.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)