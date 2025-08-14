#!/usr/bin/env python3
"""
SpiderX CLI Demo
عرض توضيحي للأداة الأسطورية

This demonstrates the full capabilities of SpiderX CLI tool
"""

import asyncio
import json
from collections import Counter

from spiderx.utils import print_banner, print_info, print_success, print_error
from spiderx.filters import ParameterFilter
from spiderx.exporters import ResultExporter


class DemoArgs:
    def __init__(self):
        self.max_urls = 100
        self.timeout = 30
        self.proxy = None
        self.debug = False
        self.boring_list = None
        self.custom_filter = None
        self.no_filter = False
        self.format = 'txt'
        self.output = 'demo_results.txt'
        self.stats = True


def create_demo_results():
    """Create comprehensive demo results"""
    # Simulate realistic URL discovery results
    demo_urls = [
        {
            'original_url': 'https://example.com/search?q=python&category=programming&utm_source=google',
            'cleaned_url': 'https://example.com/search?q=FUZZ&category=FUZZ',
            'domain': 'example.com',
            'source': 'wayback',
            'parameters': ['q', 'category'],
            'param_count': 2
        },
        {
            'original_url': 'https://example.com/api/users?id=123&format=json&key=secret',
            'cleaned_url': 'https://example.com/api/users?id=FUZZ&format=FUZZ&key=FUZZ',
            'domain': 'example.com', 
            'source': 'sitemap',
            'parameters': ['id', 'format', 'key'],
            'param_count': 3
        },
        {
            'original_url': 'https://test.example.com/product?pid=456&color=red&size=large',
            'cleaned_url': 'https://test.example.com/product?pid=FUZZ&color=FUZZ&size=FUZZ',
            'domain': 'test.example.com',
            'source': 'js',
            'parameters': ['pid', 'color', 'size'],
            'param_count': 3
        },
        {
            'original_url': 'https://example.com/redirect?url=target&callback=func',
            'cleaned_url': 'https://example.com/redirect?url=FUZZ&callback=FUZZ',
            'domain': 'example.com',
            'source': 'crawl',
            'parameters': ['url', 'callback'],
            'param_count': 2
        }
    ]
    
    # Calculate statistics
    all_params = []
    for url_data in demo_urls:
        all_params.extend(url_data['parameters'])
    
    param_counter = Counter(all_params)
    
    # Source statistics
    source_stats = {
        'wayback': {'total_urls': 25, 'errors': 0},
        'sitemap': {'total_urls': 15, 'errors': 1},
        'js': {'total_urls': 8, 'errors': 0},
        'crawl': {'total_urls': 12, 'errors': 2}
    }
    
    return {
        'urls': demo_urls,
        'parameters': param_counter,
        'domains': {'example.com', 'test.example.com'},
        'stats': {
            'domains_processed': 2,
            'total_urls_fetched': 60,
            'total_urls_with_params': len(demo_urls),
            'unique_parameters': len(param_counter),
            'execution_time': 12.5,
            'filtered_out': 15
        },
        'source_stats': source_stats
    }


def demo_filtering():
    """Demonstrate intelligent parameter filtering"""
    print_info("=== INTELLIGENT PARAMETER FILTERING DEMO ===")
    print("")
    
    args = DemoArgs()
    filter_obj = ParameterFilter(args)
    
    test_cases = [
        {
            'name': 'E-commerce Product Page',
            'url': 'https://shop.example.com/product?id=123&color=blue&size=medium&utm_campaign=summer&session=abc123&ref=google'
        },
        {
            'name': 'Search Results',
            'url': 'https://example.com/search?q=security&page=2&sort=date&category=web&gclid=tracking123&_ga=analytics'
        },
        {
            'name': 'API Endpoint',
            'url': 'https://api.example.com/data?key=secret&format=json&callback=jsonp&debug=true&timestamp=1234567890'
        },
        {
            'name': 'User Profile',
            'url': 'https://example.com/user?uid=456&profile=full&admin=false&token=auth123&cache=false'
        }
    ]
    
    for test in test_cases:
        print_info(f"Test Case: {test['name']}")
        print(f"Original URL: {test['url']}")
        
        # Extract parameters
        params = filter_obj.extract_parameters(test['url'])
        print(f"All Parameters: {params}")
        
        # Apply filtering
        filtered = filter_obj.filter_parameters(params)
        print(f"After Filtering: {filtered}")
        
        # Create cleaned URL
        cleaned = filter_obj.create_cleaned_url(test['url'], filtered, "FUZZ")
        print(f"Cleaned URL: {cleaned}")
        
        # Get interesting parameters
        interesting = filter_obj.get_interesting_parameters(params)
        print(f"High-Value Parameters: {interesting}")
        print("")


