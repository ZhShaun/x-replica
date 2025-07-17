from fastapi import APIRouter, Request, Form, Response, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlmodel import Session

from ..db import get_session
from ..services import message_service  # Import the service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/submit-modal-form", response_class=HTMLResponse)
def submit_modal_form(
    user_name: Annotated[str, Form()],
    user_message: Annotated[str, Form()],
    session: Session = Depends(get_session),
):
    try:
        message_service.create_user_message(session, user_name, user_message)
        return Response(
            content="",
            status_code=200,
            headers={"HX-Trigger": "closeModal, refreshTimeline"},
        )
    except Exception as e:
        print(f"Error saving message: {e}")
        response_html = """<div class="alert alert-danger" role="alert">Oops! Something went wrong. Please try again.</div>"""
        return HTMLResponse(content=response_html, status_code=400)


@router.get("/timeline-events", response_class=HTMLResponse)
async def get_timeline_events(
    request: Request,
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(5, ge=1, le=20),
):
    messages_to_send, has_more, next_offset = message_service.get_paginated_messages(
        session, offset, limit
    )

    context = {
        "request": request,
        "messages": messages_to_send,
        "next_offset": next_offset,
        "has_more": has_more,
    }
    return templates.TemplateResponse("timeline_events.html", context)
