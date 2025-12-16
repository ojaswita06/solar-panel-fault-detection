# main.py
import pandas as pd
import pickle
import os

# ------------------ LOAD MODEL ------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "solar_fault_model.pkl")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

model = pickle.load(open(MODEL_PATH, "rb"))

# ------------------ EXPECTED COLUMNS ------------------
EXPECTED_COLUMNS = [
    "DC_POWER",
    "AC_POWER",
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "IRRADIATION"
]

# ------------------ FUNCTIONS ------------------
def load_and_clean(csv_file):
    """Load CSV and validate columns."""
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found at {csv_file}")
    
    df = pd.read_csv(csv_file)
    
    # Check for expected columns
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}")
    
    # Keep only expected columns
    df = df[EXPECTED_COLUMNS]
    df = df.dropna()  # Drop rows with missing data
    return df

def predict_fault(df):
    """Predict faults using the loaded model."""
    predictions = model.predict(df)
    df["fault"] = predictions
    return df
