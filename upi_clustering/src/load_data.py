import pandas as pd

def load_upi_data(path="../data/upi_processed2.csv"):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            
            if len(parts) < 2:
                continue
            
            upi_id = parts[0].strip()
            source = parts[1].strip()
            
            # Everything after source = anomaly tags
            anomaly_tags = parts[2:]
            anomaly_tags = [t.strip() for t in anomaly_tags if t.strip() != ""]
            
            rows.append({
                "upi_id": upi_id,
                "source": source,
                "anomaly_tags": anomaly_tags
            })

    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    df = load_upi_data()
    print("Loaded rows:", len(df))
    print(df.head())
    print(df.iloc[0]["anomaly_tags"])

