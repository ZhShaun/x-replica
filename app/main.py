from fastapi import FastAPI, Request, Form, Response, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from .db import create_db_and_tables, get_session
from .models import UserMessage
from contextlib import asynccontextmanager
from sqlmodel import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


templates = Jinja2Templates(directory="app/templates")
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")


@app.get("/modal", response_class=HTMLResponse)
def get_modal(request: Request):
    context = {
        "request": request,
        "modal_title": "今日の質問",
        "modal_body": "最近読んだ本は何ですか？",
    }
    return templates.TemplateResponse("modal_content.html", context)

@app.post("/submit-modal-form", response_class=HTMLResponse)
def submit_modal_form(
    user_name: Annotated[str, Form()],
    user_message: Annotated[str, Form()],
    session: Session = Depends(get_session),
):
    """
    Endpoint to handle form submission from the modal.
    """
    print("Received form submission:")
    print(f"  Name: {user_name}")
    print(f"  Message: {user_message}")

    db_user_message = UserMessage(user_name=user_name, user_message=user_message)
    success = False
    try:
        session.add(db_user_message) 
        session.commit()             
        session.refresh(db_user_message) # Refresh the object to get its ID (and any default values)

        print(f"Saved message with ID: {db_user_message.id}")
        success = True
    except Exception as e:
        print(f"Error saving message: {e}")
        success = False

    if success:
        return Response(content="", status_code=200) # HTMX expects 200 for success
    else:
        response_html = """
        <div class="alert alert-danger" role="alert">
            Oops! Something went wrong. Please try again.
        </div>
        """
        return HTMLResponse(content=response_html, status_code=400)

