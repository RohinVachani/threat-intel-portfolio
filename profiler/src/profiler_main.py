import sys
from whois_lookup import run as whois_run
from ssl_fetch import fetch_certificate as ssl_run
from html_http_fetch import run as http_run
from favicon_hash import run as favicon_run
from robots_fetch import run as robots_run
from crtsh_subdomains import run as crtsh_run

from feature_eng import extract_features
from dataset_builder import save_features
from ml_model import train_model, predict


def main():
    if len(sys.argv) < 2:
        print("Usage: python profiler_main.py <domain> [--save]")
        print("Usage --save : pipe features to ml model")
        sys.exit(1)

    domain = sys.argv[1]
    save_flag = "--save" in sys.argv

    print(f"\n=== PROFILING {domain} ===")

    print("\n=== WHOIS INFO ===")
    whois_info = whois_run(domain)
    for k, v in whois_info.items():
        print(f"{k}: {v}")

    print("\n=== SSL CERTIFICATE ===")
    ssl_info = ssl_run(domain)
    for k, v in ssl_info.items():
        print(f"{k}: {v}")

    print("\n=== HTTP & HTML INFO ===")
    http_info = http_run(domain)

    print("\n--- HEADERS ---")
    for k, v in http_info["headers"].items():
        print(f"{k}: {v}")

    print("\n--- HTML META TAGS ---")
    for k, v in http_info["html_meta"].items():
        print(f"{k}: {v}")

    print("\n=== FAVICON HASH ===")
    fav_info = favicon_run(domain)
    for k, v in fav_info.items():
        print(f"{k}: {v}")

    print("\n=== ROBOTS.TXT ===")
    robots_info = robots_run(domain)
    for k, v in robots_info.items():
        print(f"{k}: {v}")

    print("\n=== CT SUBDOMAINS (crt.sh) ===")
    crt_info = crtsh_run(domain)

    if "error" in crt_info:
        print(f"CT Error: {crt_info['error']}")
    else:
        print(f"Found: {crt_info['count']} subdomains")
        subs = crt_info.get("subdomains", [])
        for sub in subs:
            print(f"- {sub}")

    features = extract_features(
        domain,
        whois_info,
        ssl_info,
        http_info["headers"],
        http_info["html_meta"],
        fav_info,
        crt_info,
        robots_info
    )

    if save_flag:
        print("\n Saving feature vector...")
        save_features(domain, features)
        train_model()
        print(" Saved and model retrained.")

    anomaly = predict(features)
    if anomaly is not None:
        print(f"\n=== ML ANOMALY SCORE ===")
        print(f"Score: {anomaly:.3f}")

if __name__ == "__main__":
    main()

