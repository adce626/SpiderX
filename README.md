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
║         Legendary Parameter Discovery & Analysis              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

🕷️ **Legendary multi-source URL parameter discovery**  
🎯 **Intelligent filtering & smart analytics**  
⚡ **Async, high-performance, and beautifully simple**

</div>

---

## What is SpiderX?

**SpiderX** is an advanced, modular, and blazing-fast tool for discovering, analyzing, and exporting URL parameters from many sources.  
It’s designed for bug bounty hunters, pentesters, and web security professionals who need **speed, flexibility, and practical analytics** in one CLI.

---

## 🏆 Features

- **Multi-source mining:** Wayback, Sitemap, JavaScript, live crawling, and URL file import
- **One-command filtering:** Instantly enable, disable, or customize boring parameters (with wildcards!)
- **Live analytics:** See frequency, most interesting parameters, and full stats instantly
- **Export your way:** TXT, CSV, JSON—choose one or all in a single run
- **Session save & resume:** Never lose big scans; pause and continue anytime
- **Professional CLI:** Colorful progress bars, ETA, clear examples, and zero-nonsense usage

---

## 🛠️ Usage Example

```bash
# Legendary scan of a single domain (all sources)
python3 spiderx_cli.py -d example.com

# Scan multiple domains from a list
python3 spiderx_cli.py -l domains.txt

# Focus on Wayback and Sitemap only, save as JSON
python3 spiderx_cli.py -d target.com --sources wayback,sitemap --format json

# Custom boring parameters, show top 10 parameters
python3 spiderx_cli.py -d example.com --boring-list boring.txt --top-params 10

# Import URLs from file and export all formats
python3 spiderx_cli.py -i urls.txt --format txt --format csv --format json
```

---

## ⚡ Command-Line Options

| Option                   | Description                                                     |
|--------------------------|-----------------------------------------------------------------|
| `-d, --domain`           | Target domain to scan                                           |
| `-l, --list`             | File containing list of domains (one per line)                  |
| `-i, --import-urls`      | Import URLs from file for analysis                              |
| `--sources`              | Use specific sources: wayback, sitemap, js, crawl, all          |
| `-o, --output`           | Output file name (default: results_<timestamp>.txt)             |
| `--format`               | Output format: txt, csv, json (choose multiple if needed)       |
| `--no-save`              | Don’t save results, just print to screen                        |
| `--boring-list`          | File with custom boring parameters (supports wildcards)         |
| `--no-filter`            | Disable parameter filtering                                     |
| `--custom-filter`        | Add custom parameters to filter (space/comma separated)         |
| `--placeholder`          | Set parameter placeholder (default: FUZZ)                       |
| `--proxy`                | Use HTTP proxy for requests                                     |
| `--threads`              | Number of threads (default: 10)                                 |
| `--timeout`              | Per-request timeout (default: 30s)                              |
| `--max-urls`             | Maximum URLs per domain (default: 10000)                        |
| `--top-params`           | Show top N most frequent parameters                             |
| `--stats`                | Show detailed statistics                                        |
| `--crawl-depth`          | Crawling depth (default: 2)                                     |
| `--crawl-pages`          | Max pages to crawl (default: 20)                                |
| `--verbose, -v`          | Verbose output                                                  |
| `--debug`                | Debug mode                                                      |
| `-h, --help`             | Show this help message and exit                                 |

---

## 🎉 Output Samples

**TXT**
```
# SpiderX Results — 2025-08-14 09:18 UTC
# Domain: example.com
# Total URLs: 2,345   |   Unique Params: 59

https://example.com/search?q=FUZZ&cat=FUZZ
https://example.com/api?token=FUZZ&type=FUZZ
...
```

**CSV**
```csv
cleaned_url,original_url,domain,source,parameters,param_count
https://example.com/search?q=FUZZ,https://example.com/search?q=test,example.com,wayback,"q",1
...
```

**JSON**
```json
{
  "metadata": {
    "generated_at": "2025-08-14T09:18:13Z",
    "tool": "SpiderX",
    "domains": ["example.com"],
    "total_urls": 2345,
    "unique_parameters": 59
  },
  "statistics": {
    "source_breakdown": {
      "wayback": 1800,
      "sitemap": 300,
      "js": 200,
      "crawl": 45
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

---

## 🤖 Smart Filtering

- **60+ built-in boring parameters** (utm_*, session*, gclid, etc) with wildcard support
- Add/remove your own boring parameters—live—via file or CLI
- Instantly disable filtering for full raw output

---

## 💡 Pro Tips

- Use `--threads 20` for faster results on big domains
- Combine `--sources` for precision: `--sources wayback,sitemap`
- Use `--stats` and `--top-params 20` for instant analytics
- Try `--no-save` and pipe output directly to other tools

---

## 🛡️ Who is SpiderX For?

- Security researchers
- Bug bounty hunters
- Red/purple teamers
- Web developers & QA
- Anyone who wants legendary, reliable, and fast URL parameter discovery!

---

## 📚 License

MIT License.  
Feel free to use, modify, and share!

---

<div align="center">

**🕷️ SpiderX — The Legendary URL Parameter Mining Tool**  
*Built for those who demand the best.*

</div>
