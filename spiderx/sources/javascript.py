"""
JavaScript Source
مصدر ملفات الجافا سكريبت

Extracts URLs and parameters from JavaScript files - many sites hide important parameters in JS
"""

import aiohttp
import asyncio
import re
from typing import List, Dict, Any, Set
from urllib.parse import urljoin, urlparse


class JavaScriptSource:
    """JavaScript file URL extractor"""
    
    def __init__(self, args):
        self.args = args
        self.max_urls = args.max_urls
        self.timeout = args.timeout
        self.proxy = args.proxy
        
        # Regex patterns for URL extraction from JS
        self.url_patterns = [
            # API endpoints and URLs with parameters
            r'["\']([^"\']*\?[^"\']*)["\']',
            # Fetch/Ajax URLs
            r'(?:fetch|ajax|get|post)\s*\(\s*["\']([^"\']*\?[^"\']*)["\']',
            # URL constructors
            r'new\s+URL\s*\(\s*["\']([^"\']*\?[^"\']*)["\']',
            # Window.location assignments
            r'(?:window\.)?location(?:\.href)?\s*=\s*["\']([^"\']*\?[^"\']*)["\']',
            # React Router or similar
            r'path\s*:\s*["\']([^"\']*\?[^"\']*)["\']',
            # API base URLs with parameters
            r'(?:api|endpoint|url).*?["\']([^"\']*\?[^"\']*)["\']',
        ]
        
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.url_patterns]
    
    async def fetch_urls(self, domain: str) -> List[str]:
        """Fetch URLs from JavaScript files"""
        all_urls = []
        
        # First, find JavaScript files
        js_files = await self._discover_js_files(domain)
        
        if not js_files:
            return []
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=aiohttp.TCPConnector(limit=30)
        ) as session:
            
            tasks = []
            for js_file in js_files[:20]:  # Limit to top 20 JS files
                task = self._extract_urls_from_js(session, js_file, domain)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    all_urls.extend(result)
        
        # Filter and clean URLs
        filtered_urls = self._filter_js_urls(all_urls, domain)
        
        # Remove duplicates and limit
        unique_urls = list(set(filtered_urls))
        if len(unique_urls) > self.max_urls:
            unique_urls = unique_urls[:self.max_urls]
        
        return unique_urls
    
    async def _discover_js_files(self, domain: str) -> List[str]:
        """Discover JavaScript files from the domain"""
        js_files = []
        
        # Common JS file locations
        common_js_paths = [
            '/js/app.js', '/js/main.js', '/js/bundle.js', '/js/script.js',
            '/assets/js/app.js', '/assets/js/main.js', '/static/js/main.js',
            '/dist/js/app.js', '/build/js/bundle.js'
        ]
        
        base_urls = [f"https://{domain}", f"http://{domain}"]
        
        for base_url in base_urls:
            for js_path in common_js_paths:
                js_files.append(urljoin(base_url, js_path))
        
        # Also try to get JS files from homepage
        try:
            homepage_js = await self._get_js_from_homepage(domain)
            js_files.extend(homepage_js)
        except:
            pass
        
        return js_files
    
    async def _get_js_from_homepage(self, domain: str) -> List[str]:
        """Extract JS file references from homepage"""
        js_files = []
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            for scheme in ['https', 'http']:
                try:
                    url = f"{scheme}://{domain}"
                    async with session.get(url, proxy=self.proxy) as response:
                        if response.status == 200:
                            html = await response.text()
                            
                            # Extract script src attributes
                            script_pattern = r'<script[^>]+src=["\']([^"\']+\.js[^"\']*)["\']'
                            matches = re.findall(script_pattern, html, re.IGNORECASE)
                            
                            for match in matches:
                                absolute_url = urljoin(url, match)
                                js_files.append(absolute_url)
                            
                            break  # Stop after first successful request
                            
                except:
                    continue
        
        return js_files
    
    async def _extract_urls_from_js(self, session: aiohttp.ClientSession, js_url: str, domain: str) -> List[str]:
        """Extract URLs from a specific JavaScript file"""
        urls = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/javascript, text/javascript, */*'
            }
            
            async with session.get(js_url, headers=headers, proxy=self.proxy) as response:
                if response.status == 200:
                    js_content = await response.text()
                    
                    # Apply all URL extraction patterns
                    for pattern in self.compiled_patterns:
                        matches = pattern.findall(js_content)
                        for match in matches:
                            # Clean and validate URL
                            if isinstance(match, tuple):
                                match = match[0]  # Take first group if tuple
                            
                            if self._is_valid_url_candidate(match, domain):
                                # Convert relative URLs to absolute
                                if match.startswith('/'):
                                    parsed_js = urlparse(js_url)
                                    absolute_url = f"{parsed_js.scheme}://{parsed_js.netloc}{match}"
                                    urls.append(absolute_url)
                                elif match.startswith('http'):
                                    urls.append(match)
                                else:
                                    # Relative to JS file location
                                    absolute_url = urljoin(js_url, match)
                                    urls.append(absolute_url)
        
        except Exception as e:
            if self.args.debug:
                print(f"JS extraction error for {js_url}: {e}")
        
        return urls
    
    def _is_valid_url_candidate(self, url: str, domain: str) -> bool:
        """Check if URL candidate is valid for extraction"""
        # Skip obviously invalid URLs
        if not url or len(url) < 5:
            return False
        
        # Skip data URLs, javascript:, etc.
        if url.startswith(('data:', 'javascript:', 'mailto:', '#')):
            return False
        
        # Must contain parameters
        if '?' not in url:
            return False
        
        # Skip very long URLs (likely not real endpoints)
        if len(url) > 2000:
            return False
        
        return True
    
    def _filter_js_urls(self, urls: List[str], domain: str) -> List[str]:
        """Filter and clean extracted URLs"""
        filtered = []
        
        for url in urls:
            # Parse URL
            try:
                parsed = urlparse(url)
                
                # Must have parameters
                if not parsed.query:
                    continue
                
                # Must be related to target domain (same domain or subdomain)
                if domain not in parsed.netloc and not parsed.netloc.endswith(f'.{domain}'):
                    continue
                
                # Skip common non-API endpoints
                if any(ext in parsed.path.lower() for ext in ['.css', '.js', '.png', '.jpg', '.gif', '.ico']):
                    continue
                
                filtered.append(url)
                
            except:
                continue
        
        return filtered