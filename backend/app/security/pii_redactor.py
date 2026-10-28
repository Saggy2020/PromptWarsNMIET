"""
PII Redactor: Strips emails, phone numbers, credit cards, and addresses from untrusted text
before transmission to external LLM APIs.
"""

import re
from typing import Tuple

# Regex patterns for common PII
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
PHONE_REGEX = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
CREDIT_CARD_REGEX = re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b|\b\d{15,16}\b')
SSN_REGEX = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
ADDRESS_PATTERNS = re.compile(r'\b\d{1,5}\s+[A-Za-z0-9\s.,]{3,30}\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b', re.IGNORECASE)

class PIIRedactor:
    def redact(self, text: str) -> Tuple[str, int]:
        """
        Redacts PII matches from text.
        Returns: (sanitized_text, count_of_redactions)
        """
        if not text:
            return "", 0

        count = 0
        
        # Redact Credit Cards
        text, n = CREDIT_CARD_REGEX.subn("[REDACTED_CARD_NUMBER]", text)
        count += n
        
        # Redact SSN
        text, n = SSN_REGEX.subn("[REDACTED_SSN]", text)
        count += n
        
        # Redact Emails
        text, n = EMAIL_REGEX.subn("[REDACTED_EMAIL]", text)
        count += n
        
        # Redact Phone numbers
        text, n = PHONE_REGEX.subn("[REDACTED_PHONE]", text)
        count += n
        
        # Redact Physical Addresses
        text, n = ADDRESS_PATTERNS.subn("[REDACTED_ADDRESS]", text)
        count += n

        return text, count

pii_redactor = PIIRedactor()
