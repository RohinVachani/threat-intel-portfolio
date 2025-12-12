import csv
import os

DATASET_PATH = "../data/profiler_data.csv"

def save_features(domain, feature_dict):
    

    
    columns = ["domain"] + list(feature_dict.keys())

    
    new_file = not os.path.exists(DATASET_PATH)

    with open(DATASET_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)

        if new_file:
            writer.writeheader()

        row = {"domain": domain}
        row.update(feature_dict)

        writer.writerow(row)

    return True

