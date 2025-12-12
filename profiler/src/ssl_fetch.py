import ssl
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def fetch_certificate(domain):
    try:
        ctx = ssl.create_default_context()
        connection = ctx.wrap_socket(socket.socket(), server_hostname=domain)
        connection.settimeout(5)
        connection.connect((domain, 443))

        der_cert = connection.getpeercert(binary_form=True)
        certificate = parse_certificate(der_cert)
        return extract_info(certificate)

    except Exception as e:
        return {
            "issuer": None,
            "subject": None,
            "not_before": None,
            "not_after": None,
            "valid_days": 0,
            "error": str(e)
        }

def extract_info(cert):
    info = {
        "issuer": cert.issuer.rfc4514_string(),
        "subject": cert.subject.rfc4514_string(),
        "not_before": cert.not_valid_before_utc,
        "not_after": cert.not_valid_after_utc,
        "valid_days": (cert.not_valid_after_utc - cert.not_valid_before_utc).days,
    }
    return info

def parse_certificate(der_bytes):
    cert = x509.load_der_x509_certificate(der_bytes, default_backend())
    return cert

