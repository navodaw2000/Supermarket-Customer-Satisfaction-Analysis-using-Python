# File: C:\Users\Chalani\Desktop\Customer_Satisfication\notebooks\02_visualizations.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Step 1: Load cleaned data ---
base_path = r"C:\Users\Chalani\Desktop\Customer_Satisfication"
data_path = os.path.join(base_path, "data", "processed", "responses_cleaned.csv")
df = pd.read_csv(data_path)

# --- Step 2: Create output folder for charts ---
plots_dir = os.path.join(base_path, "plots")
os.makedirs(plots_dir, exist_ok=True)

# --- Step 3: Convert necessary columns to numeric ---
numeric_columns = [
    'overall,_how_satisfied_are_you_with_your_supermarket?',
    'how_likely_are_you_to_recommend_this_supermarket_to_others?'
]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Step 4: Plot gender distribution ---
plt.figure(figsize=(6,4))
sns.countplot(x='what_is_your_gender?', data=df, palette='Set2')
plt.title("Gender Distribution of Respondents")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "gender_distribution.png"))
plt.close()

# --- Step 5: Plot age group distribution ---
plt.figure(figsize=(7,4))
sns.countplot(y='what_is_your_age_group?', data=df, palette='Set3')
plt.title("Age Group Distribution")
plt.xlabel("Count")
plt.ylabel("Age Group")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "age_group_distribution.png"))
plt.close()

# --- Step 6: Average satisfaction per province ---
if 'province' in df.columns:
    province_avg = df.groupby('province')['overall_satisfaction'].mean().sort_values()
    plt.figure(figsize=(8,5))
    province_avg.plot(kind='barh', color='skyblue')
    plt.title("Average Satisfaction by Province")
    plt.xlabel("Average Satisfaction")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "avg_satisfaction_by_province.png"))
    plt.close()

# --- Step 7: Correlation heatmap for ratings ---
rating_cols = [col for col in df.columns if "rate_the_following" in col]
if rating_cols:
    df_ratings = df[rating_cols].apply(pd.to_numeric, errors='coerce')
    plt.figure(figsize=(8,6))
    sns.heatmap(df_ratings.corr(), annot=True, cmap='YlGnBu')
    plt.title("Correlation Between Rating Aspects")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "ratings_correlation_heatmap.png"))
    plt.close()

# --- Step 8: Overall satisfaction vs. recommendation ---
plt.figure(figsize=(6,4))
sns.scatterplot(x='overall_satisfaction',
                y='how_likely_are_you_to_recommend_this_supermarket_to_others?',
                data=df, alpha=0.6, color='purple')
plt.title("Satisfaction vs. Recommendation")
plt.xlabel("Overall Satisfaction")
plt.ylabel("Likelihood to Recommend")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "satisfaction_vs_recommendation.png"))
plt.close()

print(f"✅ All visualizations saved successfully in: {plots_dir}")
