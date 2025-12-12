import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_PATH = "../models/isolation_forest.pkl"
DATASET_PATH = "../data/profiler_data.csv"

def train_model():
    if not os.path.exists(DATASET_PATH):
        return

    df = pd.read_csv(DATASET_PATH)
    if df.empty:
        return

    df = df.drop(columns=["domain"])

    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42
    )
    model.fit(df)
    joblib.dump(model, MODEL_PATH)

def predict(features):
    if not os.path.exists(MODEL_PATH):
        return None
    model = joblib.load(MODEL_PATH)
    df = pd.DataFrame([features])
    score = model.score_samples(df)[0]
    anomaly = 1 - ((score + 0.5) / 1.5)
    return anomaly

