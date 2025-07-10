from typing import Optional
from sqlmodel import Field, SQLModel

class UserMessageBase(SQLModel):
    user_name: str = Field(index=True) 
    user_message: str

class UserMessage(UserMessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # You might want to add a timestamp
    # created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    # For now, let's keep it simple.

# Optional: Pydantic models for request/response if needed for validation/filtering
class UserMessageCreate(UserMessageBase):
    pass # No extra fields for creation beyond base

class UserMessagePublic(UserMessageBase):
    id: int
    # created_at: datetime # Include if you add it to the main model