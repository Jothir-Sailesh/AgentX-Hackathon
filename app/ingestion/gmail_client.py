import imaplib
import email
from email.message import Message
from typing import List, Optional
from app.core.config import settings


class GmailClient:
    """
    Gmail IMAP client using EMAIL_USER / EMAIL_PASSWORD from config
    """

    def __init__(self):
        self.imap_server = "imap.gmail.com"
        self.email_user = settings.EMAIL_USER
        self.email_password = (
            settings.EMAIL_PASSWORD.get_secret_value()
            if settings.EMAIL_PASSWORD
            else None
        )
        self.connection: Optional[imaplib.IMAP4_SSL] = None

    def connect(self):
        if not self.email_user or not self.email_password:
            raise ValueError("EMAIL_USER or EMAIL_PASSWORD not set in environment")

        self.connection = imaplib.IMAP4_SSL(self.imap_server)
        self.connection.login(self.email_user, self.email_password)
        self.connection.select("inbox")

    def fetch_unread_emails(self, limit: int = 10) -> List[Message]:
        if not self.connection:
            raise ConnectionError("Not connected to Gmail")

        status, messages = self.connection.search(None, "UNSEEN")
        if status != "OK":
            return []

        email_ids = messages[0].split()
        fetched = []

        for email_id in reversed(email_ids[-limit:]):
            res, msg_data = self.connection.fetch(email_id, "(BODY.PEEK[])")
            if res != "OK":
                continue

            for part in msg_data:
                if isinstance(part, tuple):
                    msg = email.message_from_bytes(part[1])
                    fetched.append(msg)

        return fetched

    def close(self):
        if self.connection:
            self.connection.logout()
            self.connection = None
