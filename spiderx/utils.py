"""
Utility Functions

Common utilities for logging, progress tracking, and formatting
"""

import logging
import sys
import time
import random
import re
from typing import List, Dict, Set
from urllib.parse import urlparse, parse_qs
from tqdm import tqdm
from colorama import Fore, Style, init


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
    ║          Legendary Parameter Discovery & Analysis             ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print("    🕷️  Legendary URL parameter discovery with multiple sources")
    print("    🎯  Intelligent filtering and comprehensive analysis")
    print("    ⚡  High-performance async processing")
    print("")

# Initialize colorama
init(autoreset=True)

def get_user_agents() -> List[str]:
    """Get a list of realistic user agents for web requests"""
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]

def get_random_user_agent() -> str:
    """Get a random user agent"""
    return random.choice(get_user_agents())

def clean_url(url: str) -> str:
    """Clean URL by removing redundant port information"""
    try:
        parsed = urlparse(url)
        if (parsed.port == 80 and parsed.scheme == "http") or (parsed.port == 443 and parsed.scheme == "https"):
            netloc = parsed.netloc.rsplit(":", 1)[0]
            parsed = parsed._replace(netloc=netloc)
        return parsed.geturl()
    except Exception:
        return url

def has_extension(url: str, extensions: List[str] = None) -> bool:
    """Check if URL has a file extension"""
    if extensions is None:
        extensions = [
            ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", ".json",
            ".css", ".js", ".webp", ".woff", ".woff2", ".eot", ".ttf", 
            ".otf", ".mp4", ".mp3", ".avi", ".mov", ".txt", ".xml", ".ico",
            ".zip", ".rar", ".tar", ".gz", ".doc", ".docx", ".xls", ".xlsx"
        ]
    
    try:
        parsed = urlparse(url)
        path = parsed.path.lower()
        return any(path.endswith(ext) for ext in extensions)
    except Exception:
        return False

def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return url

def is_same_domain(url1: str, url2: str) -> bool:
    """Check if two URLs are from the same domain"""
    return extract_domain(url1) == extract_domain(url2)

def validate_url(url: str) -> bool:
    """Validate if URL is properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def detect_potential_vulnerability_params(params: Set[str]) -> Dict[str, List[str]]:
    """Detect parameters that might indicate vulnerabilities - LEGENDARY FEATURE"""
    vuln_patterns = {
        'xss_potential': ['search', 'query', 'q', 'keyword', 'term', 'input', 'data', 'content', 'msg', 'message'],
        'sqli_potential': ['id', 'uid', 'user_id', 'product_id', 'item_id', 'post_id', 'page_id', 'category_id'],
        'lfi_potential': ['file', 'path', 'page', 'include', 'template', 'view', 'load', 'read'],
        'redirect_potential': ['url', 'redirect', 'next', 'return', 'continue', 'goto', 'target', 'dest'],
        'api_potential': ['key', 'token', 'api_key', 'access_token', 'auth', 'secret', 'password'],
        'debug_potential': ['debug', 'test', 'dev', 'admin', 'trace', 'verbose', 'log']
    }
    
    found_vulns = {}
    for vuln_type, patterns in vuln_patterns.items():
        matches = []
        for param in params:
            param_lower = param.lower()
            for pattern in patterns:
                if pattern in param_lower or param_lower.startswith(pattern):
                    matches.append(param)
                    break
        if matches:
            found_vulns[vuln_type] = matches
    
    return found_vulns

def analyze_parameter_complexity(params: Set[str]) -> Dict[str, int]:
    """Analyze parameter complexity for fuzzing priority - LEGENDARY FEATURE"""
    complexity_scores = {}
    
    for param in params:
        score = 0
        param_lower = param.lower()
        
        # Length bonus
        if len(param) > 3:
            score += 1
        if len(param) > 6:
            score += 2
            
        # Complexity patterns
        if '_' in param or '-' in param:
            score += 2
        if any(char.isdigit() for char in param):
            score += 1
        if param.endswith('_id') or param.endswith('Id'):
            score += 3
        if any(keyword in param_lower for keyword in ['search', 'query', 'input', 'data']):
            score += 4
        if any(keyword in param_lower for keyword in ['admin', 'user', 'auth', 'key']):
            score += 5
            
        complexity_scores[param] = score
    
    return complexity_scores

def smart_rate_limit(domain: str, request_count: int) -> float:
    """Smart rate limiting based on domain and request count - LEGENDARY FEATURE"""
    # Base delay
    base_delay = 0.1
    
    # Popular domains get more aggressive rate limiting
    popular_domains = ['google.com', 'facebook.com', 'youtube.com', 'amazon.com', 'twitter.com']
    if any(pop_domain in domain for pop_domain in popular_domains):
        base_delay = 1.0
    
    # Increase delay based on request count
    if request_count > 100:
        base_delay *= 1.5
    if request_count > 500:
        base_delay *= 2.0
    if request_count > 1000:
        base_delay *= 3.0
    
    # Add some randomization to avoid detection
    return base_delay + random.uniform(0, base_delay * 0.5)



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