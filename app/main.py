from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def read_root():
    """
    root endpoint of the API, returning static part of website
    """
    return FileResponse("app/static/index.html")

@app.get("/modal", response_class=HTMLResponse)
def get_modal(request: Request):
    context = {"request": request, "modal_title": "Dynamic Modal Title", "modal_body": "This text came from the backend!"}
    return templates.TemplateResponse("modal_content.html", context)
