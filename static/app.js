class SpiderXApp {
    constructor() {
        this.currentScanId = null;
        this.currentResults = null;
        this.statusCheckInterval = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupThemeToggle();
    }

    setupEventListeners() {
        // Form submission
        document.getElementById('scanForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.startScan();
        });

        // Filter controls
        document.getElementById('filterUrls').addEventListener('input', () => {
            this.filterResults();
        });

        document.getElementById('filterDomain').addEventListener('change', () => {
            this.filterResults();
        });
    }

    setupThemeToggle() {
        const themeToggle = document.getElementById('themeToggle');
        const currentTheme = localStorage.getItem('theme') || 'light';
        
        this.setTheme(currentTheme);
        
        themeToggle.addEventListener('click', () => {
            const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            this.setTheme(newTheme);
        });
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        const themeToggle = document.getElementById('themeToggle');
        const icon = themeToggle.querySelector('i');
        
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
            themeToggle.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
        } else {
            icon.className = 'fas fa-moon';
            themeToggle.innerHTML = '<i class="fas fa-moon"></i> Dark Mode';
        }
    }

    async startScan() {
        const domains = document.getElementById('domains').value.trim();
        if (!domains) {
            this.showAlert('Please enter at least one domain', 'warning');
            return;
        }

        const domainList = domains.split('\n').map(d => d.trim()).filter(d => d);
        
        const scanRequest = {
            domains: domainList,
            placeholder: document.getElementById('placeholder').value || 'FUZZ',
            proxy: document.getElementById('proxy').value || null,
            filter_extensions: document.getElementById('filterExtensions').checked,
            max_urls_per_domain: parseInt(document.getElementById('maxUrls').value) || 10000,
            include_subdomains: document.getElementById('includeSubdomains').checked
        };

        try {
            this.showLoading(true);
            this.resetUI();

            const response = await fetch('/api/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(scanRequest)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.currentScanId = result.scan_id;
            
            this.showStatusCard();
            this.startStatusPolling();
            
        } catch (error) {
            console.error('Error starting scan:', error);
            this.showAlert('Failed to start scan: ' + error.message, 'danger');
        } finally {
            this.showLoading(false);
        }
    }

    startStatusPolling() {
        if (this.statusCheckInterval) {
            clearInterval(this.statusCheckInterval);
        }

        this.statusCheckInterval = setInterval(async () => {
            try {
                const response = await fetch(`/api/scan/${this.currentScanId}/status`);
                if (response.ok) {
                    const status = await response.json();
                    this.updateStatus(status);

                    if (status.status === 'completed' || status.status === 'failed') {
                        clearInterval(this.statusCheckInterval);
                        
                        if (status.status === 'completed') {
                            await this.loadResults();
                        } else {
                            this.showAlert('Scan failed', 'danger');
                        }
                    }
                }
            } catch (error) {
                console.error('Error checking status:', error);
            }
        }, 2000);
    }

    updateStatus(status) {
        document.getElementById('progressBar').style.width = `${status.progress}%`;
        document.getElementById('progressBar').textContent = `${status.progress}%`;
        
        const statusBadge = document.getElementById('scanStatus');
        statusBadge.textContent = status.status;
        statusBadge.className = `badge bg-${this.getStatusColor(status.status)}`;
        
        document.getElementById('urlsFound').textContent = status.urls_processed || 0;
    }

    getStatusColor(status) {
        switch (status) {
            case 'running': return 'primary';
            case 'completed': return 'success';
            case 'failed': return 'danger';
            default: return 'secondary';
        }
    }

    async loadResults() {
        try {
            const response = await fetch(`/api/scan/${this.currentScanId}/results`);
            if (response.ok) {
                this.currentResults = await response.json();
                this.displayResults();
            }
        } catch (error) {
            console.error('Error loading results:', error);
            this.showAlert('Failed to load results', 'danger');
        }
    }

    displayResults() {
        const results = this.currentResults;
        
        // Update statistics
        document.getElementById('urlsFound').textContent = results.total_urls_found;
        document.getElementById('urlsWithParams').textContent = results.urls_with_parameters;
        document.getElementById('uniqueParams').textContent = results.unique_parameters.length;

        // Populate domain filter
        const domainFilter = document.getElementById('filterDomain');
        domainFilter.innerHTML = '<option value="">All Domains</option>';
        results.domains_scanned.forEach(domain => {
            domainFilter.innerHTML += `<option value="${domain}">${domain}</option>`;
        });

        // Display results table
        this.renderResultsTable(results.urls);

        // Display domain statistics
        this.renderDomainStats(results.domain_stats);

        // Show results card
        document.getElementById('resultsCard').style.display = 'block';
    }

    renderResultsTable(urls) {
        const tbody = document.getElementById('resultsTableBody');
        tbody.innerHTML = '';

        urls.forEach((urlInfo, index) => {
            const row = document.createElement('tr');
            row.setAttribute('data-testid', `row-url-${index}`);
            
            const paramTags = urlInfo.parameters.map(param => 
                `<span class="param-tag">${param}</span>`
            ).join(' ');

            row.innerHTML = `
                <td>${urlInfo.domain}</td>
                <td class="url-text">${this.truncateUrl(urlInfo.cleaned_url)}</td>
                <td>${paramTags}</td>
                <td><span class="badge bg-info">${urlInfo.parameter_count}</span></td>
            `;
            
            tbody.appendChild(row);
        });
    }

    renderDomainStats(domainStats) {
        const container = document.getElementById('domainStats');
        container.innerHTML = '';

        domainStats.forEach(stats => {
            const statCard = document.createElement('div');
            statCard.className = 'stat-card';
            statCard.innerHTML = `
                <div class="row">
                    <div class="col-md-3">
                        <strong>${stats.domain}</strong>
                    </div>
                    <div class="col-md-3">
                        <small>URLs Found: ${stats.total_urls_found}</small>
                    </div>
                    <div class="col-md-3">
                        <small>With Params: ${stats.urls_with_parameters}</small>
                    </div>
                    <div class="col-md-3">
                        <small>Time: ${stats.processing_time.toFixed(2)}s</small>
                    </div>
                </div>
            `;
            container.appendChild(statCard);
        });
    }

    filterResults() {
        if (!this.currentResults) return;

        const urlFilter = document.getElementById('filterUrls').value.toLowerCase();
        const domainFilter = document.getElementById('filterDomain').value;

        let filteredUrls = this.currentResults.urls;

        if (urlFilter) {
            filteredUrls = filteredUrls.filter(url => 
                url.cleaned_url.toLowerCase().includes(urlFilter) ||
                url.parameters.some(param => param.toLowerCase().includes(urlFilter))
            );
        }

        if (domainFilter) {
            filteredUrls = filteredUrls.filter(url => url.domain === domainFilter);
        }

        this.renderResultsTable(filteredUrls);
    }

    truncateUrl(url, maxLength = 80) {
        if (url.length <= maxLength) return url;
        return url.substring(0, maxLength) + '...';
    }

    showStatusCard() {
        document.getElementById('statusCard').style.display = 'block';
        document.getElementById('statusCard').classList.add('fade-in-up');
    }

    resetUI() {
        document.getElementById('statusCard').style.display = 'none';
        document.getElementById('resultsCard').style.display = 'none';
        document.getElementById('progressBar').style.width = '0%';
        document.getElementById('progressBar').textContent = '0%';
        document.getElementById('urlsFound').textContent = '0';
        document.getElementById('urlsWithParams').textContent = '0';
        document.getElementById('uniqueParams').textContent = '0';
    }

    showLoading(show) {
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        if (show) {
            modal.show();
        } else {
            modal.hide();
        }
    }

    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Download functions
async function downloadResults(format) {
    if (!window.spiderApp.currentScanId) {
        window.spiderApp.showAlert('No scan results available', 'warning');
        return;
    }

    try {
        const response = await fetch(`/api/scan/${window.spiderApp.currentScanId}/download/${format}`);
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `spiderx_results.${format}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            throw new Error('Download failed');
        }
    } catch (error) {
        console.error('Download error:', error);
        window.spiderApp.showAlert('Download failed', 'danger');
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.spiderApp = new SpiderXApp();
});