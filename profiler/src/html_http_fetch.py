import requests
from bs4 import BeautifulSoup

def fetch_headers(domain):
    
    try:
        url = f"https://{domain}"
        r = requests.get(url, timeout=5)

        return {
            "status_code": r.status_code,
            "server": r.headers.get("Server"),
            "x_powered_by": r.headers.get("X-Powered-By"),
            "content_type": r.headers.get("Content-Type"),
            "redirected": True if r.history else False,
            "final_url": r.url
        }

    except Exception as e:
        return {"error": str(e)}

def fetch_html_meta(domain):
    
    try:
        url = f"https://{domain}"
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        
        title = soup.title.string.strip() if soup.title else None

        # Meta description
        description = None
        desc_tag = soup.find("meta", {"name": "description"})
        if desc_tag:
            description = desc_tag.get("content")

        
        keywords = None
        key_tag = soup.find("meta", {"name": "keywords"})
        if key_tag:
            keywords = key_tag.get("content")

        # OpenGraph TITLE
        og_title = None
        og_title_tag = soup.find("meta", property="og:title")
        if og_title_tag:
            og_title = og_title_tag.get("content")

        # OpenGraph DESC
        og_desc = None
        og_desc_tag = soup.find("meta", property="og:description")
        if og_desc_tag:
            og_desc = og_desc_tag.get("content")

        return {
            "title": title,
            "meta_description": description,
            "meta_keywords": keywords,
            "og_title": og_title,
            "og_description": og_desc
        }

    except Exception as e:
        return {"error": str(e)}

def run(domain):
    
    return {
        "headers": fetch_headers(domain),
        "html_meta": fetch_html_meta(domain)
    }

