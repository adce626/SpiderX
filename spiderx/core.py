import asyncio
import aiohttp
import time
import json
import csv
import io
from urllib.parse import urlparse, parse_qs, urlencode
from typing import List, Dict, Optional, Tuple
import re
from datetime import datetime

from .models import ScanRequest, ScanResult, URLInfo, DomainStats, ScanStatus
from .utils import clean_url, has_extension

class SpiderXCore:
    def __init__(self):
        self.active_scans: Dict[str, ScanResult] = {}
        self.hardcoded_extensions = [
            ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", ".json",
            ".css", ".js", ".webp", ".woff", ".woff2", ".eot", ".ttf", 
            ".otf", ".mp4", ".txt", ".xml", ".ico", ".zip", ".rar",
            ".tar", ".gz", ".exe", ".dmg", ".pkg", ".deb", ".rpm"
        ]
    
    async def scan_domains(self, request: ScanRequest) -> ScanResult:
        """Start scanning domains for URL parameters"""
        result = ScanResult(domains_scanned=request.domains)
        self.active_scans[result.scan_id] = result
        
        # Start background task for scanning
        asyncio.create_task(self._perform_scan(request, result))
        
        return result
    
    async def _perform_scan(self, request: ScanRequest, result: ScanResult):
        """Perform the actual scanning process"""
        try:
            result.status = "running"
            start_time = time.time()
            
            extensions = request.custom_extensions or self.hardcoded_extensions if request.filter_extensions else []
            
            total_domains = len(request.domains)
            all_urls = []
            all_parameters = set()
            
            for i, domain in enumerate(request.domains):
                result.progress = int((i / total_domains) * 100)
                
                domain_start = time.time()
                domain_urls = await self._fetch_domain_urls(domain, request, extensions)
                domain_time = time.time() - domain_start
                
                # Process URLs for this domain
                domain_params = set()
                urls_with_params = 0
                
                for url_info in domain_urls:
                    all_urls.append(url_info)
                    if url_info.parameters:
                        urls_with_params += 1
                        domain_params.update(url_info.parameters)
                        all_parameters.update(url_info.parameters)
                
                # Create domain stats
                domain_stats = DomainStats(
                    domain=domain,
                    total_urls_found=len(domain_urls),
                    urls_with_parameters=urls_with_params,
                    unique_parameters=list(domain_params),
                    processing_time=domain_time
                )
                result.domain_stats.append(domain_stats)
            
            # Finalize results
            result.urls = all_urls
            result.total_urls_found = len(all_urls)
            result.urls_with_parameters = len([url for url in all_urls if url.parameters])
            result.unique_parameters = list(all_parameters)
            result.status = "completed"
            result.completed_at = datetime.now()
            result.progress = 100
            
        except Exception as e:
            result.status = "failed"
            result.error_message = str(e)
            result.completed_at = datetime.now()
    
    async def _fetch_domain_urls(self, domain: str, request: ScanRequest, extensions: List[str]) -> List[URLInfo]:
        """Fetch URLs for a specific domain from Wayback Machine"""
        wayback_url = f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=txt&collapse=urlkey&fl=original&page=/"
        
        urls_info = []
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                proxy = request.proxy if request.proxy else None
                
                async with session.get(wayback_url, headers=headers, proxy=proxy) as response:
                    if response.status == 200:
                        text = await response.text()
                        raw_urls = text.strip().split('\n')
                        
                        # Limit URLs per domain
                        if len(raw_urls) > request.max_urls_per_domain:
                            raw_urls = raw_urls[:request.max_urls_per_domain]
                        
                        for raw_url in raw_urls:
                            if raw_url.strip():
                                url_info = self._process_url(raw_url.strip(), domain, request.placeholder, extensions)
                                if url_info:
                                    urls_info.append(url_info)
        
        except Exception as e:
            print(f"Error fetching URLs for {domain}: {str(e)}")
        
        return urls_info
    
    def _process_url(self, url: str, domain: str, placeholder: str, extensions: List[str]) -> Optional[URLInfo]:
        """Process a single URL and extract parameter information"""
        try:
            # Skip URLs with unwanted extensions
            if extensions and has_extension(url, extensions):
                return None
            
            cleaned = clean_url(url)
            parsed = urlparse(cleaned)
            
            # Extract parameters
            query_params = parse_qs(parsed.query)
            parameters = list(query_params.keys())
            
            # Only include URLs with parameters
            if not parameters:
                return None
            
            # Create cleaned URL with placeholder
            if placeholder and placeholder != "FUZZ":
                cleaned_params = {key: placeholder for key in parameters}
                cleaned_query = urlencode(cleaned_params, doseq=True)
                cleaned_url = parsed._replace(query=cleaned_query).geturl()
            else:
                cleaned_url = cleaned
            
            return URLInfo(
                url=url,
                domain=domain,
                parameters=parameters,
                parameter_count=len(parameters),
                cleaned_url=cleaned_url
            )
        
        except Exception:
            return None
    
    def get_scan_status(self, scan_id: str) -> ScanStatus:
        """Get the status of a running scan"""
        if scan_id not in self.active_scans:
            raise ValueError("Scan not found")
        
        result = self.active_scans[scan_id]
        
        return ScanStatus(
            scan_id=scan_id,
            status=result.status,
            progress=result.progress,
            urls_processed=len(result.urls),
            elapsed_time=(datetime.now() - result.started_at).total_seconds()
        )
    
    def get_scan_results(self, scan_id: str) -> ScanResult:
        """Get the complete results of a scan"""
        if scan_id not in self.active_scans:
            raise ValueError("Scan not found")
        
        return self.active_scans[scan_id]
    
    def export_results(self, scan_id: str, format: str) -> Tuple[str, str, str]:
        """Export scan results in specified format"""
        if scan_id not in self.active_scans:
            raise ValueError("Scan not found")
        
        result = self.active_scans[scan_id]
        
        if format.lower() == "json":
            content = json.dumps(result.dict(), indent=2, default=str)
            return content, "application/json", f"spiderx_results_{scan_id}.json"
        
        elif format.lower() == "txt":
            lines = []
            for url_info in result.urls:
                lines.append(url_info.cleaned_url)
            content = "\n".join(lines)
            return content, "text/plain", f"spiderx_results_{scan_id}.txt"
        
        elif format.lower() == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["URL", "Domain", "Parameters", "Parameter Count", "Cleaned URL"])
            
            for url_info in result.urls:
                writer.writerow([
                    url_info.url,
                    url_info.domain,
                    ", ".join(url_info.parameters),
                    url_info.parameter_count,
                    url_info.cleaned_url
                ])
            
            content = output.getvalue()
            return content, "text/csv", f"spiderx_results_{scan_id}.csv"
        
        else:
            raise ValueError("Unsupported format. Use: json, txt, or csv")