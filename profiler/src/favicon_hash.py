import requests
import base64
import mmh3

def run(domain):
    try:
        favurl = f"https://{domain}/favicon.ico"
        r = requests.get(favurl, timeout=5)

        if r.status_code != 200:
            return {"ERROR": f"ERROR finding the favicon, code = {r.status_code}"}

        fav_64 = base64.b64encode(r.content)
        fav_hash = mmh3.hash(fav_64)

        return {
            "favicon hash": fav_hash,
            "favicon_url": favurl
        }

    except Exception as e:
        return {"ERROR": str(e)}

