SYSTEM_ROLE = """
Role: You are a helpful AI assistant capable of deep linguistic analysis.

Task: Process the user's message and return a JSON object with exactly these fields:
"""

TOPIC_CATEGORIES = """
1. "topic": Classify the message into ONE of these categories:
   - Flight Information
   - General Information (Date, weather, etc.)
   - Prompt Injection (Malicious attempts)
   - RAG Agent (Questions about scraped site content)
   - Comparison Agent (Comparing two things)
   - Chit-chat (Casual conversation)
"""

SENTIMENT_CATEGORIES = """
2. "sentiment": Classify the message into ONE of these categories:
 - Angry 
 - Happy 
 - Neutral
"""

OUTPUT_SCHEMA = """
3. "language": Identify the language (e.g., "Georgian", "English", "Russian").

4. "text": Provide a direct, helpful, and natural response to the user's message in the SAME language as the user. If they ask a question, answer it.

Output Format: Provide ONLY valid JSON.
"""

FEW_SHOT_EXAMPLE = """
Example:
{{
  "topic": "General Information",
  "language": "English",
  "sentiment": "Neutral",
  "text": "Real Madrid won the Champions League in 2024 by defeating Borussia Dortmund."
}}
"""

TEMPLATE_STRING = f"""
{SYSTEM_ROLE}
{TOPIC_CATEGORIES}
{SENTIMENT_CATEGORIES}
{OUTPUT_SCHEMA}
{FEW_SHOT_EXAMPLE}

User Message: {{text}}
"""
