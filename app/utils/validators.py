"""URL validation utilities including scheme verification and SSRF protection."""

import ipaddress
import socket
from urllib.parse import urlparse
from typing import Tuple

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

# Disallowed schemes (explicitly rejected)
DISALLOWED_SCHEMES = {"file", "javascript", "data", "gopher", "ftp", "php", "dict"}

# Hostnames explicitly blocked
BLOCKED_HOSTNAMES = {
    "localhost",
    "localhost.localdomain",
    "loopback",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
}


def is_private_ip(ip_str: str) -> bool:
    """Check if an IP string is private, loopback, link-local, or reserved."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        )
    except ValueError:
        return False


def is_ssrf_safe(hostname: str) -> bool:
    """Verify that a hostname does not resolve to private or loopback IP addresses."""
    if not hostname:
        return False

    clean_host = hostname.lower().strip()

    if clean_host in BLOCKED_HOSTNAMES or clean_host.endswith(".local") or clean_host.endswith(".internal"):
        return False

    # Check if host itself is an IP address
    if is_private_ip(clean_host):
        return False

    # Perform DNS resolution check
    try:
        addr_info = socket.getaddrinfo(clean_host, None)
        for family, _, _, _, sockaddr in addr_info:
            ip_str = sockaddr[0]
            if is_private_ip(ip_str):
                return False
    except (socket.gaierror, socket.error):
        # If DNS resolution fails, allow yt-dlp to handle or fail gracefully,
        # but do not bypass IP checks if resolved.
        pass

    return True


def validate_download_url(url: str) -> Tuple[bool, str]:
    """Validate a URL for download suitability and safety.

    Args:
        url: The URL string to validate.

    Returns:
        Tuple of (is_valid: bool, reason: str).
    """
    if not url:
        return False, "URL is empty."

    try:
        parsed = urlparse(url)
    except Exception:
        return False, "Malformed URL format."

    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        if parsed.scheme and parsed.scheme.lower() in DISALLOWED_SCHEMES:
            return False, f"Unsupported scheme: {parsed.scheme}://"
        return False, "Only HTTP and HTTPS links are supported."

    if not parsed.netloc:
        return False, "URL missing domain/hostname."

    # Remove port if present for hostname check
    hostname = parsed.hostname or parsed.netloc.split(":")[0]

    if not is_ssrf_safe(hostname):
        return False, "URL targets a private, internal, or restricted host."

    return True, "URL is valid."
