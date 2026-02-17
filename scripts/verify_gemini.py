import sys
from pathlib import Path
import os

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.gemini_client import GeminiClient
from app.core.config import settings

def verify_gemini_client():
    print("🚀 Starting Gemini Client Verification...")

    # Check config
    if not settings.GEMINI_API_KEY and not settings.LLM_API_KEY:
        print("❌ GEMINI_API_KEY or LLM_API_KEY not set in .env")
        return

    try:
        client = GeminiClient()
        prompt = "Explain quantum computing in one sentence."
        
        print(f"📝 Prompt: {prompt}")
        print("🤖 Generating response...")
        
        response = client.generate(prompt)
        
        print("\n✅ Response Received:")
        print(f"   {response}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    with open("gemini_results.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        verify_gemini_client()

