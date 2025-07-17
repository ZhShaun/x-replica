from fastapi import APIRouter, Request, Form, Response, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlmodel import Session, select
from sqlalchemy import func
from datetime import datetime

from ..db import get_session
from ..models import UserMessage

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/submit-modal-form", response_class=HTMLResponse)
def submit_modal_form(
    user_name: Annotated[str, Form()],
    user_message: Annotated[str, Form()],
    session: Session = Depends(get_session),
):
    db_user_message = UserMessage(user_name=user_name, user_message=user_message)
    try:
        session.add(db_user_message)
        session.commit()
        session.refresh(db_user_message)
        return Response(content="", status_code=200, headers={"HX-Trigger": "closeModal, refreshTimeline"})
    except Exception as e:
        print(f"Error saving message: {e}")
        response_html = """<div class="alert alert-danger" role="alert">Oops! Something went wrong. Please try again.</div>"""
        return HTMLResponse(content=response_html, status_code=400)

@router.get("/timeline-events", response_class=HTMLResponse)
async def get_timeline_events(
    request: Request,
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(5, ge=1, le=20)
):
    query = select(UserMessage).order_by(UserMessage.created_at.desc()).offset(offset).limit(limit)
    db_messages = session.exec(query).all()

    messages_to_send = []
    for msg in db_messages:
        messages_to_send.append({
            "id": msg.id,
            "user_name": msg.user_name,
            "user_message": msg.user_message,
            "created_at": msg.created_at.strftime("%b %d, %Y %I:%M %p")
        })

    total_count_query = select(func.count(UserMessage.id))
    total_messages = session.exec(total_count_query).one()
    has_more = (offset + limit) < total_messages
    next_offset = offset + limit if has_more else None

    context = {
        "request": request,
        "messages": messages_to_send,
        "next_offset": next_offset,
        "has_more": has_more
    }
    return templates.TemplateResponse("timeline_events.html", context)
