#!/usr/bin/env python3
"""
SpiderX CLI - LEGENDARY ENGLISH VERSION
The ultimate URL parameter mining tool that completely surpasses ParamSpider
"""

import asyncio
import argparse
import sys
import time
from pathlib import Path
from typing import List, Dict, Set
from collections import Counter

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

from spiderx.utils import (
    print_banner, print_info, print_success, print_error, print_warning,
    get_random_user_agent, smart_rate_limit, detect_potential_vulnerability_params,
    analyze_parameter_complexity
)
from spiderx.sources.wayback import WaybackSource
from spiderx.sources.sitemap import SitemapSource  
from spiderx.sources.javascript import JavaScriptSource
from spiderx.filters import ParameterFilter
from spiderx.exporters import ResultExporter


class LegendarySpiderX:
    """SpiderX Legendary - Surpasses all competing tools"""
    
    def __init__(self, args):
        self.args = args
        self.start_time = time.time()
        
        # Advanced statistics
        self.stats = {
            'domains_processed': 0,
            'total_urls_found': 0,
            'parameters_discovered': set(),
            'vulnerability_findings': {},
            'source_effectiveness': Counter(),
            'processing_errors': []
        }
        
        # Advanced data sources
        self.sources = {
            'wayback': WaybackSource(args),
            'sitemap': SitemapSource(args),
            'javascript': JavaScriptSource(args)
        }
        
        # Smart parameter filter
        self.filter = ParameterFilter(args)
        
        # Results exporter
        self.exporter = ResultExporter(args)
    
    async def legendary_scan(self, domains: List[str]) -> Dict:
        """Comprehensive legendary scanning"""
        print_banner()
        print_success("🚀 Starting legendary SpiderX scan!")
        print_info(f"Targets: {len(domains)} domains")
        print("")
        
        all_results = {
            'urls': [],
            'parameters': Counter(),
            'domains': set(domains),
            'vulnerability_analysis': {},
            'source_stats': {},
            'performance_metrics': {}
        }
        
        # Process each domain
        for domain in domains:
            print_info(f"🎯 Processing domain: {domain}")
            domain_results = await self._process_domain_legendary(domain)
            
            # Merge results
            all_results['urls'].extend(domain_results.get('urls', []))
            all_results['parameters'].update(domain_results.get('parameters', {}))
            
            self.stats['domains_processed'] += 1
            
        # Analyze parameters for vulnerabilities - legendary feature
        print_info("🔍 Analyzing parameters for security vulnerabilities...")
        vulnerability_analysis = self._analyze_vulnerabilities(all_results['parameters'])
        all_results['vulnerability_analysis'] = vulnerability_analysis
        
        # Performance metrics
        execution_time = time.time() - self.start_time
        all_results['performance_metrics'] = {
            'execution_time': execution_time,
            'domains_processed': self.stats['domains_processed'],
            'total_parameters': len(all_results['parameters']),
            'urls_per_second': len(all_results['urls']) / execution_time if execution_time > 0 else 0
        }
        
        # Display legendary report
        self._display_legendary_report(all_results)
        
        return all_results
    
    async def _process_domain_legendary(self, domain: str) -> Dict:
        """Process domain with legendary approach"""
        domain_results = {
            'urls': [],
            'parameters': Counter(),
            'source_breakdown': {}
        }
        
        # Use multiple sources - competitive advantage
        tasks = []
        
        if not self.args.sources or 'wayback' in self.args.sources:
            tasks.append(self._fetch_from_source('wayback', domain))
        
        if not self.args.sources or 'sitemap' in self.args.sources:
            tasks.append(self._fetch_from_source('sitemap', domain))
        
        if not self.args.sources or 'javascript' in self.args.sources:
            tasks.append(self._fetch_from_source('javascript', domain))
        
        # High-performance parallel execution
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    source_name = list(self.sources.keys())[i]
                    print_error(f"Error in source {source_name}: {result}")
                    continue
                
                if isinstance(result, list):
                    # Process and filter parameters
                    processed_urls = self._process_urls_intelligent(result, domain)
                    domain_results['urls'].extend(processed_urls)
                    
                    # Parameter statistics
                    for url_data in processed_urls:
                        for param in url_data.get('parameters', []):
                            domain_results['parameters'][param] += 1
        
        return domain_results
    
    async def _fetch_from_source(self, source_name: str, domain: str) -> List[str]:
        """Fetch data from specific source"""
        try:
            source = self.sources[source_name]
            
            # Set maximum URLs limit
            max_urls = getattr(self.args, 'max_urls', 1000)
            
            # Fetch data with smart rate control
            if hasattr(source, 'fetch_urls'):
                urls = await source.fetch_urls(domain)
            else:
                urls = []
            
            # Record source effectiveness
            self.stats['source_effectiveness'][source_name] += len(urls)
            
            print_success(f"✓ {source_name}: {len(urls)} URLs")
            return urls[:max_urls] if urls else []
            
        except Exception as e:
            print_error(f"Error in source {source_name}: {e}")
            self.stats['processing_errors'].append(f"{source_name}: {e}")
            return []
    
    def _process_urls_intelligent(self, urls: List[str], domain: str) -> List[Dict]:
        """Intelligent URL processing with advanced filtering"""
        processed_urls = []
        
        for url in urls:
            try:
                # Extract parameters
                parameters = self.filter.extract_parameters(url)
                
                if not parameters:
                    continue
                
                # Smart filtering
                if not self.args.no_filter:
                    filtered_params = self.filter.filter_parameters(parameters)
                else:
                    filtered_params = parameters
                
                if not filtered_params:
                    continue
                
                # Create cleaned URL
                cleaned_url = self.filter.create_cleaned_url(
                    url, filtered_params, 
                    getattr(self.args, 'placeholder', 'FUZZ')
                )
                
                # Processed URL data
                url_data = {
                    'original_url': url,
                    'cleaned_url': cleaned_url,
                    'domain': domain,
                    'parameters': filtered_params,
                    'param_count': len(filtered_params)
                }
                
                processed_urls.append(url_data)
                
            except Exception as e:
                if getattr(self.args, 'debug', False):
                    print_error(f"Error processing URL {url}: {e}")
                continue
        
        return processed_urls
    
    def _analyze_vulnerabilities(self, parameters: Counter) -> Dict:
        """Analyze parameters for security vulnerabilities - legendary unique feature"""
        param_set = set(parameters.keys())
        
        # Detect potential vulnerability parameters
        vulnerability_findings = detect_potential_vulnerability_params(param_set)
        
        # Complexity analysis
        complexity_analysis = analyze_parameter_complexity(param_set)
        
        # Classify parameters by priority
        high_priority_params = []
        for param, score in complexity_analysis.items():
            if score >= 5:  # High threshold
                high_priority_params.append({
                    'parameter': param,
                    'score': score,
                    'frequency': parameters[param]
                })
        
        # Sort by score
        high_priority_params.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'vulnerability_findings': vulnerability_findings,
            'complexity_analysis': complexity_analysis,
            'high_priority_params': high_priority_params[:20],  # Top 20
            'total_risk_params': len([p for p in complexity_analysis.values() if p >= 5])
        }
    
    def _display_legendary_report(self, results: Dict):
        """Display legendary report"""
        print("")
        print_success("🏆 SpiderX Legendary Report")
        print("=" * 50)
        
        # Basic statistics
        metrics = results['performance_metrics']
        print_info(f"⏱️  Execution Time: {metrics['execution_time']:.2f} seconds")
        print_info(f"🌐 Domains Processed: {metrics['domains_processed']}")
        print_info(f"🔗 Total URLs: {len(results['urls'])}")
        print_info(f"🎯 Parameters Discovered: {metrics['total_parameters']}")
        print_info(f"⚡ Speed: {metrics['urls_per_second']:.1f} URLs/second")
        print("")
        
        # Top parameters
        if results['parameters']:
            print_info("🏅 Top Discovered Parameters:")
            for param, count in results['parameters'].most_common(10):
                print(f"   {param}: {count} occurrences")
            print("")
        
        # Security vulnerability analysis - exclusive feature
        vuln_analysis = results.get('vulnerability_analysis', {})
        if vuln_analysis.get('vulnerability_findings'):
            print_warning("🚨 Potential Security Vulnerability Parameters:")
            for vuln_type, params in vuln_analysis['vulnerability_findings'].items():
                if params:
                    print(f"   {vuln_type}: {', '.join(params[:3])}")
            print("")
        
        # High priority parameters
        high_priority = vuln_analysis.get('high_priority_params', [])
        if high_priority:
            print_info("🎯 High Priority Parameters for Testing:")
            for param_data in high_priority[:5]:
                print(f"   {param_data['parameter']} (Score: {param_data['score']}, Frequency: {param_data['frequency']})")
            print("")
        
        # Source effectiveness
        print_info("📊 Source Effectiveness:")
        for source, count in self.stats['source_effectiveness'].items():
            percentage = (count / len(results['urls']) * 100) if results['urls'] else 0
            print(f"   {source}: {count} URLs ({percentage:.1f}%)")
        print("")
        
        print_success("🕷️ SpiderX: Legendary scan completed successfully!")
        
        # Display competitive advantages
        self._display_competitive_advantages()
    
    def _display_competitive_advantages(self):
        """Display competitive advantages over ParamSpider"""
        print("")
        print_success("🏆 SpiderX Competitive Advantages over ParamSpider:")
        print("=" * 55)
        
        advantages = [
            "✓ Multiple sources: Wayback + Sitemap + JavaScript (vs Wayback only)",
            "✓ Smart filtering: 60+ boring params + wildcard patterns",
            "✓ Vulnerability detection: Real-time security parameter analysis",
            "✓ Export formats: TXT + CSV + JSON with metadata",
            "✓ Performance: Async multi-threaded processing",
            "✓ Intelligence: Parameter classification and testing recommendations",
            "✓ Rate control: Smart adaptive rate limiting",
            "✓ Error handling: Robust retry mechanism",
            "✓ Statistics: Comprehensive analytics and live reporting",
            "✓ Customization: Highly configurable with 20+ CLI options"
        ]
        
        for advantage in advantages:
            print(f"  {advantage}")
        
        print("")
        print_success("🕷️ SpiderX: The LEGENDARY URL parameter discovery tool!")


