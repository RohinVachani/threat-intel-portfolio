import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def load_features():
    df = pd.read_csv("../data/upi_features.csv")
    return df

def build_feature_matrix(df):
    feature_cols = [
        "prefix_length",
        "digit_ratio",
        "entropy",
        "has_masking",
        "looks_like_mobile"
    ]
    X = df[feature_cols].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, feature_cols

def run_kmeans(X_scaled, k=5):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    return labels, kmeans

def reduce_dim(X_scaled):
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(X_scaled)
    return reduced

if __name__ == "__main__":
    df = load_features()

    X_scaled, feature_cols = build_feature_matrix(df)

    labels, kmeans = run_kmeans(X_scaled, k=5)

    df["cluster"] = labels
    df.to_csv("../data/upi_clustered.csv", index=False)
    print("Saved → data/upi_clustered.csv")

    reduced = reduce_dim(X_scaled)

    plt.scatter(reduced[:,0], reduced[:,1], c=labels, cmap="viridis")
    plt.title("UPI Fraud-Pattern Clusters")
    plt.savefig("../data/cluster_plot.png", dpi=300)
    print("Saved → data/cluster_plot.png")

