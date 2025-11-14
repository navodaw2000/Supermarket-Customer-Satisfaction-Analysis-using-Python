import pandas as pd
import os

# --- File paths ---
RAW_DATA_PATH = "C:/Users/Chalani/Desktop/Customer_Satisfication/data/raw/Form_Responses.csv"
CLEANED_DATA_PATH = "C:/Users/Chalani/Desktop/Customer_Satisfication/data/processed/responses_cleaned.csv"

# --- Check if raw file exists ---
if not os.path.exists(RAW_DATA_PATH):
    print(f"❌ File not found: {RAW_DATA_PATH}")
    exit()

# --- Load CSV with UTF-8 fallback ---
try:
    df = pd.read_csv(RAW_DATA_PATH, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(RAW_DATA_PATH, encoding='cp1252')

# --- Replace all double-encoded dashes and en dashes in string columns ---
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.replace('Ã¢â‚¬â€œ', '-', regex=False)  # double-encoded dash
    df[col] = df[col].str.replace('–', '-', regex=False)        # en dash
    df[col] = df[col].str.replace(r'(\d+)-(\d+)', r'\1-\2', regex=True)  # numeric ranges

# --- Rename columns for easier access ---
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")

# --- Remove duplicates ---
df.drop_duplicates(inplace=True)

# --- Replace all missing values with "-" ---
df = df.fillna("-")

# --- Standardize categorical values ---
if "gender" in df.columns:
    df["gender"] = df["gender"].str.strip().str.lower().replace({
        "male": "Male", "m": "Male",
        "female": "Female", "f": "Female"
    })

if "satisfaction" in df.columns:
    df["satisfaction"] = df["satisfaction"].str.strip().str.capitalize()

# --- Convert numeric safely ---
if 'overall_satisfaction' in df.columns:
    df['overall_satisfaction'] = pd.to_numeric(df['overall_satisfaction'], errors='coerce')
    # Replace NaN after conversion with "-"
    df['overall_satisfaction'] = df['overall_satisfaction'].fillna("-")

# --- Ensure folder exists ---
os.makedirs(os.path.dirname(CLEANED_DATA_PATH), exist_ok=True)

# --- Save cleaned CSV ---
if os.path.exists(CLEANED_DATA_PATH):
    os.remove(CLEANED_DATA_PATH)

df.to_csv(CLEANED_DATA_PATH, index=False)

print(f"💾 Cleaned CSV saved to {CLEANED_DATA_PATH}")
print("✅ All missing values replaced with '-' and all double-encoded dashes fixed!")
