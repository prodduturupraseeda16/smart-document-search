from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import logging

load_dotenv()


def get_llm():
    try:
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )
    except Exception as e:
        logging.error(f"Failed to initialize ChatGroq client: {str(e)}", exc_info=True)
        raise RuntimeError("The AI service is temporarily unavailable. Please try again later.")