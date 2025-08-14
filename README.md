# SpiderX - Advanced URL Parameter Mining Tool

<div align="center">

```
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ███████╗██████╗ ██╗██████╗ ███████╗██████╗ ██╗  ██╗        ║
    ║   ██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗╚██╗██╔╝        ║
    ║   ███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝ ╚███╔╝         ║
    ║   ╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗ ██╔██╗         ║
    ║   ███████║██║     ██║██████╔╝███████╗██║  ██║██╔╝ ██╗        ║
    ║   ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝        ║
    ║                                                               ║
    ║           Advanced URL Parameter Mining Tool                  ║
    ║              الأداة الأسطورية لاستخراج المعاملات             ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
```

🕷️ **Legendary URL parameter discovery with multiple sources**  
🎯 **Intelligent filtering and comprehensive analysis**  
⚡ **High-performance async processing**

</div>

## Overview

SpiderX is a **legendary and highly competitive** URL parameter mining tool that surpasses existing solutions like ParamSpider by offering:

- **Multiple diverse data sources** for comprehensive coverage
- **Intelligent filtering** with customizable boring parameters and wildcard patterns  
- **Professional CLI** with extensive options and real-time progress tracking
- **High-performance processing** with async operations and automatic retries
- **Flexible export formats** with detailed statistics and analytics
- **Modular architecture** that's easy to extend and customize

## Key Features

### 🎯 **Multiple Data Sources**
- **Wayback Machine**: Enhanced archive mining with multiple endpoints
- **Sitemap.xml**: Recursive sitemap discovery including robots.txt parsing
- **JavaScript Files**: Parameter extraction from JS code (hidden API endpoints)
- **Live Crawling**: Smart crawling of important pages (configurable depth)
- **File Import**: Import URLs from existing files

### 🧠 **Intelligent Filtering**
- **60+ Built-in Boring Parameters**: Comprehensive list of tracking/analytics parameters
- **Wildcard Patterns**: Advanced pattern matching (utm_*, session*, etc.)
- **Customizable Filter Lists**: Add your own boring parameters via file or CLI
- **Complete Filter Control**: Easy enable/disable filtering
- **Parameter Analysis**: Categorize parameters by type (tracking, API, user input)

### 🚀 **Professional CLI**
- **Clear Options**: Intuitive command structure with extensive help
- **Progress Tracking**: Real-time progress bars and status updates  
- **Flexible Output**: Multiple formats (TXT, CSV, JSON) with custom filenames
- **Advanced Configuration**: Proxy support, threading, timeouts, depth control
- **Comprehensive Statistics**: Detailed reports with source breakdown

### ⚡ **High Performance**
- **Async Processing**: Concurrent operations for maximum speed
- **Automatic Retries**: Robust error handling with exponential backoff
- **Memory Efficient**: Stream processing for large datasets
- **Configurable Limits**: Control resource usage and rate limiting

## Installation

```bash
# Clone the repository
git clone https://github.com/yourrepo/spiderx.git
cd spiderx

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x spiderx_cli.py
```

## Quick Start

```bash
# Basic domain scan
python spiderx_cli.py -d example.com

# Multiple domains
python spiderx_cli.py -l domains.txt

# With custom output
python spiderx_cli.py -d example.com -o results.txt

# JSON export with statistics
python spiderx_cli.py -d example.com --format json --stats
```

## Command Line Options

### Target Options
```bash
-d, --domain DOMAIN        Target domain to scan
-l, --list FILE           File containing list of domains  
-i, --import-urls FILE    Import URLs from existing file
```

### Source Selection
```bash
--sources SOURCE          Choose sources: wayback,sitemap,js,crawl,all (default: all)
```

### Output Options
```bash
-o, --output FILE         Output filename (default: auto-generated)
--format FORMAT           Export format: txt,csv,json (default: txt)
--no-save                 Don't save to file, only display results
```

### Filtering Options
```bash
--boring-list FILE        Custom boring parameters file
--no-filter               Disable parameter filtering
--custom-filter PARAMS    Add custom parameters to filter
```

### Advanced Options
```bash
--placeholder TEXT        Parameter placeholder (default: FUZZ)
--proxy URL               HTTP proxy (e.g., http://127.0.0.1:8080)
--threads NUM             Number of concurrent threads (default: 10)
--timeout SEC             Request timeout seconds (default: 30)
--max-urls NUM            Maximum URLs per domain (default: 10000)
```

### Analysis Options
```bash
--top-params N            Show top N most frequent parameters
--stats                   Display detailed statistics
--crawl-depth N           Crawling depth for live sites (default: 2)
--crawl-pages N           Maximum pages to crawl (default: 20)
```

### Debug Options
```bash
-v, --verbose             Verbose output
--debug                   Enable debug mode
```

## Usage Examples

### Basic Usage
```bash
# Single domain scan
python spiderx_cli.py -d example.com

# Multiple domains from file
python spiderx_cli.py -l domains.txt

# Show results on screen without saving
python spiderx_cli.py -d example.com --no-save
```

### Source Selection
```bash
# Only Wayback Machine and Sitemaps
python spiderx_cli.py -d example.com --sources wayback,sitemap

# Only JavaScript file analysis
python spiderx_cli.py -d example.com --sources js

# All sources (default)
python spiderx_cli.py -d example.com --sources all
```

### Filtering Options
```bash
# Use custom boring parameters
python spiderx_cli.py -d example.com --boring-list myboring.txt

# Disable all filtering
python spiderx_cli.py -d example.com --no-filter

# Add specific parameters to filter
python spiderx_cli.py -d example.com --custom-filter sessionid trackid
```

