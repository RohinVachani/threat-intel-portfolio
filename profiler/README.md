# **README — Domain Intelligence Profiler**

**Overview**  
This project is a compact, extensible domain-intelligence pipeline designed to collect and correlate signals that reveal how a domain is configured, maintained, and operated. It performs passive reconnaissance across multiple layers — WHOIS, SSL/TLS, HTTP behaviour, metadata, favicon hashing, robots.txt, and Certificate Transparency logs — and turns them into a structured feature set suitable for analysis or anomaly detection.  
The profiler is intentionally simple, modular, and transparent: every signal is collected through its own script, errors are handled gracefully, and nothing is hidden behind black-box abstractions. The purpose is to demonstrate the ability to design and automate an intelligence workflow end-to-end.  
An optional machine-learning component (`Isolation Forest`) sits on top of this pipeline. Its goal is not to produce a final verdict on whether a domain is malicious, but to show how these engineered features can feed anomaly-detection models.

**Features**

**1. WHOIS Enumeration**  
Extracts:  
- Domain age  
- Registrar  
- Nameservers  
- Privacy usage  
- Registration/expiration timestamps  
Handles redacted, missing, and region-blocked WHOIS with safe fallbacks.

**2. SSL Certificate Analysis**  
Parses the domain’s certificate and extracts:  
- Issuer & trust category  
- Validity window  
- Subject CN  
- Self-signed / mismatched certificate behaviour  
Designed to capture the operational hygiene of a domain, not just certificate validity.

**3. HTTP & HTML Metadata**  
Fetches:  
- Response headers  
- Hosting stack indicators  
- Redirection behaviour  
- Title, meta description/keywords, OpenGraph tags  
Useful for identifying template phishing sites, cloned content, and low-effort scam pages.

**4. Favicon Hashing**  
Computes mmh3 hash of the favicon.  
- Strong signal for clustering related infrastructure  
- Helps identify reused scam kits or shared hosting setups

**5. robots.txt Behaviour**  
Detects:  
- Missing or intentionally empty `robots.txt`  
- Excessive disallow rules (common in scammy deployments)

**6. Certificate Transparency Subdomain Discovery**  
Enumerates subdomains seen in CT logs. Reveals:  
- Infrastructure sprawl  
- Sensitive subdomains accidentally exposed  
- Signs of automated or bulk domain generation

**7. Machine Learning Pipeline (Optional)**  
- `Isolation Forest` model  
- Takes engineered features as input  
- Produces an anomaly score (0–1 scale)  
Used only for illustration — the analysis in the report is independent of ML scores.

**Installation**  
Run these commands in your shell:  
`git clone <repo>`  
`cd profiler`  
`python3 -m venv profiler_env`  
`source profiler_env/bin/activate`  
`pip install -r requirements.txt`

**Usage**

Run profiler without saving features:  
`python3 profiler_main.py <domain>`

Run profiler and update dataset + retrain ML model:  
`python3 profiler_main.py <domain> --save`

**Why This Project Matters**  
This profiler demonstrates the ability to:  
- Build real intelligence pipelines  
- Engineer meaningful signals  
- Automate multi-stage collection  
- Handle unreliable, inconsistent internet data  
- Convert raw data into structured, interpretable features  
- Extend the pipeline into ML-based anomaly detection  
The emphasis is on design, reasoning, and workflow automation, not chasing perfect accuracy.

**Limitations**  
- WHOIS access varies by region and registry  
- CT logs occasionally timeout  
- Favicon and HTML fetches depend on domain uptime  
- ML model intentionally kept minimal  
- Not intended as a production-grade detector  
Each limitation is discussed openly in the full report.

**Directory Structure**  
profiler/  
├── src/  
│   ├── `profiler_main.py`  
│   ├── `whois_lookup.py`  
│   ├── `ssl_fetch.py`  
│   ├── `html_http_fetch.py`  
│   ├── `favicon_hash.py`  
│   ├── `robots_fetch.py`  
│   ├── `crtsh_subdomains.py`  
│   ├── `feature_eng.py`  
│   ├── `dataset_builder.py`  
│   └── `ml_model.py`  
├── data/  
│   └── `profiler_data.csv`  
├── models/  
│   └── `isolation_forest.pkl`  
└── `README.md`

