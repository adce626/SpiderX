"""
Live Crawler Source
مصدر الزحف المباشر

Simple crawling of live website pages to discover URLs with parameters
"""

import aiohttp
import asyncio
import re
from typing import List, Dict, Any, Set
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup


class CrawlerSource:
    """Simple live crawler for URL discovery"""
    
    def __init__(self, args):
        self.args = args
        self.max_urls = min(args.max_urls, 1000)  # Limit crawling
        self.timeout = args.timeout
        self.proxy = args.proxy
        self.max_depth = getattr(args, 'crawl_depth', 2)
        self.max_pages = getattr(args, 'crawl_pages', 20)
        
        self.visited_urls: Set[str] = set()
        self.discovered_urls: List[str] = []
    
    async def fetch_urls(self, domain: str) -> List[str]:
        """Crawl the domain for URLs with parameters"""
        if not hasattr(self.args, 'crawl_pages') or self.args.crawl_pages <= 0:
            return []  # Crawling disabled
        
        # Start with homepage and common entry points
        start_urls = [
            f"https://{domain}",
            f"https://{domain}/search",
            f"https://{domain}/products",
            f"https://{domain}/shop",
            f"https://{domain}/category",
            f"https://{domain}/api",
        ]
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=aiohttp.TCPConnector(limit=10)
        ) as session:
            
            # Crawl starting from each entry point
            for start_url in start_urls:
                if len(self.visited_urls) >= self.max_pages:
                    break
                
                await self._crawl_recursive(session, start_url, domain, 0)
        
        # Filter URLs with parameters
        param_urls = [url for url in self.discovered_urls if '?' in url]
        
        # Remove duplicates and limit
        unique_urls = list(set(param_urls))
        if len(unique_urls) > self.max_urls:
            unique_urls = unique_urls[:self.max_urls]
        
        return unique_urls
    
    async def _crawl_recursive(self, session: aiohttp.ClientSession, url: str, domain: str, depth: int):
        """Recursively crawl pages"""
        if depth > self.max_depth or len(self.visited_urls) >= self.max_pages:
            return
        
        if url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            async with session.get(url, headers=headers, proxy=self.proxy) as response:
                if response.status == 200 and 'text/html' in response.headers.get('content-type', ''):
                    html = await response.text()
                    
                    # Extract URLs from this page
                    page_urls = self._extract_urls_from_html(html, url, domain)
                    self.discovered_urls.extend(page_urls)
                    
                    # Get links for deeper crawling
                    if depth < self.max_depth:
                        soup = BeautifulSoup(html, 'html.parser')
                        links = soup.find_all('a', href=True)
                        
                        crawl_tasks = []
                        for link in links[:10]:  # Limit links per page
                            href = link.get('href', '')
                            absolute_url = urljoin(url, href)
                            
                            # Only crawl same domain
                            if self._is_same_domain(absolute_url, domain):
                                if len(self.visited_urls) < self.max_pages:
                                    task = self._crawl_recursive(session, absolute_url, domain, depth + 1)
                                    crawl_tasks.append(task)
                        
                        if crawl_tasks:
                            await asyncio.gather(*crawl_tasks, return_exceptions=True)
        
        except Exception as e:
            if self.args.debug:
                print(f"Crawl error for {url}: {e}")
    
    def _extract_urls_from_html(self, html: str, base_url: str, domain: str) -> List[str]:
        """Extract URLs with parameters from HTML"""
        urls = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract from various HTML elements
            selectors = [
                'a[href*="?"]',  # Links with parameters
                'form[action*="?"]',  # Forms with parameters
                'iframe[src*="?"]',  # Iframes with parameters
                'img[src*="?"]',  # Images with parameters (sometimes API endpoints)
                'script[src*="?"]',  # Scripts with parameters
                'link[href*="?"]'  # CSS/other resources with parameters
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    attr = 'href' if element.name in ['a', 'link'] else 'src' if element.name in ['img', 'script', 'iframe'] else 'action'
                    url = element.get(attr)
                    
                    if url:
                        absolute_url = urljoin(base_url, url)
                        if self._is_valid_crawl_url(absolute_url, domain):
                            urls.append(absolute_url)
            
            # Also extract URLs from JavaScript in script tags
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string:
                    js_urls = self._extract_urls_from_js_snippet(script.string, base_url, domain)
                    urls.extend(js_urls)
        
        except Exception as e:
            if self.args.debug:
                print(f"HTML parsing error: {e}")
        
        return urls
    
    def _extract_urls_from_js_snippet(self, js_code: str, base_url: str, domain: str) -> List[str]:
        """Extract URLs from JavaScript code snippets"""
        urls = []
        
        # Simple regex patterns for URLs in JS
        patterns = [
            r'["\']([^"\']*\?[^"\']*)["\']',  # Quoted URLs with parameters
            r'url\s*[:=]\s*["\']([^"\']*\?[^"\']*)["\']',  # url: "..." patterns
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, js_code, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                
                absolute_url = urljoin(base_url, match)
                if self._is_valid_crawl_url(absolute_url, domain):
                    urls.append(absolute_url)
        
        return urls
    
    def _is_same_domain(self, url: str, domain: str) -> bool:
        """Check if URL belongs to the same domain"""
        try:
            parsed = urlparse(url)
            return parsed.netloc == domain or parsed.netloc.endswith(f'.{domain}')
        except:
            return False
    
    def _is_valid_crawl_url(self, url: str, domain: str) -> bool:
        """Check if URL is valid for crawling"""
        try:
            parsed = urlparse(url)
            
            # Must have parameters
            if not parsed.query:
                return False
            
            # Must be same domain
            if not self._is_same_domain(url, domain):
                return False
            
            # Skip obvious static files
            if any(parsed.path.lower().endswith(ext) for ext in ['.css', '.js', '.png', '.jpg', '.gif', '.ico', '.pdf']):
                return False
            
            # Skip very long URLs
            if len(url) > 2000:
                return False
            
            return True
            
        except:
            return False