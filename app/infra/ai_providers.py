from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.interfaces.ai_client import AIClient
from app.services.prompts import TEMPLATE_STRING


class GeminiClient(AIClient):
    """
    Implementation of AIClient using Google's Gemini model via LangChain.
    """

    def __init__(self, api_key: str):
        """
        Initializes the GeminiClient with the provided API key.

        :param api_key: The Google API key for accessing Gemini.
        """
        self.chat = ChatGoogleGenerativeAI(
            vertexai=True,
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3,
        )
        self.parser = JsonOutputParser()
        self.prompt_template = ChatPromptTemplate.from_template(
            template=TEMPLATE_STRING
        )

        self.chain = self.prompt_template | self.chat | self.parser

    async def analyze_text(self, text: str) -> dict:
        """
        Analyzes the text using the configured Gemini model chain.

        :param text: The text to analyze.
        :return: A dictionary containing the analysis results or an error message.
        """
        try:
            return await self.chain.ainvoke({"text": text})
        except Exception as e:
            print(f"AI Error: {e}")
            return {
                "topic": "Error",
                "language": "Unknown",
                "sentiment": "Neutral",
                "text": "Sorry, I am having trouble processing your request right now.",
            }
