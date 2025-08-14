#!/usr/bin/env python3
"""
Quick test script for SpiderX CLI
"""

import asyncio
import sys
from spiderx.sources.wayback import WaybackSource
from spiderx.filters import ParameterFilter
from spiderx.utils import print_banner, print_info, print_success, print_error

class SimpleArgs:
    def __init__(self):
        self.max_urls = 50
        self.timeout = 10
        self.proxy = None
        self.debug = True
        self.boring_list = None
        self.custom_filter = None
        self.no_filter = False

async def test_wayback():
    """Test Wayback Machine source"""
    print_info("Testing Wayback Machine source...")
    args = SimpleArgs()
    wayback = WaybackSource(args)
    
    try:
        urls = await wayback.fetch_urls("example.com")
        print_success(f"Found {len(urls)} URLs from Wayback Machine")
        
        # Show sample URLs with parameters
        param_urls = [url for url in urls if '?' in url]
        if param_urls:
            print_info(f"Sample URLs with parameters:")
            for url in param_urls[:5]:
                print(f"  {url}")
        else:
            print_info("No URLs with parameters found")
            
    except Exception as e:
        print_error(f"Wayback test failed: {e}")

def test_filter():
    """Test parameter filtering"""
    print_info("Testing parameter filtering...")
    args = SimpleArgs()
    filter_obj = ParameterFilter(args)
    
    test_urls = [
        "https://example.com/search?q=test&utm_source=google&ref=facebook",
        "https://example.com/product?id=123&category=books&session=abc123",
        "https://example.com/api?key=secret&format=json&callback=func"
    ]
    
    for url in test_urls:
        params = filter_obj.extract_parameters(url)
        filtered = filter_obj.filter_parameters(params)
        cleaned = filter_obj.create_cleaned_url(url, filtered, "FUZZ")
        
        print_info(f"Original: {url}")
        print_info(f"Parameters: {params}")
        print_info(f"Filtered: {filtered}")
        print_info(f"Cleaned: {cleaned}")
        print("")

async def main():
    print_banner()
    print_info("Running SpiderX tests...")
    print("")
    
    # Test filtering (synchronous)
    test_filter()
    
    # Test Wayback source (async)
    await test_wayback()
    
    print_success("All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())