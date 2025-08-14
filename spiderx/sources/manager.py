"""
Source Manager
مدير مصادر البيانات

Coordinates and manages different data sources for URL discovery
"""

import asyncio
from typing import List, Dict, Any

from .wayback import WaybackSource
from .sitemap import SitemapSource
from .javascript import JavaScriptSource
from .crawler import CrawlerSource


class SourceManager:
    """Manages all data sources for URL discovery"""
    
    def __init__(self, args):
        self.args = args
        self.sources = {
            'wayback': WaybackSource(args),
            'sitemap': SitemapSource(args),
            'js': JavaScriptSource(args),
            'crawl': CrawlerSource(args)
        }
    
    async def fetch_from_source(self, source_name: str, domain: str) -> List[Dict[str, Any]]:
        """Fetch URLs from a specific source"""
        if source_name not in self.sources:
            raise ValueError(f"Unknown source: {source_name}")
        
        source = self.sources[source_name]
        
        try:
            urls = await source.fetch_urls(domain)
            
            # Add metadata to each URL
            enriched_urls = []
            for url in urls:
                if isinstance(url, str):
                    url_data = {
                        'url': url,
                        'domain': domain,
                        'source': source_name
                    }
                else:
                    url_data = url
                    url_data.update({
                        'domain': domain,
                        'source': source_name
                    })
                
                enriched_urls.append(url_data)
            
            return enriched_urls
            
        except Exception as e:
            raise Exception(f"{source_name} source error: {str(e)}")
    
    async def fetch_from_all_sources(self, domain: str) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch URLs from all available sources"""
        results = {}
        
        tasks = []
        for source_name in self.sources.keys():
            task = asyncio.create_task(
                self.fetch_from_source(source_name, domain),
                name=f"{source_name}_{domain}"
            )
            tasks.append((source_name, task))
        
        for source_name, task in tasks:
            try:
                results[source_name] = await task
            except Exception as e:
                results[source_name] = []
                print(f"Warning: {source_name} failed for {domain}: {e}")
        
        return results