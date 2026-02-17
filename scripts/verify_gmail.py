import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from app.ingestion.gmail_client import GmailClient
from app.core.config import settings

def verify_gmail_connection():
    print(f"Checking configuration...")
    if not settings.EMAIL_USER or not settings.EMAIL_PASSWORD:
        print("❌ EMAIL_USER or EMAIL_PASSWORD not set in .env")
        return

    print("✅ Configuration found.")
    
    client = GmailClient()
    try:
        print("Connecting to Gmail...")
        client.connect()
        print("✅ Connected successfully.")
        
        print("Fetching unread emails...")
        emails = client.fetch_unread_emails(limit=5)
        print(f"✅ Fetched {len(emails)} unread emails.")
        
        for i, msg in enumerate(emails):
            print(f"  [{i+1}] Subject: {msg['subject']}")
            print(f"      From: {msg['from']}")
            
        client.close()
        print("✅ Connection closed.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_gmail_connection()
