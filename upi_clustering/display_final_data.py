import pandas as pd
from tabulate import tabulate


def display_table(df, title="Table"):
    print(f"\n===== {title} =====\n")
    print(tabulate(df, headers="keys", tablefmt="plain", showindex=False))
    print("\n========================\n")


def main():

    # --------------------------
    # LOAD BOTH CSV FILES
    # --------------------------
    clustered = pd.read_csv("data/upi_clustered.csv", engine="python")
    metadata = pd.read_csv("data/upi_metadata.csv", engine="python")

    # --------------------------
    # NORMALIZE UPI COLUMN NAMES
    # --------------------------
    if "upi_id" in clustered.columns:
        clustered = clustered.rename(columns={"upi_id": "UPI"})

    # normalize UPI names
    clustered["UPI"] = clustered["UPI"].astype(str).str.strip()
    metadata["UPI"] = metadata["UPI"].astype(str).str.strip()

    # --------------------------
    # RENAME SOURCE COLUMNS
    # --------------------------
    # cluster source → source_clustered
    if "source" in clustered.columns:
        clustered = clustered.rename(columns={"source": "source_clustered"})
    else:
        clustered["source_clustered"] = ""

    # metadata source → source_meta
    if "Source" in metadata.columns:
        metadata = metadata.rename(columns={"Source": "source_meta"})
    else:
        metadata["source_meta"] = ""

    # --------------------------
    # MERGE
    # --------------------------
    final = pd.merge(clustered, metadata, on="UPI", how="left")

    # --------------------------
    # BUILD FINAL SOURCE FIELD
    # Metadata preferred, fallback to clustered
    # --------------------------
    final["source_meta"] = final["source_meta"].astype(str).str.strip()
    final["source_clustered"] = final["source_clustered"].astype(str).str.strip()

    final["Source"] = final["source_meta"]
    final.loc[final["Source"].isin(["", "nan", "None"]), "Source"] = final["source_clustered"]

    # --------------------------
    # REMOVE TEMP SOURCE COLUMNS
    # --------------------------
    final = final.drop(columns=["source_meta", "source_clustered"], errors="ignore")

    # --------------------------
    # FINAL COLUMN ORDER (Option 2)
    # --------------------------
    metadata_cols = ["UPI", "Amount", "Date", "Scam Type", "State", "Source"]
    cluster_cols = [
        "anomaly_tags", "prefix", "psp", "prefix_length", "digit_ratio",
        "entropy", "has_masking", "looks_like_mobile", "cluster"
    ]

    # combine preserving only columns that exist
    final_cols = [c for c in metadata_cols if c in final.columns] + \
                 [c for c in cluster_cols if c in final.columns]

    final = final[final_cols]

    # --------------------------
    # SAVE CSV
    # --------------------------
    final.to_csv("upi_final.csv", index=False)
    print("Saved merged file as upi_final.csv\n")

    # --------------------------
    # CLUSTER MENU
    # --------------------------
    clusters = sorted([int(c) for c in final["cluster"].dropna().unique()])
    print("===== CLUSTER INFORMATION =====")
    print("Total clusters:", len(clusters))
    print("Clusters:", clusters)
    print("================================")

    print("\nMenu:")
    print("1) Display FULL merged table")
    print("2) Display ONE cluster")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        display_table(final, "FULL MERGED TABLE")
        return

    elif choice == "2":
        cluster_choice = input("Enter cluster number: ").strip()

        if not cluster_choice.isdigit():
            print("Invalid cluster number.")
            return

        cluster_choice = int(cluster_choice)

        if cluster_choice not in clusters:
            print("Cluster does not exist.")
            return

        subset = final[final["cluster"] == cluster_choice]
        display_table(subset, f"Cluster {cluster_choice}")
        return

    else:
        print("Invalid choice.")
        return


if __name__ == "__main__":
    main()

