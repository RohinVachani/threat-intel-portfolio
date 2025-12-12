import requests

def run(domain):
    try:
        url = f"https://crt.sh/?q={domain}&output=json"
        r = requests.get(url, timeout=7)

        if r.status_code != 200:
            return {"error": "crt.sh unavailable"}

        data = r.json()
        subdomains = set()

        for entry in data:
            name = entry.get("name_value")
            if name:
                subdomains.update(name.split("\n"))

        subdomains = sorted(list(subdomains))

        return {
            "count": len(subdomains),
            "subdomains": subdomains
        }

    except Exception as e:
        return {"error": str(e)}

