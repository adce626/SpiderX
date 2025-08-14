"""
SpiderX Data Sources Module
وحدة مصادر البيانات للأداة الأسطورية

Modular data source implementations for comprehensive URL discovery
"""

from .manager import SourceManager
from .wayback import WaybackSource
from .sitemap import SitemapSource
from .javascript import JavaScriptSource
from .crawler import CrawlerSource

__all__ = [
    'SourceManager',
    'WaybackSource', 
    'SitemapSource',
    'JavaScriptSource',
    'CrawlerSource'
]