#!/usr/bin/env python3
"""
SpiderX CLI Entry Point
نقطة دخول أداة SpiderX الأسطورية

Main executable for the legendary SpiderX URL parameter mining tool
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the CLI
from spiderx_cli import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())