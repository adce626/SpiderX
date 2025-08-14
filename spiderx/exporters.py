"""
Result Export Module
وحدة تصدير النتائج

Flexible result exporting in multiple formats with comprehensive statistics
"""

import json
import csv
import io
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime


class ResultExporter:
    """Flexible result exporter with multiple format support"""
    
    def __init__(self, args):
        self.args = args
        self.output_format = getattr(args, 'format', 'txt')
        self.output_file = getattr(args, 'output', None)
    
    def export(self, results: Dict[str, Any]) -> str | None:
        """Export results in specified format"""
        if not results or not results.get('urls'):
            print("No results to export")
            return None
        
        # Generate output filename if not specified
        if not self.output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_file = f"spiderx_results_{timestamp}.{self.output_format}"
        
        try:
            if self.output_format == 'json':
                return self._export_json(results)
            elif self.output_format == 'csv':
                return self._export_csv(results)
            else:  # default to txt
                return self._export_txt(results)
                
        except Exception as e:
            print(f"Export error: {e}")
            return None
    
    def _export_txt(self, results: Dict[str, Any]) -> str:
        """Export as plain text format"""
        lines = []
        
        # Add header with statistics
        lines.append("# SpiderX Results")
        lines.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"# Total URLs: {len(results['urls'])}")
        lines.append(f"# Unique Parameters: {results['stats']['unique_parameters']}")
        lines.append(f"# Domains: {', '.join(results['domains'])}")
        lines.append("#")
        
        # Add URLs
        for url_data in results['urls']:
            lines.append(url_data['cleaned_url'])
        
        # Write to file
        content = '\n'.join(lines)
        with open(self.output_file, 'w') as f:
            f.write(content)
        
        return self.output_file
    
    def _export_csv(self, results: Dict[str, Any]) -> str:
        """Export as CSV format"""
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'cleaned_url', 'original_url', 'domain', 'source', 
                'parameters', 'param_count'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data
            for url_data in results['urls']:
                row = {
                    'cleaned_url': url_data['cleaned_url'],
                    'original_url': url_data['original_url'],
                    'domain': url_data['domain'],
                    'source': url_data['source'],
                    'parameters': ', '.join(url_data['parameters']),
                    'param_count': url_data['param_count']
                }
                writer.writerow(row)
        
        return self.output_file
    
    def _export_json(self, results: Dict[str, Any]) -> str:
        """Export as JSON format"""
        # Prepare data for JSON serialization
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'tool': 'SpiderX',
                'version': '1.0',
                'domains': list(results['domains']),
                'total_urls': len(results['urls']),
                'unique_parameters': results['stats']['unique_parameters'],
                'execution_time': results['stats']['execution_time']
            },
            'statistics': {
                'source_breakdown': dict(results['source_stats']),
                'parameter_frequency': dict(results['parameters'].most_common(50)),
                'general_stats': dict(results['stats'])
            },
            'urls': results['urls']
        }
        
        # Write to file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return self.output_file
    
    def generate_summary_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive summary report"""
        report_lines = []
        
        # Header
        report_lines.extend([
            "="*60,
            "SPIDERX COMPREHENSIVE REPORT",
            "="*60,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ])
        
        # Executive Summary
        stats = results['stats']
        report_lines.extend([
            "EXECUTIVE SUMMARY:",
            f"• Domains Scanned: {len(results['domains'])}",
            f"• Total URLs Found: {stats.get('total_urls_fetched', 0)}",
            f"• URLs with Parameters: {stats.get('total_urls_with_params', 0)}",
            f"• Unique Parameters: {stats.get('unique_parameters', 0)}",
            f"• Processing Time: {stats.get('execution_time', 0):.2f} seconds",
            ""
        ])
        
        # Domain Breakdown
        if len(results['domains']) > 1:
            report_lines.extend([
                "DOMAIN BREAKDOWN:",
                *[f"• {domain}" for domain in results['domains']],
                ""
            ])
        
        # Source Statistics
        if results['source_stats']:
            report_lines.extend(["SOURCE STATISTICS:"])
            for source, source_stats in results['source_stats'].items():
                total = source_stats.get('total_urls', 0)
                errors = source_stats.get('errors', 0)
                report_lines.append(f"• {source.capitalize()}: {total} URLs" + (f" ({errors} errors)" if errors else ""))
            report_lines.append("")
        
        # Top Parameters
        if results['parameters']:
            report_lines.extend([
                "TOP 20 PARAMETERS:",
                *[f"• {param}: {count} occurrences" for param, count in results['parameters'].most_common(20)],
                ""
            ])
        
        # Parameter Analysis (if available)
        if 'parameter_analysis' in results:
            analysis = results['parameter_analysis']
            report_lines.extend([
                "PARAMETER ANALYSIS:",
                f"• Tracking Parameters: {len(analysis.get('categories', {}).get('tracking', []))}",
                f"• User Input Parameters: {len(analysis.get('categories', {}).get('user_input', []))}",
                f"• Navigation Parameters: {len(analysis.get('categories', {}).get('navigation', []))}",
                f"• API Parameters: {len(analysis.get('categories', {}).get('api', []))}",
                ""
            ])
        
        # Sample URLs
        if results['urls']:
            report_lines.extend([
                "SAMPLE URLS (First 10):",
                *[f"• {url_data['cleaned_url']}" for url_data in results['urls'][:10]],
                ""
            ])
        
        report_lines.append("="*60)
        
        return '\n'.join(report_lines)
    
    def export_summary_report(self, results: Dict[str, Any]) -> str:
        """Export a summary report to file"""
        report_content = self.generate_summary_report(results)
        
        # Generate report filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"spiderx_report_{timestamp}.txt"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            return report_file
        except Exception as e:
            print(f"Failed to save report: {e}")
            return None