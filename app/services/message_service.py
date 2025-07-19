from sqlmodel import Session, select
from sqlalchemy import func
from sqlmodel.sql.expression import desc  # Import desc for ordering
from ..models import UserMessage
from typing import List, Dict


def create_user_message(
    session: Session, user_name: str, user_message: str
) -> UserMessage:
    db_user_message = UserMessage(user_name=user_name, user_message=user_message)
    session.add(db_user_message)
    session.commit()
    session.refresh(db_user_message)
    return db_user_message


def get_paginated_messages(
    session: Session, offset: int, limit: int
) -> tuple[List[Dict], bool, int | None]:
    # Use desc() function for ordering to resolve Mypy error
    query = (
        select(UserMessage)
        .order_by(desc(UserMessage.created_at))
        .offset(offset)
        .limit(limit)
    )
    db_messages = session.exec(query).all()

    messages_to_send = []
    for msg in db_messages:
        messages_to_send.append(
            {
                "id": msg.id,
                "user_name": msg.user_name,
                "user_message": msg.user_message,
                "created_at": msg.created_at.strftime("%b %d, %Y %I:%M %p"),
            }
        )

    # FIX: Use select(func.count()).select_from(UserMessage) for robust row counting
    # This avoids Mypy's "int | None" error for func.count(UserMessage.id)
    total_count_query = select(func.count()).select_from(UserMessage)
    total_messages = session.exec(total_count_query).one()
    has_more = (offset + limit) < total_messages
    next_offset = offset + limit if has_more else None

    return messages_to_send, has_more, next_offset