def demo_export_formats():
    """Demonstrate multiple export formats"""
    print_info("=== EXPORT FORMATS DEMO ===")
    print("")
    
    results = create_demo_results()
    
    # Test different export formats
    formats = ['txt', 'csv', 'json']
    
    for format_type in formats:
        args = DemoArgs()
        args.format = format_type
        args.output = f'demo_output.{format_type}'
        
        exporter = ResultExporter(args)
        output_file = exporter.export(results)
        
        if output_file:
            print_success(f"✓ {format_type.upper()} export: {output_file}")
            
            # Show file size
            try:
                import os
                size = os.path.getsize(output_file)
                print(f"  File size: {size} bytes")
            except:
                pass
        else:
            print_error(f"✗ {format_type.upper()} export failed")
    
    # Generate comprehensive report
    args = DemoArgs()
    exporter = ResultExporter(args)
    report_file = exporter.export_summary_report(results)
    if report_file:
        print_success(f"✓ Summary report: {report_file}")


def demo_statistics():
    """Demonstrate comprehensive statistics"""
    print_info("=== ADVANCED STATISTICS DEMO ===")
    print("")
    
    results = create_demo_results()
    
    print("📊 SCAN SUMMARY")
    print(f"  Domains Scanned: {len(results['domains'])}")
    print(f"  Total URLs Found: {results['stats']['total_urls_fetched']}")
    print(f"  URLs with Parameters: {results['stats']['total_urls_with_params']}")
    print(f"  Unique Parameters: {results['stats']['unique_parameters']}")
    print(f"  Execution Time: {results['stats']['execution_time']}s")
    print("")
    
    print("🔍 SOURCE BREAKDOWN")
    for source, stats in results['source_stats'].items():
        success_rate = ((stats['total_urls'] - stats['errors']) / stats['total_urls'] * 100) if stats['total_urls'] > 0 else 0
        print(f"  {source.capitalize()}: {stats['total_urls']} URLs ({success_rate:.1f}% success)")
    print("")
    
    print("🏆 TOP PARAMETERS")
    for param, count in results['parameters'].most_common(10):
        print(f"  {param}: {count} occurrences")
    print("")


def demo_cli_examples():
    """Show CLI usage examples"""
    print_info("=== CLI USAGE EXAMPLES ===")
    print("")
    
    examples = [
        {
            'description': 'Basic domain scan',
            'command': 'python spiderx_cli.py -d example.com'
        },
        {
            'description': 'Multiple domains from file',
            'command': 'python spiderx_cli.py -l domains.txt'
        },
        {
            'description': 'Specific sources only',
            'command': 'python spiderx_cli.py -d example.com --sources wayback,sitemap'
        },
        {
            'description': 'Custom output with JSON format',
            'command': 'python spiderx_cli.py -d example.com -o results.json --format json'
        },
        {
            'description': 'With proxy and custom boring parameters',
            'command': 'python spiderx_cli.py -d example.com --proxy http://127.0.0.1:8080 --boring-list myboring.txt'
        },
        {
            'description': 'Disable filtering (get all parameters)',
            'command': 'python spiderx_cli.py -d example.com --no-filter'
        },
        {
            'description': 'Show top 20 parameters with statistics',
            'command': 'python spiderx_cli.py -d example.com --top-params 20 --stats'
        },
        {
            'description': 'Import URLs from file',
            'command': 'python spiderx_cli.py -i existing_urls.txt'
        }
    ]
    
    for example in examples:
        print_success(f"# {example['description']}")
        print(f"  {example['command']}")
        print("")


def main():
    """Main demo function"""
    print_banner()
    print_info("🚀 Welcome to SpiderX Advanced Demo!")
    print_info("This demonstrates the legendary capabilities of SpiderX")
    print("")
    
    # Demo sections
    demo_filtering()
    demo_statistics()
    demo_export_formats()
    demo_cli_examples()
    
    print_success("🎉 Demo completed! SpiderX is ready for legendary URL parameter discovery!")
    print("")
    print_info("Key advantages over competitors:")
    print("  ✓ Multiple data sources (Wayback, Sitemap, JS, Live Crawling)")
    print("  ✓ Intelligent filtering with 60+ boring parameters")
    print("  ✓ Wildcard patterns for advanced filtering")
    print("  ✓ Multiple export formats (TXT, CSV, JSON)")
    print("  ✓ Comprehensive statistics and analysis")
    print("  ✓ High-performance async processing")
    print("  ✓ Professional CLI with extensive options")
    print("  ✓ Modular and extensible architecture")


if __name__ == "__main__":
    main()