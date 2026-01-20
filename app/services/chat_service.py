from sqlmodel import Session

from app.interfaces.ai_client import AIClient
from app.models.ai import MessageLog
from app.schemas.schemas import AnalyzeResponse


class ChatService:
    """
    Service responsible for handling chat interactions and analyzing user messages.
    """

    def __init__(self, ai_client: AIClient, session: Session):
        """
        Initializes the ChatService with an AI client and a database session.

        :param ai_client: The client used to interact with the AI service.
        :param session: The database session for persisting message logs.
        """
        self.ai_client = ai_client
        self.session = session

    async def analyze_and_save(self, user_text: str) -> AnalyzeResponse:
        """
        Analyzes the user's text using the AI client and saves the result to the database.

        :param user_text: The text message provided by the user.
        :return: An AnalyzeResponse object containing the status and the AI's response text.
        """
        ai_response = await self.ai_client.analyze_text(user_text)

        db_entry = MessageLog(
            user_message=user_text,
            topic=ai_response.get("topic", "Unknown"),
            language=ai_response.get("language", "Unknown"),
            sentiment=ai_response.get("sentiment", "Unknown"),
            ai_response_text=ai_response.get("text", "No response generated"),
        )

        self.session.add(db_entry)
        self.session.commit()
        self.session.refresh(db_entry)

        return AnalyzeResponse(status="success", response=ai_response.get("text", ""))
