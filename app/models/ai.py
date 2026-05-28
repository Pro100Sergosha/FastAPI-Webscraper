import uuid
from typing import Optional

from sqlmodel import Field, SQLModel


class MessageLog(SQLModel, table=True):
    """
    Database model representing a log of a user message and its AI analysis.
    """

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_message: str
    topic: str
    language: str
    sentiment: str
    ai_response_text: str
