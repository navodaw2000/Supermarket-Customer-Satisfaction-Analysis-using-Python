# File: 01_exploratory_data_analysis.py
# Location: notebooks/

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 1. Load cleaned data ---
CLEANED_DATA_PATH = "C:/Users/Chalani/Desktop/Customer_Satisfication/data/processed/responses_cleaned.csv"  # relative path from notebooks
if not os.path.exists(CLEANED_DATA_PATH):
    print(f"❌ File not found: {CLEANED_DATA_PATH}")
    exit()

df = pd.read_csv(CLEANED_DATA_PATH)
print(f"✅ Loaded cleaned data: {len(df)} rows × {len(df.columns)} columns\n")

# --- 2. Basic exploration ---
print("=== First 5 rows ===")
print(df.head(), "\n")

print("=== Info ===")
print(df.info(), "\n")

print("=== Descriptive statistics ===")
print(df.describe(include='all'), "\n")

print("=== Response counts by Province ===")
print(df['province'].value_counts(), "\n")

print("=== Response counts by Supermarket ===")
print(df['supermarket'].value_counts(), "\n")

# --- 3. Set Seaborn style ---
sns.set(style="whitegrid")

# --- 4. Visualization 1: Responses per Province ---
plt.figure(figsize=(8,5))
sns.countplot(data=df, x='province', order=df['province'].value_counts().index)
plt.title("Number of Responses by Province")
plt.xlabel("Province")
plt.ylabel("Number of Responses")
plt.tight_layout()
plt.savefig("../plots/responses_by_province.png")  # save figure
plt.show()

# --- 5. Visualization 2: Average Satisfaction by Supermarket ---
avg_satisfaction = df.groupby('supermarket')['overall_satisfaction'].mean().sort_values()

plt.figure(figsize=(8,5))
sns.barplot(x=avg_satisfaction.index, y=avg_satisfaction.values)
plt.title("Average Overall Satisfaction by Supermarket")
plt.xlabel("Supermarket")
plt.ylabel("Average Satisfaction")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../plots/avg_satisfaction_by_supermarket.png")
plt.show()

# --- 6. Visualization 3: Distribution of Overall Satisfaction ---
plt.figure(figsize=(6,4))
sns.histplot(df['overall_satisfaction'], bins=5, kde=False)
plt.title("Distribution of Overall Satisfaction")
plt.xlabel("Satisfaction Score")
plt.ylabel("Number of Responses")
plt.tight_layout()
plt.savefig("../plots/overall_satisfaction_distribution.png")
plt.show()

