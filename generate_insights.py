# File: C:\Users\Chalani\Desktop\Customer_Satisfication\src\generate_insights.py

import pandas as pd
import numpy as np
import os

# --- Step 1: Load processed data ---
base_path = r"C:\Users\Chalani\Desktop\Customer_Satisfication"
data_path = os.path.join(base_path, "data", "processed", "responses_cleaned.csv")

df = pd.read_csv(data_path)

# --- Step 2: Basic Information ---
total_responses = len(df)
gender_counts = df['what_is_your_gender?'].value_counts()
age_groups = df['what_is_your_age_group?'].value_counts()

# --- Step 3: Convert text ratings to numeric safely ---
numeric_columns = [
    'overall,_how_satisfied_are_you_with_your_supermarket?',
    'how_likely_are_you_to_recommend_this_supermarket_to_others?',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[product_quality]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[product_availability]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[price_fairness]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[staff_friendliness]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[store_cleanliness]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[checkout_speed]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[parking_convenience]'
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Step 4: Satisfaction & Ratings ---
avg_satisfaction = df['overall_satisfaction'].mean()
avg_recommendation = df['how_likely_are_you_to_recommend_this_supermarket_to_others?'].mean()

rating_columns = [
    'rate_the_following_aspects_of_your_preferred_supermarket:___[product_quality]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[product_availability]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[price_fairness]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[staff_friendliness]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[store_cleanliness]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[checkout_speed]',
    'rate_the_following_aspects_of_your_preferred_supermarket:___[parking_convenience]'
]

avg_ratings = df[rating_columns].mean().sort_values(ascending=False)

# --- Step 5: Complaints Summary ---
if 'have_you_ever_faced_any_issues_or_complaints_at_this_supermarket?' in df.columns:
    complaints = df['have_you_ever_faced_any_issues_or_complaints_at_this_supermarket?'].value_counts()
else:
    complaints = pd.Series(dtype='int64')

# --- Step 6: Loyalty Card Analysis ---
if 'do_you_have_a_loyalty/reward_card_for_this_supermarket?' in df.columns:
    loyalty = df['do_you_have_a_loyalty/reward_card_for_this_supermarket?'].value_counts()
else:
    loyalty = pd.Series(dtype='int64')

# --- Step 7: Create Insights Dictionary ---
insights = {
    "Total Responses": total_responses,
    "Gender Distribution": gender_counts.to_dict(),
    "Age Group Distribution": age_groups.to_dict(),
    "Average Satisfaction Score": round(avg_satisfaction, 2),
    "Average Recommendation Score": round(avg_recommendation, 2),
    "Average Ratings by Aspect": avg_ratings.to_dict(),
    "Complaints Summary": complaints.to_dict(),
    "Loyalty Card Holders": loyalty.to_dict()
}

# --- Step 8: Save insights to CSV file ---
output_dir = os.path.join(base_path, "reports")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "insights_summary.csv")

insights_df = pd.DataFrame({
    "Metric": insights.keys(),
    "Value": [str(v) for v in insights.values()]
})

insights_df.to_csv(output_path, index=False)
print(f"✅ Insights generated successfully and saved to {output_path}")