### Export Formats
```bash
# Save as JSON with full metadata
python spiderx_cli.py -d example.com --format json -o results.json

# CSV format for spreadsheet analysis  
python spiderx_cli.py -d example.com --format csv -o results.csv

# Plain text (default)
python spiderx_cli.py -d example.com --format txt -o results.txt
```

### Advanced Analysis
```bash
# Show top 20 parameters with detailed stats
python spiderx_cli.py -d example.com --top-params 20 --stats

# Use proxy with custom placeholder
python spiderx_cli.py -d example.com --proxy http://127.0.0.1:8080 --placeholder "PAYLOAD"

# High-performance scan with custom limits
python spiderx_cli.py -d example.com --threads 20 --max-urls 50000 --timeout 60
```

### File Operations
```bash
# Import existing URLs for processing
python spiderx_cli.py -i existing_urls.txt --format json

# Process domains and export comprehensive report
python spiderx_cli.py -l domains.txt --stats --format json -o comprehensive_scan.json
```

## Output Formats

### TXT Format (Default)
```
# SpiderX Results
# Generated: 2024-08-14 10:30:45
# Total URLs: 1,234
# Unique Parameters: 56
# Domains: example.com

https://example.com/search?q=FUZZ&category=FUZZ
https://example.com/product?id=FUZZ&color=FUZZ
...
```

### CSV Format
```csv
cleaned_url,original_url,domain,source,parameters,param_count
https://example.com/search?q=FUZZ,https://example.com/search?q=test,example.com,wayback,"q",1
...
```

### JSON Format
```json
{
  "metadata": {
    "generated_at": "2024-08-14T10:30:45",
    "tool": "SpiderX",
    "domains": ["example.com"],
    "total_urls": 1234,
    "unique_parameters": 56
  },
  "statistics": {
    "source_breakdown": {
      "wayback": {"total_urls": 800},
      "sitemap": {"total_urls": 200},
      "js": {"total_urls": 150},
      "crawl": {"total_urls": 84}
    },
    "parameter_frequency": {
      "id": 45,
      "q": 38,
      "category": 22
    }
  },
  "urls": [...]
}
```

## Boring Parameters

SpiderX includes **60+ built-in boring parameters** and supports **wildcard patterns**:

### Built-in Categories
- **Tracking**: utm_*, gclid, fbclid, ga_*, _ga, _gid
- **Social Media**: ref, referrer, source, share, social
- **Sessions**: session*, sid, sessionid, userid, uid
- **Cache**: cache*, timestamp, version, rev, _
- **Common**: lang, theme, format, redirect, mobile

### Wildcard Patterns
- `utm_*` - All UTM parameters
- `session*` - All session-related parameters  
- `*_tracking` - Parameters ending with tracking
- `track*` - Parameters starting with track

### Custom Boring Parameters
Create a file with one parameter per line:
```
# myboring.txt
my_tracking_param
custom_session_id
internal_debug
# Comments are supported
```

Use with: `--boring-list myboring.txt`

## Architecture

SpiderX uses a **modular architecture** for easy extension:

```
spiderx/
├── sources/           # Data source modules
│   ├── wayback.py     # Wayback Machine integration
│   ├── sitemap.py     # Sitemap.xml parsing
│   ├── javascript.py  # JS file analysis  
│   └── crawler.py     # Live crawling
├── filters.py         # Parameter filtering logic
├── exporters.py       # Export format handlers
├── utils.py          # Common utilities
└── cli_core.py       # Main CLI logic
```

## Comparison with ParamSpider

| Feature | ParamSpider | SpiderX |
|---------|-------------|---------|
| **Data Sources** | Wayback only | Wayback + Sitemap + JS + Crawling |
| **Filtering** | Basic hardcoded list | 60+ params + wildcards + custom |
| **Export Formats** | TXT only | TXT + CSV + JSON |
| **Statistics** | Basic count | Comprehensive analytics |
| **Performance** | Single-threaded | Async multi-threaded |
| **CLI Options** | Limited | Professional with 20+ options |
| **Error Handling** | Basic | Robust with retries |
| **Customization** | Minimal | Highly customizable |

## Performance Tips

### Optimize for Speed
```bash
# Increase threads for faster processing
python spiderx_cli.py -d example.com --threads 20

# Use specific sources only
python spiderx_cli.py -d example.com --sources wayback,sitemap

# Limit URLs per domain
python spiderx_cli.py -d example.com --max-urls 5000
```

### Handle Large Datasets
```bash
# Use streaming for large scans
python spiderx_cli.py -l large_domains.txt --no-save | tee results.txt

# Process in batches
split -l 100 domains.txt batch_
for batch in batch_*; do
    python spiderx_cli.py -l $batch -o results_$batch.txt
done
```

## Contributing

SpiderX welcomes contributions! Areas for enhancement:

1. **New Data Sources**: Add more URL discovery methods
2. **Advanced Filtering**: Improve parameter categorization
3. **Export Formats**: Add new output options
4. **Performance**: Optimize async operations
5. **Analysis**: Enhanced parameter analysis features

## License

MIT License - See LICENSE file for details.

## Changelog

### v1.0.0 (2024-08-14)
- Initial release with legendary capabilities
- Multiple data sources implementation
- Intelligent filtering with 60+ boring parameters
- Professional CLI with comprehensive options
- High-performance async processing
- Multiple export formats (TXT, CSV, JSON)
- Comprehensive statistics and analytics

---

<div align="center">

**🕷️ SpiderX - The Legendary URL Parameter Mining Tool 🕷️**

*Built for security researchers, bug bounty hunters, and penetration testers who demand the best.*

</div>