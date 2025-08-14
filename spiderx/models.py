from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import uuid

class ScanRequest(BaseModel):
    domains: List[str] = Field(..., description="List of domains to scan")
    placeholder: str = Field(default="FUZZ", description="Placeholder for parameter values")
    proxy: Optional[str] = Field(None, description="Proxy configuration (http://host:port)")
    filter_extensions: bool = Field(default=True, description="Filter out URLs with static file extensions")
    custom_extensions: Optional[List[str]] = Field(None, description="Custom extensions to filter")
    max_urls_per_domain: int = Field(default=10000, description="Maximum URLs to process per domain")
    include_subdomains: bool = Field(default=False, description="Include subdomains in search")

class URLInfo(BaseModel):
    url: str
    domain: str
    parameters: List[str]
    parameter_count: int
    cleaned_url: str
    
class DomainStats(BaseModel):
    domain: str
    total_urls_found: int
    urls_with_parameters: int
    unique_parameters: List[str]
    processing_time: float

class ScanResult(BaseModel):
    scan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str = Field(default="running")  # running, completed, failed
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    domains_scanned: List[str] = []
    total_urls_found: int = 0
    urls_with_parameters: int = 0
    unique_parameters: List[str] = []
    domain_stats: List[DomainStats] = []
    urls: List[URLInfo] = []
    error_message: Optional[str] = None
    progress: int = Field(default=0, description="Progress percentage")

class ScanStatus(BaseModel):
    scan_id: str
    status: str
    progress: int
    current_domain: Optional[str] = None
    urls_processed: int = 0
    elapsed_time: float = 0