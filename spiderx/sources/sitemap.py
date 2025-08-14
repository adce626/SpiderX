"""
Sitemap Source
مصدر خريطة الموقع

Fetches URLs from sitemap.xml files with recursive sitemap discovery
"""

import aiohttp
import asyncio
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Set
from urllib.parse import urljoin, urlparse


class SitemapSource:
    """Sitemap.xml URL source with recursive discovery"""
    
    def __init__(self, args):
        self.args = args
        self.max_urls = args.max_urls
        self.timeout = args.timeout
        self.proxy = args.proxy
        self.discovered_sitemaps: Set[str] = set()
    
    async def fetch_urls(self, domain: str) -> List[str]:
        """Fetch URLs from sitemap files"""
        all_urls = []
        
        # Common sitemap locations
        sitemap_urls = [
            f"https://{domain}/sitemap.xml",
            f"https://{domain}/sitemap_index.xml",
            f"https://{domain}/sitemaps.xml",
            f"https://{domain}/sitemap/",
            f"http://{domain}/sitemap.xml",
            f"http://{domain}/robots.txt"  # Check robots.txt for sitemap references
        ]
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=aiohttp.TCPConnector(limit=50)
        ) as session:
            
            # First, get sitemaps from robots.txt
            robots_sitemaps = await self._get_sitemaps_from_robots(session, domain)
            sitemap_urls.extend(robots_sitemaps)
            
            # Process all sitemap URLs
            tasks = []
            for sitemap_url in set(sitemap_urls):  # Remove duplicates
                if sitemap_url not in self.discovered_sitemaps:
                    self.discovered_sitemaps.add(sitemap_url)
                    task = self._process_sitemap(session, sitemap_url, domain)
                    tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    all_urls.extend(result)
        
        # Remove duplicates and limit
        unique_urls = list(set(all_urls))
        if len(unique_urls) > self.max_urls:
            unique_urls = unique_urls[:self.max_urls]
        
        return unique_urls
    
    async def _get_sitemaps_from_robots(self, session: aiohttp.ClientSession, domain: str) -> List[str]:
        """Extract sitemap URLs from robots.txt"""
        sitemaps = []
        robots_urls = [f"https://{domain}/robots.txt", f"http://{domain}/robots.txt"]
        
        for robots_url in robots_urls:
            try:
                async with session.get(robots_url, proxy=self.proxy) as response:
                    if response.status == 200:
                        text = await response.text()
                        for line in text.split('\n'):
                            if line.lower().startswith('sitemap:'):
                                sitemap_url = line.split(':', 1)[1].strip()
                                sitemaps.append(sitemap_url)
                        break  # Stop after first successful robots.txt
            except:
                continue
        
        return sitemaps
    
    async def _process_sitemap(self, session: aiohttp.ClientSession, sitemap_url: str, domain: str) -> List[str]:
        """Process a single sitemap file"""
        urls = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with session.get(sitemap_url, headers=headers, proxy=self.proxy) as response:
                if response.status == 200:
                    content = await response.text()
                    urls = self._parse_sitemap_content(content, domain)
                    
        except Exception as e:
            if self.args.debug:
                print(f"Sitemap error for {sitemap_url}: {e}")
        
        return urls
    
    def _parse_sitemap_content(self, content: str, domain: str) -> List[str]:
        """Parse sitemap XML content"""
        urls = []
        
        try:
            root = ET.fromstring(content)
            
            # Handle sitemap index files
            for sitemap in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                loc_elem = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc_elem is not None and loc_elem.text:
                    # TODO: Recursively process nested sitemaps
                    pass
            
            # Handle regular sitemap files
            for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc_elem = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc_elem is not None and loc_elem.text:
                    url_str = loc_elem.text.strip()
                    # Only include URLs with parameters
                    if '?' in url_str and domain in url_str:
                        urls.append(url_str)
            
        except ET.ParseError:
            # Try to parse as plain text (some sitemaps are just URL lists)
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('http') and '?' in line and domain in line:
                    urls.append(line)
        
        return urls