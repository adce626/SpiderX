"""
Smart Crawler Module
زاحف ذكي متطور

Advanced crawling with intelligent page discovery - LEGENDARY FEATURE  
"""

import asyncio
import aiohttp
import re
from typing import List, Set, Dict, Optional
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
from .utils import get_random_user_agent, has_extension, smart_rate_limit, validate_url


class SmartCrawler:
    """Intelligent crawler that finds hidden parameters"""
    
    def __init__(self, args):
        self.args = args
        self.crawled_urls: Set[str] = set()
        self.found_params: Set[str] = set()
        self.request_count = 0
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Smart crawling patterns
        self.priority_paths = [
            '/search', '/api', '/admin', '/user', '/profile', '/login',
            '/dashboard', '/settings', '/config', '/panel', '/manage'
        ]
        
        # Parameter extraction patterns
        self.js_param_patterns = [
            r'[\'""](\w+)[\'""]\s*:\s*[\'""]?[^\'""]*[\'""]?',  # JSON-like
            r'\.(\w+)\s*=',  # Property assignment
            r'[\[\.](\w+)[\]\.]',  # Array/object access
            r'data-(\w+)',  # Data attributes
            r'name=[\'"""](\w+)[\'"""]',  # Form names
        ]
        
        # Form detection patterns
        self.form_patterns = [
            r'<form[^>]*>.*?</form>',
            r'<input[^>]*name=[\'"""](\w+)[\'"""]',
            r'<select[^>]*name=[\'"""](\w+)[\'"""]',
            r'<textarea[^>]*name=[\'"""](\w+)[\'"""]'
        ]
    
    async def smart_crawl(self, domain: str) -> List[str]:
        """Smart crawling with priority-based discovery"""
        found_urls = []
        
        try:
            timeout = aiohttp.ClientTimeout(total=self.args.timeout)
            connector = aiohttp.TCPConnector(limit=20, limit_per_host=10)
            
            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                self.session = session
                
                # Start with domain root
                base_url = f"https://{domain}"
                initial_urls = await self._discover_initial_urls(base_url)
                
                # Priority crawling
                priority_urls = self._prioritize_urls(initial_urls)
                
                # Crawl priority URLs
                crawl_tasks = []
                for url in priority_urls[:self.args.crawl_pages]:
                    if url not in self.crawled_urls:
                        task = self._crawl_url_smart(url, domain)
                        crawl_tasks.append(task)
                
                if crawl_tasks:
                    results = await asyncio.gather(*crawl_tasks, return_exceptions=True)
                    
                    for result in results:
                        if isinstance(result, list):
                            found_urls.extend(result)
        
        except Exception as e:
            if self.args.debug:
                print(f"Smart crawl error for {domain}: {e}")
        
        return found_urls
    
    async def _discover_initial_urls(self, base_url: str) -> List[str]:
        """Discover initial URLs from multiple sources"""
        urls = set()
        
        try:
            # Try robots.txt
            robots_urls = await self._check_robots_txt(base_url)
            urls.update(robots_urls)
            
            # Try sitemap.xml  
            sitemap_urls = await self._check_sitemap(base_url)
            urls.update(sitemap_urls)
            
            # Try common paths
            common_urls = self._generate_common_paths(base_url)
            urls.update(common_urls)
            
            # Crawl main page
            main_page_urls = await self._crawl_main_page(base_url)
            urls.update(main_page_urls)
            
        except Exception as e:
            if self.args.debug:
                print(f"Initial discovery error: {e}")
        
        return list(urls)
    
    async def _check_robots_txt(self, base_url: str) -> List[str]:
        """Extract URLs from robots.txt"""
        urls = []
        
        try:
            robots_url = urljoin(base_url, '/robots.txt')
            headers = {"User-Agent": get_random_user_agent()}
            
            async with self.session.get(robots_url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Extract disallowed paths (often interesting)
                    disallow_pattern = r'Disallow:\s*([^\s]+)'
                    matches = re.findall(disallow_pattern, content, re.IGNORECASE)
                    
                    for path in matches:
                        if path != '/' and '?' in path:  # Only paths with parameters
                            full_url = urljoin(base_url, path)
                            if validate_url(full_url):
                                urls.append(full_url)
        
        except Exception:
            pass
        
        return urls
    
    async def _check_sitemap(self, base_url: str) -> List[str]:
        """Extract URLs from sitemap.xml"""
        urls = []
        
        try:
            sitemap_urls = [
                urljoin(base_url, '/sitemap.xml'),
                urljoin(base_url, '/sitemap_index.xml'),
                urljoin(base_url, '/sitemap.txt')
            ]
            
            for sitemap_url in sitemap_urls:
                try:
                    headers = {"User-Agent": get_random_user_agent()}
                    
                    async with self.session.get(sitemap_url, headers=headers) as response:
                        if response.status == 200:
                            content = await response.text()
                            
                            # Extract URLs with parameters
                            url_pattern = r'<loc>(.*?)</loc>'
                            matches = re.findall(url_pattern, content)
                            
                            for url in matches:
                                if '?' in url and validate_url(url):
                                    urls.append(url)
                
                except Exception:
                    continue
        
        except Exception:
            pass
        
        return urls
    
    def _generate_common_paths(self, base_url: str) -> List[str]:
        """Generate common paths that might have parameters"""
        urls = []
        
        for path in self.priority_paths:
            # Try with common parameters
            common_params = [
                '?id=1', '?search=test', '?q=test', '?page=1',
                '?user=1', '?category=1', '?type=1'
            ]
            
            for param in common_params:
                url = urljoin(base_url, path + param)
                if validate_url(url):
                    urls.append(url)
        
        return urls
    
    async def _crawl_main_page(self, base_url: str) -> List[str]:
        """Crawl main page for links and forms"""
        urls = []
        
        try:
            headers = {"User-Agent": get_random_user_agent()}
            
            async with self.session.get(base_url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract links with parameters
                    links = soup.find_all('a', href=True)
                    for link in links:
                        href = link['href']
                        if '?' in href:
                            full_url = urljoin(base_url, href)
                            if validate_url(full_url):
                                urls.append(full_url)
                    
                    # Extract form actions
                    forms = soup.find_all('form', action=True)
                    for form in forms:
                        action = form['action']
                        if action and not action.startswith('#'):
                            full_url = urljoin(base_url, action)
                            if validate_url(full_url):
                                # Add common parameters to form actions
                                urls.append(full_url + '?test=1')
        
        except Exception:
            pass
        
        return urls
    
    def _prioritize_urls(self, urls: List[str]) -> List[str]:
        """Prioritize URLs based on potential value"""
        scored_urls = []
        
        for url in urls:
            score = 0
            url_lower = url.lower()
            
            # Priority path bonus
            for priority_path in self.priority_paths:
                if priority_path in url_lower:
                    score += 10
                    break
            
            # Parameter count bonus
            try:
                parsed = urlparse(url)
                params = parse_qs(parsed.query)
                score += len(params) * 2
            except Exception:
                pass
            
            # Interesting parameter names
            interesting_params = ['search', 'id', 'user', 'admin', 'key', 'token']
            for param in interesting_params:
                if param in url_lower:
                    score += 5
            
            # Avoid static files
            if has_extension(url):
                score -= 10
            
            scored_urls.append((url, score))
        
        # Sort by score descending
        scored_urls.sort(key=lambda x: x[1], reverse=True)
        return [url for url, score in scored_urls]
    
    async def _crawl_url_smart(self, url: str, domain: str) -> List[str]:
        """Smart crawling of individual URL"""
        if url in self.crawled_urls:
            return []
        
        self.crawled_urls.add(url)
        found_urls = []
        
        try:
            # Smart rate limiting
            if self.request_count > 0:
                delay = smart_rate_limit(domain, self.request_count)
                await asyncio.sleep(delay)
            
            self.request_count += 1
            headers = {"User-Agent": get_random_user_agent()}
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Extract URLs from content
                    extracted_urls = self._extract_urls_from_content(content, url)
                    found_urls.extend(extracted_urls)
                    
                    # Extract parameters from JavaScript
                    js_params = self._extract_js_parameters(content)
                    self.found_params.update(js_params)
                    
                    # Create URLs with found parameters
                    base_url = url.split('?')[0]
                    for param in js_params:
                        param_url = f"{base_url}?{param}=FUZZ"
                        found_urls.append(param_url)
        
        except Exception as e:
            if self.args.debug:
                print(f"Error crawling {url}: {e}")
        
        return found_urls
    
    def _extract_urls_from_content(self, content: str, base_url: str) -> List[str]:
        """Extract URLs from HTML content"""
        urls = []
        
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Links with parameters
            links = soup.find_all('a', href=True)
            for link in links[:20]:  # Limit to avoid too many URLs
                href = link['href']
                if '?' in href:
                    full_url = urljoin(base_url, href)
                    if validate_url(full_url) and not has_extension(full_url):
                        urls.append(full_url)
            
            # Form actions with method GET
            forms = soup.find_all('form')
            for form in forms:
                method = form.get('method', 'get').lower()
                action = form.get('action', '')
                
                if method == 'get' and action:
                    full_url = urljoin(base_url, action)
                    if validate_url(full_url):
                        # Extract input names as parameters
                        inputs = form.find_all(['input', 'select', 'textarea'])
                        params = []
                        for inp in inputs:
                            name = inp.get('name')
                            if name and name not in ['submit', 'reset']:
                                params.append(f"{name}=FUZZ")
                        
                        if params:
                            param_string = '&'.join(params)
                            param_url = f"{full_url}?{param_string}"
                            urls.append(param_url)
        
        except Exception:
            pass
        
        return urls
    
    def _extract_js_parameters(self, content: str) -> Set[str]:
        """Extract potential parameters from JavaScript code"""
        params = set()
        
        try:
            # Extract script content
            soup = BeautifulSoup(content, 'html.parser')
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string:
                    js_code = script.string
                    
                    # Apply parameter extraction patterns
                    for pattern in self.js_param_patterns:
                        matches = re.findall(pattern, js_code, re.IGNORECASE)
                        for match in matches:
                            if isinstance(match, tuple):
                                match = match[0]
                            
                            # Filter out common non-parameter words
                            if (len(match) > 2 and 
                                match.isalnum() and 
                                not match.isdigit() and
                                match.lower() not in ['var', 'let', 'const', 'function', 'return', 'true', 'false']):
                                params.add(match)
        
        except Exception:
            pass
        
        return params
    
    def get_crawl_statistics(self) -> Dict:
        """Get crawling statistics"""
        return {
            'urls_crawled': len(self.crawled_urls),
            'parameters_found': len(self.found_params),
            'requests_made': self.request_count,
            'unique_parameters': list(self.found_params)
        }