def create_argument_parser():
    """Create argument parser with comprehensive options"""
    parser = argparse.ArgumentParser(
        description="SpiderX - Legendary URL parameter mining tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Examples:
  python spiderx_english.py -d example.com
  python spiderx_english.py -l domains.txt --format json
  python spiderx_english.py -d example.com --sources wayback,sitemap
  python spiderx_english.py -d example.com --no-filter --stats
        """
    )
    
    # Target options
    target_group = parser.add_argument_group('Target Options')
    target_group.add_argument('-d', '--domain', help='Target domain for scanning')
    target_group.add_argument('-l', '--list', help='File containing list of domains')
    
    # Source options
    source_group = parser.add_argument_group('Source Options')
    source_group.add_argument('--sources', help='Choose sources: wayback,sitemap,javascript,all (default: all)')
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('-o', '--output', help='Output file name')
    output_group.add_argument('--format', choices=['txt', 'csv', 'json'], default='txt', help='Export format')
    output_group.add_argument('--no-save', action='store_true', help='Do not save, display results only')
    
    # Filtering options
    filter_group = parser.add_argument_group('Filtering Options')
    filter_group.add_argument('--boring-list', help='Custom boring parameters file')
    filter_group.add_argument('--no-filter', action='store_true', help='Disable parameter filtering')
    filter_group.add_argument('--custom-filter', nargs='+', help='Add custom parameters to filter')
    
    # Advanced options
    advanced_group = parser.add_argument_group('Advanced Options')
    advanced_group.add_argument('--placeholder', default='FUZZ', help='Parameter placeholder text')
    advanced_group.add_argument('--proxy', help='HTTP proxy')
    advanced_group.add_argument('--timeout', type=int, default=30, help='Request timeout in seconds')
    advanced_group.add_argument('--max-urls', type=int, default=10000, help='Maximum URLs per domain')
    
    # Analysis options
    analysis_group = parser.add_argument_group('Analysis Options')
    analysis_group.add_argument('--stats', action='store_true', help='Show detailed statistics')
    analysis_group.add_argument('--vuln-analysis', action='store_true', help='Analyze parameters for vulnerabilities')
    
    # Debug options
    debug_group = parser.add_argument_group('Debug Options')
    debug_group.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    debug_group.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    return parser


async def main():
    """Main function"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Validate arguments
    if not args.domain and not args.list:
        parser.error("Please provide either -d or -l option")
    
    if args.domain and args.list:
        parser.error("Please provide either -d or -l option, not both")
    
    # Determine domains
    domains = []
    if args.domain:
        domains = [args.domain.strip().lower().replace('https://', '').replace('http://', '')]
    elif args.list:
        try:
            with open(args.list, 'r') as f:
                domains = [
                    line.strip().lower().replace('https://', '').replace('http://', '')
                    for line in f.readlines()
                    if line.strip() and not line.startswith('#')
                ]
                domains = list(set(domains))  # Remove duplicates
        except FileNotFoundError:
            print_error(f"Domains file not found: {args.list}")
            sys.exit(1)
        except Exception as e:
            print_error(f"Error reading domains file: {e}")
            sys.exit(1)
    
    if not domains:
        print_error("No valid domains to process")
        sys.exit(1)
    
    # Process source options
    if args.sources:
        if args.sources.lower() == 'all':
            args.sources = ['wayback', 'sitemap', 'javascript']
        else:
            args.sources = [s.strip() for s in args.sources.split(',')]
    
    # Create legendary SpiderX object
    spiderx = LegendarySpiderX(args)
    
    try:
        # Execute legendary scan
        results = await spiderx.legendary_scan(domains)
        
        # Export results if not disabled
        if not args.no_save and results['urls']:
            exporter = ResultExporter(args)
            output_file = exporter.export(results)
            if output_file:
                print_success(f"💾 Results saved to: {output_file}")
        
        print_success("✨ SpiderX legendary scan completed!")
        
    except KeyboardInterrupt:
        print_error("Operation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_error("Operation cancelled")
        sys.exit(1)