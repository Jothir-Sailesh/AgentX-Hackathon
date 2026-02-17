import google.generativeai as genai
from app.core.config import settings

class GeminiClient:
    """
    A wrapper for the Google Gemini API.
    """
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            # Fallback to LLM_API_KEY if GEMINI_API_KEY is not set
            api_key = settings.LLM_API_KEY.get_secret_value() if settings.LLM_API_KEY else None
        else:
            api_key = settings.GEMINI_API_KEY.get_secret_value()
            
        if not api_key:
            raise ValueError("GEMINI_API_KEY or LLM_API_KEY must be set in settings.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def generate(self, prompt: str) -> str:
        """
        Generates content from the Gemini model based on the prompt.
        
        Args:
            prompt (str): The input prompt.
            
        Returns:
            str: The generated text response.
            
        Raises:
            Exception: If an API error occurs.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Log the error or re-raise with a custom exception if needed
            # For now, we'll raise it to fail gracefully as per requirements (caller handles it)
            raise RuntimeError(f"Gemini API Error: {str(e)}")
