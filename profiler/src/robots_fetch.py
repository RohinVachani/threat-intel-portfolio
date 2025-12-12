import requests

def run(domain):
    """Fetch and analyze robots.txt"""
    try:
        url = f"https://{domain}/robots.txt"
        r = requests.get(url, timeout=5)

        if r.status_code != 200:
            return {"status": "missing", "content": None}

        content = r.text.strip()

        return {
            "status": "found",
            "content": content[:500]  # limit output
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}

