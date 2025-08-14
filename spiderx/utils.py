"""
Utility Functions
وظائف مساعدة للأداة الأسطورية

Common utilities for logging, progress tracking, and formatting
"""

import logging
import sys
import time
from typing import List
from tqdm import tqdm


def setup_logging(verbose: bool = False, debug: bool = False):
    """Setup logging configuration"""
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    else:
        level = logging.WARNING
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def print_banner():
    """Print SpiderX banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ███████╗██████╗ ██╗██████╗ ███████╗██████╗ ██╗  ██╗        ║
    ║   ██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗╚██╗██╔╝        ║
    ║   ███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝ ╚███╔╝         ║
    ║   ╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗ ██╔██╗         ║
    ║   ███████║██║     ██║██████╔╝███████╗██║  ██║██╔╝ ██╗        ║
    ║   ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝        ║
    ║                                                               ║
    ║           Advanced URL Parameter Mining Tool                  ║
    ║              الأداة الأسطورية لاستخراج المعاملات             ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print("    🕷️  Legendary URL parameter discovery with multiple sources")
    print("    🎯  Intelligent filtering and comprehensive analysis")
    print("    ⚡  High-performance async processing")
    print("")


def print_info(message: str):
    """Print info message with formatting"""
    print(f"[*] {message}")


def print_success(message: str):
    """Print success message with formatting"""
    print(f"[+] {message}")


def print_error(message: str):
    """Print error message with formatting"""
    print(f"[!] {message}")


def print_warning(message: str):
    """Print warning message with formatting"""
    print(f"[!] WARNING: {message}")


def format_time(seconds: float) -> str:
    """Format time duration"""
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}h {minutes}m {secs:.1f}s"


class ProgressBar:
    """Simple progress bar wrapper"""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.pbar = tqdm(total=total, desc=description, unit="items")
    
    def update(self, n: int = 1):
        """Update progress bar"""
        self.pbar.update(n)
    
    def set_description(self, desc: str):
        """Set description"""
        self.pbar.set_description(desc)
    
    def close(self):
        """Close progress bar"""
        self.pbar.close()


def clean_url(url: str) -> str:
    """Clean URL by removing redundant port information"""
    from urllib.parse import urlparse
    
    parsed_url = urlparse(url)
    
    if (parsed_url.port == 80 and parsed_url.scheme == "http") or \
       (parsed_url.port == 443 and parsed_url.scheme == "https"):
        parsed_url = parsed_url._replace(netloc=parsed_url.netloc.rsplit(":", 1)[0])

    return parsed_url.geturl()


def has_extension(url: str, extensions: List[str]) -> bool:
    """Check if URL has unwanted file extension"""
    import os
    from urllib.parse import urlparse
    
    parsed_url = urlparse(url)
    path = parsed_url.path
    extension = os.path.splitext(path)[1].lower()

    return extension in extensions


def is_valid_domain(domain: str) -> bool:
    """Validate domain format"""
    import re
    
    # Basic domain validation
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return re.match(pattern, domain) is not None


def normalize_url(url: str) -> str:
    """Normalize URL for comparison"""
    from urllib.parse import urlparse, urlunparse
    
    try:
        parsed = urlparse(url.lower())
        # Remove default ports
        netloc = parsed.netloc
        if (netloc.endswith(':80') and parsed.scheme == 'http') or \
           (netloc.endswith(':443') and parsed.scheme == 'https'):
            netloc = netloc.rsplit(':', 1)[0]
        
        # Remove trailing slash from path if it's just '/'
        path = parsed.path
        if path == '/':
            path = ''
        
        normalized = urlunparse((
            parsed.scheme,
            netloc,
            path,
            parsed.params,
            parsed.query,
            ''  # Remove fragment
        ))
        
        return normalized
    except:
        return url


def extract_domain_from_url(url: str) -> str:
    """Extract domain from URL"""
    from urllib.parse import urlparse
    
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return ""


def get_file_size_mb(filepath: str) -> float:
    """Get file size in MB"""
    try:
        import os
        size_bytes = os.path.getsize(filepath)
        return size_bytes / (1024 * 1024)
    except:
        return 0.0


def create_safe_filename(filename: str) -> str:
    """Create safe filename by removing invalid characters"""
    import re
    
    # Remove invalid characters
    safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing dots and spaces
    safe_filename = safe_filename.strip('. ')
    # Limit length
    if len(safe_filename) > 255:
        safe_filename = safe_filename[:255]
    
    return safe_filename


def validate_proxy_format(proxy: str) -> bool:
    """Validate proxy format"""
    if not proxy:
        return True
    
    # Basic proxy format validation
    import re
    pattern = r'^https?://[\w\.-]+:\d+$'
    return re.match(pattern, proxy) is not None