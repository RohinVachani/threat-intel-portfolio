import math
from datetime import datetime

def domain_entropy(domain):
    if not domain:
        return 0
    from collections import Counter
    probs = [freq / len(domain) for freq in Counter(domain).values()]
    return -sum(p * math.log2(p) for p in probs)

def digit_ratio(domain):
    if not domain:
        return 0
    digits = sum(c.isdigit() for c in domain)
    return digits / len(domain)


def classify_stack(header):
    if not header:
        return 0

    h = header.lower()

    high_risk = ["php/5", "php/4", "express", "wamp", "xampp", "openresty", "apache/2.2"]
    if any(x in h for x in high_risk):
        return 3

    moderate_risk = ["php/7", "tomcat/8", "apache/2.4", "nginx/1."]
    if any(x in h for x in moderate_risk):
        return 2

    low_risk = ["php/8", "node", "nginx/1.20", "gunicorn", "cloudflare", "fastly", "akamai"]
    if any(x in h for x in low_risk):
        return 1

    return 2


def classify_ssl_issuer(issuer):
    if not issuer:
        return 0
    
    issuer = issuer.lower()

    suspicious = ["unknown", "self-signed", "invalid"]
    if any(x in issuer for x in suspicious):
        return 0

    free_ca = ["let's encrypt", "letsencrypt", "zerossl", "buypass", "actalis"]
    if any(x in issuer for x in free_ca):
        return 1

    cheap = ["sectigo", "rapidssl", "geotrust", "comodoca"]
    if any(x in issuer for x in cheap):
        return 2

    enterprise = ["digicert", "globalsign", "entrust", "amazon trust", "google trust"]
    if any(x in issuer for x in enterprise):
        return 3

    return 1


def extract_features(domain, whois, ssl, headers, meta, favicon, subdomains, robots):
    features = {}

    creation = whois.get("creation_date")
    age_days = 0
    if creation:
        try:
            cd = datetime.strptime(creation, "%Y-%m-%d")
            age_days = (datetime.now() - cd).days
        except:
            age_days = 0
    features["domain_age"] = age_days
    features["whois_privacy"] = 1 if whois.get("whois_privacy") == "Yes" else 0

    registrar = whois.get("registrar")
    if registrar is None:
        registrar = ""
    else:
        registrar = registrar.lower()

    if not registrar:
        reg_cat = 0
    elif any(x in registrar for x in ["godaddy", "namecheap", "enom"]):
        reg_cat = 1
    elif any(x in registrar for x in ["google", "cloudflare", "amazon"]):
        reg_cat = 2
    else:
        reg_cat = 1
    features["registrar_category"] = reg_cat

    ns_list = whois.get("nameservers")
    if not ns_list:
        ns_list = []
    else:
        ns_list = [ns.lower() for ns in ns_list]

    if any("cloudflare" in ns for ns in ns_list):
        features["nameserver_category"] = 2
    elif any("aws" in ns or "amazon" in ns for ns in ns_list):
        features["nameserver_category"] = 2
    elif len(ns_list) == 0:
        features["nameserver_category"] = 0
    else:
        features["nameserver_category"] = 1

    features["ssl_valid_days"] = ssl.get("valid_days", 0)
    features["ssl_issuer_category"] = classify_ssl_issuer(ssl.get("issuer", ""))

    server = headers.get("server", "")
    xpb = headers.get("x_powered_by", "")
    combined_stack = f"{server} {xpb}"

    features["stack_risk"] = classify_stack(combined_stack)

    security_headers = [
        "strict-transport-security",
        "content-security-policy",
        "x-frame-options",
        "x-content-type-options"
    ]
    count = 0
    for h in security_headers:
        if h in (key.lower() for key in headers.keys()):
            count += 1
    features["security_header_score"] = count

    features["metadata_missing"] = 1 if (not meta.get("title") and not meta.get("meta_description")) else 0

    count = subdomains.get("count", 0)
    features["subdomain_count"] = count

    sensitive = 0
    for s in subdomains.get("subdomains", []):
        if any(x in s.lower() for x in ["admin", "cpanel", "panel", "webmail", "staging"]):
            sensitive = 1
            break
    features["has_sensitive_subdomain"] = sensitive

    features["robots_missing"] = 1 if robots.get("status") == "missing" else 0

    features["favicon_present"] = 1 if "favicon_hash" in favicon else 0

    features["entropy"] = domain_entropy(domain)
    features["digit_ratio"] = digit_ratio(domain)
    features["length"] = len(domain)

    return features

