import os
import random
from urllib.parse import urlparse
from typing import List

def clean_url(url: str) -> str:
    """
    Clean the URL by removing redundant port information for HTTP and HTTPS URLs.
    
    Args:
        url (str): The URL to clean.
    
    Returns:
        str: Cleaned URL.
    """
    parsed_url = urlparse(url)
    
    if (parsed_url.port == 80 and parsed_url.scheme == "http") or \
       (parsed_url.port == 443 and parsed_url.scheme == "https"):
        parsed_url = parsed_url._replace(netloc=parsed_url.netloc.rsplit(":", 1)[0])

    return parsed_url.geturl()

def has_extension(url: str, extensions: List[str]) -> bool:
    """
    Check if the URL has a file extension matching any of the provided extensions.

    Args:
        url (str): The URL to check.
        extensions (list): List of file extensions to match against.

    Returns:
        bool: True if the URL has a matching extension, False otherwise.
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    extension = os.path.splitext(path)[1].lower()

    return extension in extensions

def get_user_agents() -> List[str]:
    """
    Get a list of user agents for web requests.
    
    Returns:
        List[str]: List of user agent strings.
    """
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
    ]

def get_random_user_agent() -> str:
    """Get a random user agent string."""
    return random.choice(get_user_agents())