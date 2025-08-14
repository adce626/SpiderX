#!/usr/bin/env python3
"""
SpiderX - Advanced URL Parameter Mining Tool
الأداة الأسطورية لاستخراج وتحليل معاملات URLs

A legendary tool that extracts URL parameters from multiple sources with intelligent filtering
"""

import argparse
import asyncio
import time
import sys
from pathlib import Path
from typing import List, Dict, Set
import json
from collections import Counter

from spiderx.cli_core import SpiderXCLI
from spiderx.sources import SourceManager
from spiderx.filters import ParameterFilter
from spiderx.exporters import ResultExporter
from spiderx.utils import setup_logging, print_banner, format_time

async def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="SpiderX - Advanced URL Parameter Mining Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  spiderx -d example.com                           # Single domain from all sources
  spiderx -l domains.txt                          # Multiple domains from file
  spiderx -d example.com --sources wayback,sitemap # Specific sources only
  spiderx -d example.com -o results.txt          # Save to custom file
  spiderx -d example.com --boring-list custom.txt # Custom boring parameters
  spiderx -d example.com --no-filter             # Disable filtering
  spiderx -d example.com --format json           # Export as JSON
  spiderx -d example.com --top-params 10         # Show top 10 parameters
  spiderx -i urls.txt                            # Import URLs from file
        """
    )
    
    # Target options
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument("-d", "--domain", help="Target domain")
    target_group.add_argument("-l", "--list", help="File containing list of domains")
    target_group.add_argument("-i", "--import-urls", help="Import URLs from file")
    
    # Source selection
    parser.add_argument("--sources", 
                       choices=["wayback", "sitemap", "js", "crawl", "all"],
                       default="all",
                       help="Data sources to use (default: all)")
    
    # Output options
    parser.add_argument("-o", "--output", help="Output file (default: results_<timestamp>.txt)")
    parser.add_argument("--format", choices=["txt", "csv", "json"], default="txt",
                       help="Output format (default: txt)")
    parser.add_argument("--no-save", action="store_true", help="Don't save to file, only print")
    
    # Filtering options
    parser.add_argument("--boring-list", help="File with boring parameters to filter")
    parser.add_argument("--no-filter", action="store_true", help="Disable parameter filtering")
    parser.add_argument("--custom-filter", nargs="+", help="Custom parameters to filter")
    
    # Advanced options
    parser.add_argument("--placeholder", default="FUZZ", help="Parameter placeholder (default: FUZZ)")
    parser.add_argument("--proxy", help="HTTP proxy (e.g., http://127.0.0.1:8080)")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout (default: 30)")
    parser.add_argument("--max-urls", type=int, default=10000, help="Max URLs per domain (default: 10000)")
    
    # Analysis options
    parser.add_argument("--top-params", type=int, help="Show top N most frequent parameters")
    parser.add_argument("--stats", action="store_true", help="Show detailed statistics")
    
    # Crawling options
    parser.add_argument("--crawl-depth", type=int, default=2, help="Crawling depth (default: 2)")
    parser.add_argument("--crawl-pages", type=int, default=20, help="Max pages to crawl (default: 20)")
    
    # Debug options
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose, args.debug)
    
    # Initialize SpiderX CLI
    spiderx = SpiderXCLI(args)
    
    try:
        # Execute the scan
        results = await spiderx.run()
        
        # Display results
        spiderx.display_results(results)
        
        # Export results if requested
        if not args.no_save:
            spiderx.export_results(results)
            
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())