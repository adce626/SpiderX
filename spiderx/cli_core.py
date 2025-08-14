"""
SpiderX CLI Core Module
نواة واجهة سطر الأوامر للأداة الأسطورية

Main CLI logic and coordination between different modules
"""

import asyncio
import time
from typing import List, Dict, Set, Any
from pathlib import Path
from collections import Counter, defaultdict

from .sources import SourceManager
from .filters import ParameterFilter
from .exporters import ResultExporter
from .utils import ProgressBar, format_time, print_success, print_error, print_info


class SpiderXCLI:
    """Main CLI controller for SpiderX operations"""
    
    def __init__(self, args):
        self.args = args
        self.start_time = time.time()
        self.results = {
            'urls': [],
            'parameters': Counter(),
            'domains': set(),
            'stats': defaultdict(int),
            'source_stats': defaultdict(lambda: defaultdict(int))
        }
        
        # Initialize components
        self.source_manager = SourceManager(args)
        self.parameter_filter = ParameterFilter(args)
        self.result_exporter = ResultExporter(args)
    
    async def run(self) -> Dict[str, Any]:
        """Execute the main scanning process"""
        print_info("Starting SpiderX scan...")
        
        # Get target domains
        domains = self._get_target_domains()
        if not domains:
            raise ValueError("No valid domains found")
        
        self.results['domains'] = set(domains)
        print_info(f"Scanning {len(domains)} domain(s)")
        
        # Process each domain
        total_urls = []
        for i, domain in enumerate(domains, 1):
            print_info(f"[{i}/{len(domains)}] Processing: {domain}")
            
            domain_urls = await self._process_domain(domain)
            total_urls.extend(domain_urls)
            
            self.results['stats']['domains_processed'] += 1
        
        # Process and filter URLs
        print_info("Processing and filtering URLs...")
        processed_urls = self._process_urls(total_urls)
        
        # Final statistics
        self._calculate_final_stats(processed_urls)
        
        return self.results
    
    def _get_target_domains(self) -> List[str]:
        """Get target domains from various input methods"""
        domains = []
        
        if self.args.domain:
            domains.append(self.args.domain.strip())
        elif self.args.list:
            domains = self._read_domains_from_file(self.args.list)
        
        # Clean and validate domains
        cleaned_domains = []
        for domain in domains:
            domain = domain.strip().lower()
            domain = domain.replace('http://', '').replace('https://', '')
            domain = domain.split('/')[0]  # Remove path if present
            if domain and '.' in domain:
                cleaned_domains.append(domain)
        
        return list(set(cleaned_domains))  # Remove duplicates
    
    def _read_domains_from_file(self, filename: str) -> List[str]:
        """Read domains from file"""
        try:
            with open(filename, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            raise ValueError(f"Domain list file not found: {filename}")
    
    async def _process_domain(self, domain: str) -> List[Dict[str, Any]]:
        """Process a single domain using all enabled sources"""
        domain_urls = []
        
        # Get sources to use
        sources = self._get_enabled_sources()
        
        for source_name in sources:
            try:
                print_info(f"  Fetching from {source_name}...")
                urls = await self.source_manager.fetch_from_source(source_name, domain)
                
                self.results['source_stats'][source_name]['total_urls'] += len(urls)
                self.results['stats']['total_urls_fetched'] += len(urls)
                
                domain_urls.extend(urls)
                print_success(f"  {source_name}: {len(urls)} URLs found")
                
            except Exception as e:
                print_error(f"  {source_name}: Failed - {str(e)}")
                self.results['source_stats'][source_name]['errors'] += 1
        
        return domain_urls
    
    def _get_enabled_sources(self) -> List[str]:
        """Get list of enabled sources based on arguments"""
        if self.args.sources == "all":
            return ["wayback", "sitemap", "js", "crawl"]
        else:
            return self.args.sources.split(',')
    
    def _process_urls(self, urls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and filter URLs"""
        processed_urls = []
        
        for url_data in urls:
            # Extract parameters
            params = self.parameter_filter.extract_parameters(url_data['url'])
            
            if not params:
                continue
            
            # Apply filtering if enabled
            if not self.args.no_filter:
                filtered_params = self.parameter_filter.filter_parameters(params)
                if not filtered_params:
                    self.results['stats']['filtered_out'] += 1
                    continue
                params = filtered_params
            
            # Create cleaned URL with placeholder
            cleaned_url = self.parameter_filter.create_cleaned_url(
                url_data['url'], params, self.args.placeholder
            )
            
            processed_url = {
                'original_url': url_data['url'],
                'cleaned_url': cleaned_url,
                'domain': url_data.get('domain', ''),
                'source': url_data.get('source', ''),
                'parameters': params,
                'param_count': len(params)
            }
            
            processed_urls.append(processed_url)
            
            # Update parameter statistics
            for param in params:
                self.results['parameters'][param] += 1
        
        self.results['urls'] = processed_urls
        return processed_urls
    
    def _calculate_final_stats(self, processed_urls: List[Dict[str, Any]]):
        """Calculate final statistics"""
        self.results['stats'].update({
            'total_urls_with_params': len(processed_urls),
            'unique_parameters': len(self.results['parameters']),
            'execution_time': time.time() - self.start_time,
            'urls_per_second': len(processed_urls) / (time.time() - self.start_time) if processed_urls else 0
        })
    
    def display_results(self, results: Dict[str, Any]):
        """Display results to console"""
        print("\n" + "="*60)
        print("SPIDERX SCAN COMPLETE")
        print("="*60)
        
        stats = results['stats']
        
        # Basic statistics
        print(f"Domains Scanned: {stats['domains_processed']}")
        print(f"URLs Fetched: {stats['total_urls_fetched']}")
        print(f"URLs with Parameters: {stats['total_urls_with_params']}")
        print(f"Unique Parameters: {stats['unique_parameters']}")
        print(f"Execution Time: {format_time(stats['execution_time'])}")
        
        if stats.get('filtered_out', 0) > 0:
            print(f"URLs Filtered Out: {stats['filtered_out']}")
        
        # Source statistics
        if self.args.stats:
            print("\nSource Statistics:")
            for source, source_stats in results['source_stats'].items():
                print(f"  {source.capitalize()}: {source_stats['total_urls']} URLs")
                if source_stats['errors'] > 0:
                    print(f"    Errors: {source_stats['errors']}")
        
        # Top parameters
        if self.args.top_params and results['parameters']:
            print(f"\nTop {self.args.top_params} Parameters:")
            for param, count in results['parameters'].most_common(self.args.top_params):
                print(f"  {param}: {count} times")
        
        # Sample URLs
        if results['urls']:
            print(f"\nSample URLs (showing first 5):")
            for i, url_data in enumerate(results['urls'][:5], 1):
                print(f"  {i}. {url_data['cleaned_url']}")
                print(f"     Parameters: {', '.join(url_data['parameters'])}")
        
        print("\n" + "="*60)
    
    def export_results(self, results: Dict[str, Any]):
        """Export results to file"""
        output_file = self.result_exporter.export(results)
        if output_file:
            print_success(f"Results saved to: {output_file}")
        else:
            print_error("Failed to save results")