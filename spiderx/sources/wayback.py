"""
Wayback Machine Source
مصدر أرشيف الويب

Fetches URLs from Wayback Machine archives with enhanced capabilities
"""

import aiohttp
import asyncio
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse


class WaybackSource:
    """Wayback Machine URL source with advanced features"""
    
    def __init__(self, args):
        self.args = args
        self.max_urls = args.max_urls
        self.timeout = args.timeout
        self.proxy = args.proxy
    
    async def fetch_urls(self, domain: str) -> List[str]:
        """Fetch URLs from Wayback Machine"""
        urls = []
        
        # Multiple Wayback endpoints for better coverage
        endpoints = [
            f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=txt&collapse=urlkey&fl=original&page=/",
            f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=txt&collapse=urlkey&fl=original&page=/",
        ]
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=aiohttp.TCPConnector(limit=100)
        ) as session:
            
            tasks = []
            for endpoint in endpoints:
                task = self._fetch_from_endpoint(session, endpoint)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    urls.extend(result)
        
        # Remove duplicates and limit
        unique_urls = list(set(urls))
        if len(unique_urls) > self.max_urls:
            unique_urls = unique_urls[:self.max_urls]
        
        return unique_urls
    
    async def _fetch_from_endpoint(self, session: aiohttp.ClientSession, endpoint: str) -> List[str]:
        """Fetch URLs from a specific Wayback endpoint"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            proxy = self.proxy if self.proxy else None
            
            async with session.get(endpoint, headers=headers, proxy=proxy) as response:
                if response.status == 200:
                    text = await response.text()
                    urls = [line.strip() for line in text.split('\n') if line.strip()]
                    return urls
                else:
                    return []
                    
        except Exception as e:
            if self.args.debug:
                print(f"Wayback endpoint error: {e}")
            return []