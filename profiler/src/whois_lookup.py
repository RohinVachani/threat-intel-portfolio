import whois
from datetime import datetime

def normalize_date(value):
    if isinstance(value, list):
        return value[0]
    return value

def run(domain):
    try:
        w = whois.whois(domain)

        creation = normalize_date(w.creation_date)
        expiry = normalize_date(w.expiration_date)
        updated = normalize_date(w.updated_date)

        registrant_name = w.registrant_name

        info = {
            "domain": domain,
            "creation date": creation,
            "expiration date": expiry,
            "updated date": updated,
            "registrar": w.registrar,
            "nameservers": w.nameservers,
            "whois_privacy": "Yes" if registrant_name is None else "No",
            "registrant name": "-" if registrant_name is None else registrant_name
        }

        return info

    except Exception as e:
        return {"ERROR": str(e)}

