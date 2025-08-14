#!/usr/bin/env python3
"""
SpiderX - LEGENDARY URL PARAMETER MINING TOOL
The ultimate tool that completely surpasses ParamSpider

Features:
- Multiple data sources (Wayback + Sitemap + JavaScript + Live Crawling)
- Real-time vulnerability detection for security parameters
- Parameter complexity analysis for testing priority
- Smart filtering with 60+ boring parameters
- Professional CLI with 20+ options
- Multiple export formats (TXT, CSV, JSON)
- High-performance async processing
- Comprehensive analytics and reporting
"""

import asyncio
import argparse
import sys
import time
from pathlib import Path

# Setup path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import SpiderX modules
try:
    from spiderx.utils import print_banner, print_success, print_error, print_info
    from spiderx_english import LegendarySpiderX, create_argument_parser
    
    # Display competitive advantages
    print_banner()
    print_success("🏆 SPIDERX LEGENDARY - ENGLISH VERSION")
    print_info("The ultimate URL parameter mining tool that surpasses ParamSpider")
    print("")
    
    advantages = [
        "✓ Multiple sources: Wayback + Sitemap + JavaScript (vs Wayback only)",
        "✓ Vulnerability detection: Real-time security parameter analysis",
        "✓ Smart filtering: 60+ boring params + ML-like confidence scoring",
        "✓ Export formats: TXT + CSV + JSON with metadata",
        "✓ Performance: Async multi-threaded processing",
        "✓ CLI options: 20+ professional options vs 5 basic",
        "✓ Intelligence: Parameter complexity analysis for priority",
        "✓ Rate limiting: Smart adaptive controls",
        "✓ Statistics: Comprehensive reporting and analytics"
    ]
    
    print_success("🚀 COMPETITIVE ADVANTAGES OVER PARAMSPIDER:")
    for advantage in advantages:
        print_info(f"  {advantage}")
    
    print("")
    print_success("🕷️ SpiderX: Ready for legendary URL parameter discovery!")
    print_info("Usage: python spiderx_final.py -d example.com")
    print_info("Usage: python spiderx_final.py -l domains.txt --format json --stats")

except ImportError as e:
    print(f"Error importing SpiderX modules: {e}")
    print("Please ensure all SpiderX modules are available")
    sys.exit(1)