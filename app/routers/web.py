from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse("app/static/index.html")


@router.get("/modal", response_class=HTMLResponse)
def get_modal(request: Request):
    context = {
        "request": request,
        "modal_title": "今日の質問",
        "modal_body": "最近読んだ本は何ですか？",
    }
    return templates.TemplateResponse("modal_content.html", context)
