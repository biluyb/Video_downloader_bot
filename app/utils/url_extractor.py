"""URL extraction utilities for extracting HTTP/HTTPS links from messages."""

import re
from typing import List, Optional

# Regex pattern for extracting HTTP/HTTPS URLs from plain text
URL_REGEX = re.compile(
    r"https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::\d+)?(?:/[^\s<>'\"`{}]*)?",
    re.IGNORECASE,
)


def extract_urls(text: str) -> List[str]:
    """Extract all HTTP/HTTPS URLs from text.

    Args:
        text: Input string (e.g. message text)

    Returns:
        List of URL strings found in text.
    """
    if not text:
        return []
    
    matches = URL_REGEX.findall(text)
    cleaned_urls: List[str] = []
    
    for url in matches:
        # Strip trailing punctuation often accidentally included in text
        url = url.rstrip(".,;:!?)>}]")
        if url and url not in cleaned_urls:
            cleaned_urls.append(url)
            
    return cleaned_urls


def find_first_url(text: str) -> Optional[str]:
    """Extract the first HTTP/HTTPS URL from text.

    Args:
        text: Input string.

    Returns:
        First URL string found or None.
    """
    urls = extract_urls(text)
    return urls[0] if urls else None
