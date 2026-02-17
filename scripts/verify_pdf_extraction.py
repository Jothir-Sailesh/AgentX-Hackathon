import sys
from pathlib import Path
from typing import List

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from app.ingestion.gmail_client import GmailClient
from app.ingestion.email_parser import EmailParser
from app.core.config import settings

def verify_pdf_extraction():
    print("🚀 Starting PDF Extraction Verification...")

    # Check config
    if not settings.EMAIL_USER or not settings.EMAIL_PASSWORD:
        print("❌ EMAIL_USER or EMAIL_PASSWORD not set in .env")
        return

    gmail_client = GmailClient()
    parser = EmailParser()

    try:
        # 1. Connect
        print("📡 Connecting to Gmail...")
        gmail_client.connect()
        print("✅ Connected.")

        # 2. Fetch
        print("📥 Fetching unread emails (limit=10)...")
        emails = gmail_client.fetch_unread_emails(limit=10)
        print(f"✅ Fetched {len(emails)} unread emails.")

        if not emails:
            print("⚠️ No unread emails found. Send yourself an email with a PDF attachment to test.")
            return

        # 3. Parse and Extract
        print("🔍 Scanning for PDF attachments...")
        extracted_pdfs = parser.extract_pdfs(emails)

        # 4. Report
        if extracted_pdfs:
            print(f"\n✅ Successfully extracted {len(extracted_pdfs)} PDF(s):")
            for pdf in extracted_pdfs:
                print(f"   📄 File: {pdf['saved_filename']}")
                print(f"      Path: {pdf['file_path']}")
                print(f"      From: {pdf['email_subject']}")
        else:
            print("\n⚠️ No PDF attachments found in the fetched emails.")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    finally:
        # 5. Cleanup
        if gmail_client:
            gmail_client.close()
            print("\nExample finished. Connection closed.")

if __name__ == "__main__":
    # Ensure stdout is unbuffered or flush explicitly if redirecting
    verify_pdf_extraction()
