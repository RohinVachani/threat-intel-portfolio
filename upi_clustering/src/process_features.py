import pandas as pd
import re
import numpy as np
from load_data import load_upi_data

def extract_psp(upi_id):
    
    if '@' not in upi_id:
        return None
    return upi_id.split("@")[-1].lower().strip()

def extract_prefix(upi_id):
    
    if '@' not in upi_id:
        return None
    return upi_id.split("@")[0].strip()

def entropy(s):
    # Shannon entropy
    if not s:
        return 0
    probs = [s.count(c)/len(s) for c in set(s)]
    return -sum(p * np.log2(p) for p in probs)

def process_features(df):
    df["prefix"] = df["upi_id"].apply(extract_prefix)
    df["psp"] = df["upi_id"].apply(extract_psp)

    df["prefix_length"] = df["prefix"].apply(lambda x: len(x) if isinstance(x,str) else 0)

    df["digit_ratio"] = df["prefix"].apply(
        lambda x: sum(c.isdigit() for c in x) / len(x) if isinstance(x,str) and len(x)>0 else 0
    )

    df["entropy"] = df["prefix"].apply(
        lambda x: entropy(x) if isinstance(x,str) else 0
    )

    df["has_masking"] = df["upi_id"].apply(lambda x: 1 if "*" in x else 0)

    df["looks_like_mobile"] = df["prefix"].apply(
        lambda x: 1 if isinstance(x,str) and re.fullmatch(r"[6-9]\d{9}", x) else 0
    )

    return df

if __name__ == "__main__":
    df = load_upi_data()
    df = process_features(df)

    print(df.head())
    df.to_csv("../data/upi_features.csv", index=False)
    print("\nSaved → data/upi_features.csv")

