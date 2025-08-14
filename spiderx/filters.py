"""
Parameter Filtering Module

Intelligent parameter filtering with customizable boring parameters and wildcard support
"""

import re
from typing import List, Set, Dict, Any
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from pathlib import Path


class ParameterFilter:
    """Intelligent parameter filtering with advanced capabilities"""
    
    def __init__(self, args):
        self.args = args
        
        # Default boring parameters
        self.default_boring_params = {
            # Tracking and Analytics
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
            'utm_id', 'utm_source_platform', 'utm_creative_format', 'utm_marketing_tactic',
            'gclid', 'gclsrc', 'dclid', 'fbclid', 'msclkid', 'ttclid',
            'ga_source', 'ga_medium', 'ga_campaign', 'ga_term', 'ga_content',
            '_ga', '_gid', '_gat', '_gtm', 'gtm_debug',
            
            # Social Media
            'ref', 'referer', 'referrer', 'source', 'from', 'via',
            'share', 'shared', 'sharer', 'social', 'sns',
            
            # Session and User Tracking
            'session', 'sessionid', 'session_id', 'sessid', 'sid',
            'user', 'userid', 'user_id', 'uid', 'uuid',
            'visitor', 'visitorid', 'visitor_id', 'vid',
            'track', 'tracking', 'tracker', 'trackid', 'track_id',
            
            # Cache and Performance
            'cache', 'nocache', 'cachebuster', 'cb', 'timestamp', 'ts', 't',
            'version', 'ver', 'v', 'rev', 'revision',
            '_', '__', '___',  # Common cache busters
            
            # Common boring parameters
            'lang', 'language', 'locale', 'l', 'ln',
            'theme', 'skin', 'style', 'css',
            'debug', 'test', 'dev', 'development',
            'format', 'output', 'type', 'ext',
            'redirect', 'return', 'next', 'continue', 'back',
            'mobile', 'desktop', 'app', 'client',
            'noscript', 'nojs', 'js',
            
            # Pagination (sometimes boring)
            'page', 'p', 'offset', 'start', 'begin',
            'limit', 'count', 'size', 'per_page', 'perpage',
            
            # Time-based (often boring)
            'time', 'date', 'datetime', 'created', 'updated',
            'year', 'month', 'day', 'hour', 'minute',
        }
        
        # Load custom boring parameters if provided
        self.boring_params = self._load_boring_parameters()
        
        # Wildcard patterns for boring parameters
        self.boring_patterns = [
            r'^utm_.*',          # All UTM parameters
            r'^ga_.*',           # Google Analytics
            r'^fb_.*',           # Facebook
            r'^ig_.*',           # Instagram
            r'^tw_.*',           # Twitter
            r'^li_.*',           # LinkedIn
            r'.*_tracking$',     # Ending with _tracking
            r'.*_track$',        # Ending with _track
            r'.*_ref$',          # Ending with _ref
            r'.*_source$',       # Ending with _source
            r'.*_campaign$',     # Ending with _campaign
            r'.*_medium$',       # Ending with _medium
            r'^session.*',       # Starting with session
            r'^track.*',         # Starting with track
            r'^cache.*',         # Starting with cache
        ]
        
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.boring_patterns]
    
    def _load_boring_parameters(self) -> Set[str]:
        """Load boring parameters from various sources"""
        boring_params = self.default_boring_params.copy()
        
        # Add custom parameters from command line
        if hasattr(self.args, 'custom_filter') and self.args.custom_filter:
            boring_params.update(self.args.custom_filter)
        
        # Load from file if specified
        if hasattr(self.args, 'boring_list') and self.args.boring_list:
            file_params = self._load_boring_from_file(self.args.boring_list)
            boring_params.update(file_params)
        
        return boring_params
    
    def _load_boring_from_file(self, filename: str) -> Set[str]:
        """Load boring parameters from file"""
        params = set()
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip comments
                        params.add(line.lower())
        except FileNotFoundError:
            if self.args.debug:
                print(f"Warning: Boring parameters file not found: {filename}")
        
        return params
    
    def extract_parameters(self, url: str) -> List[str]:
        """Extract parameters from URL"""
        try:
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query, keep_blank_values=True)
            return list(query_params.keys())
        except:
            return []
    
    def filter_parameters(self, parameters: List[str]) -> List[str]:
        """Filter out boring parameters"""
        if not parameters:
            return []
        
        filtered_params = []
        
        for param in parameters:
            param_lower = param.lower()
            
            # Check against boring parameters set
            if param_lower in self.boring_params:
                continue
            
            # Check against wildcard patterns
            is_boring = False
            for pattern in self.compiled_patterns:
                if pattern.match(param_lower):
                    is_boring = True
                    break
            
            if not is_boring:
                filtered_params.append(param)
        
        return filtered_params
    
    def create_cleaned_url(self, url: str, parameters: List[str], placeholder: str = "FUZZ") -> str:
        """Create cleaned URL with parameter placeholders"""
        try:
            parsed = urlparse(url)
            
            # Create new query with placeholders
            new_query_parts = []
            for param in parameters:
                new_query_parts.append(f"{param}={placeholder}")
            
            new_query = "&".join(new_query_parts)
            
            # Reconstruct URL
            cleaned_parsed = parsed._replace(query=new_query)
            return urlunparse(cleaned_parsed)
            
        except:
            return url
    
    def analyze_parameters(self, all_parameters: List[str]) -> Dict[str, Any]:
        """Analyze parameter patterns and provide insights"""
        from collections import Counter
        
        param_counter = Counter(all_parameters)
        
        # Categorize parameters
        categories = {
            'tracking': [],
            'user_input': [],
            'navigation': [],
            'api': [],
            'other': []
        }
        
        tracking_keywords = ['utm', 'ga', 'track', 'ref', 'source', 'campaign', 'medium']
        navigation_keywords = ['page', 'sort', 'order', 'filter', 'search', 'q', 'query']
        api_keywords = ['id', 'key', 'token', 'api', 'format', 'callback']
        
        for param in param_counter:
            param_lower = param.lower()
            
            if any(keyword in param_lower for keyword in tracking_keywords):
                categories['tracking'].append(param)
            elif any(keyword in param_lower for keyword in navigation_keywords):
                categories['navigation'].append(param)
            elif any(keyword in param_lower for keyword in api_keywords):
                categories['api'].append(param)
            else:
                # Try to determine if it looks like user input
                if len(param) > 2 and not param.lower() in self.boring_params:
                    categories['user_input'].append(param)
                else:
                    categories['other'].append(param)
        
        return {
            'total_unique': len(param_counter),
            'most_common': param_counter.most_common(10),
            'categories': categories,
            'frequency_distribution': dict(param_counter)
        }
    
    def get_interesting_parameters(self, parameters: List[str]) -> List[str]:
        """Get parameters that are likely to be interesting for testing"""
        interesting = []
        
        # Parameters that often indicate vulnerabilities or interesting functionality
        interesting_keywords = [
            'id', 'user', 'admin', 'file', 'path', 'url', 'redirect', 'return',
            'callback', 'jsonp', 'api', 'query', 'search', 'q', 'cmd', 'exec',
            'eval', 'include', 'require', 'import', 'load', 'read', 'write',
            'delete', 'update', 'insert', 'select', 'sql', 'debug', 'test',
            'config', 'setting', 'option', 'param', 'var', 'data', 'input'
        ]
        
        for param in parameters:
            param_lower = param.lower()
            
            # Skip if it's a boring parameter
            if param_lower in self.boring_params:
                continue
            
            # Check if it contains interesting keywords
            if any(keyword in param_lower for keyword in interesting_keywords):
                interesting.append(param)
            # Or if it's a short, custom parameter (likely functional)
            elif len(param) <= 10 and param.isalpha():
                interesting.append(param)
        
        return interesting