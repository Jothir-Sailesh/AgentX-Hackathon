import sys
import os
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from app.ingestion.email_parser import EmailParser

def test_email_parser():
    print("Testing EmailParser...")
    
    # Setup dummy data directory for testing
    test_data_dir = "tests/data/pdfs"
    parser = EmailParser(data_dir=test_data_dir)
    
    # Crate a dummy email
    msg = MIMEMultipart()
    msg['Subject'] = 'Test Email with PDF'
    msg['From'] = 'sender@example.com'
    msg['To'] = 'receiver@example.com'
    
    # Add body
    msg.attach(MIMEText('This is a test email body.', 'plain'))
    
    # Add PDF attachment
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
    part = MIMEApplication(pdf_content, Name="test_invoice.pdf")
    part['Content-Disposition'] = 'attachment; filename="test_invoice.pdf"'
    msg.attach(part)
    
    # Run parser
    print("Extracting PDFs...")
    results = parser.extract_pdfs([msg])
    
    # Verify results
    if len(results) == 1:
        print("✅ Successfully extracted 1 PDF.")
        print(f"   Original Filename: {results[0]['original_filename']}")
        print(f"   Saved Path: {results[0]['file_path']}")
        
        # Verify file exists
        if os.path.exists(results[0]['file_path']):
            print("✅ File exists on disk.")
            
            # Clean up
            os.remove(results[0]['file_path'])
            print("✅ Cleaned up test file.")
        else:
            print("❌ File was not saved to disk.")
    else:
        print(f"❌ Expected 1 extracted PDF, found {len(results)}.")

    # Cleanup directory
    try:
        os.rmdir(test_data_dir)
    except:
        pass

if __name__ == "__main__":
    with open("test_results.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        test_email_parser()

