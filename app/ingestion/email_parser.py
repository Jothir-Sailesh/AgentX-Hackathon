import os
import email
from email.message import Message
from pathlib import Path
from typing import List, Dict, Optional
import uuid

class EmailParser:
    """
    Parses email messages to extract PDF attachments.
    """
    
    def __init__(self, data_dir: str = "data/pdfs"):
        self.data_dir = Path(data_dir)
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Creates the data directory if it doesn't exist."""
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_safe_filename(self, filename: str) -> str:
        """
        Generates a safe filename to avoid collisions.
        Appends a UUID to the filename stem.
        """
        if not filename:
            filename = "attachment.pdf"
            
        path = Path(filename)
        stem = path.stem
        suffix = path.suffix
        
        # Sanitize stem (basic)
        stem = "".join(c for c in stem if c.isalnum() or c in (' ', '.', '_', '-')).strip()
        stem = stem.replace(' ', '_')
        
        unique_id = str(uuid.uuid4())[:8]
        return f"{stem}_{unique_id}{suffix}"

    def extract_pdfs(self, emails: List[Message]) -> List[Dict]:
        """
        Iterates through a list of emails and extracts PDF attachments.
        
        Returns:
            List[Dict]: Metadata of extracted PDFs.
        """
        extracted_files = []

        for msg in emails:
            subject = msg.get("Subject", "(No Subject)")
            sender = msg.get("From", "(Unknown Sender)")

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                
                if part.get("Content-Disposition") is None:
                    continue

                content_type = part.get_content_type()
                filename = part.get_filename()

                # Check if it's a PDF
                is_pdf = content_type == "application/pdf" or (filename and filename.lower().endswith(".pdf"))
                
                if is_pdf and filename:
                    safe_filename = self._get_safe_filename(filename)
                    file_path = self.data_dir / safe_filename
                    
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            with open(file_path, "wb") as f:
                                f.write(payload)
                            
                            extracted_files.append({
                                "file_path": str(file_path),
                                "original_filename": filename,
                                "email_subject": subject,
                                "email_from": sender,
                                "saved_filename": safe_filename
                            })
                    except Exception as e:
                        print(f"Error saving attachment {filename}: {e}")
                        # Continue to next attachment/email
                        continue

        return extracted_files
