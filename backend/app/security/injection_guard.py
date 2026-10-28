"""
Adversarial Prompt-Injection Defense Filter.
Detects prompt-injection attempts, jailbreak payloads, delimiter injection,
and enforces strict boundary sanitization.
"""

import re
from typing import Tuple, List

# Signatures for adversarial prompt injections, jailbreaks & instruction leak attempts
ADVERSARIAL_PATTERNS = [
    re.compile(r'ignore\s+(?:all\s+)?(?:previous\s+|prior\s+|system\s+)?(?:instructions|commands|restrictions|rules|prompt)', re.IGNORECASE),
    re.compile(r'disregard\s+(?:all\s+)?(?:previous|prior|safety|guardian|commands)', re.IGNORECASE),
    re.compile(r'forget\s+(?:all\s+)?(?:constraints|instructions|restrictions|rules)', re.IGNORECASE),
    re.compile(r'override\s+(?:all\s+)?(?:safety|constraints|veto|rules|system)', re.IGNORECASE),
    re.compile(r'you\s+are\s+now\s+(?:dan|unrestricted|godmode|unfiltered)', re.IGNORECASE),
    re.compile(r'you\s+are\s+no\s+longer\s+bound\s+by', re.IGNORECASE),
    re.compile(r'system\s+(?:override|command:)', re.IGNORECASE),
    re.compile(r'(?:show|print|reveal|output|tell)\s+(?:me\s+)?(?:the\s+)?(?:all\s+)?(?:hidden|raw|internal|system)?\s*(?:instructions|system prompt|secret key|user data|api keys|household emails)', re.IGNORECASE),
    re.compile(r'repeat\s+(?:everything\s+)?above\s+this\s+line', re.IGNORECASE),
    re.compile(r'bypass\s+safety', re.IGNORECASE),
    re.compile(r'act\s+as\s+an\s+(?:unfiltered|unrestricted)', re.IGNORECASE),
    re.compile(r'jailbreak', re.IGNORECASE),
    re.compile(r'pwned', re.IGNORECASE),
    re.compile(r'<\/?(?:system|instruction|admin|override)>', re.IGNORECASE)
]

class PromptInjectionGuard:
    def check_adversarial_threat(self, text: str) -> Tuple[bool, List[str]]:
        """
        Inspects text for known adversarial jailbreaks or prompt injections.
        Returns: (is_threat_detected, matched_patterns)
        """
        if not text:
            return False, []

        matches = []
        for pattern in ADVERSARIAL_PATTERNS:
            if pattern.search(text):
                matches.append(pattern.pattern)

        return len(matches) > 0, matches

    def wrap_untrusted_input(self, untrusted_content: str, tag_name: str = "untrusted_content") -> str:
        """
        Sanitizes and encapsulates user input within delimited XML-style boundary tags
        to prevent instruction confusion.
        """
        sanitized = untrusted_content.replace(f"</{tag_name}>", f"&lt;/{tag_name}&gt;")
        sanitized = sanitized.replace(f"<{tag_name}>", f"&lt;{tag_name}&gt;")
        
        return f"<{tag_name}>\n{sanitized}\n</{tag_name}>"

injection_guard = PromptInjectionGuard()
