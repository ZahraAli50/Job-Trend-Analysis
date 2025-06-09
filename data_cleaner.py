import pandas as pd
import json
import os

def load_skills(path='skills.txt'):
    with open(path, 'r') as f:
        return [line.strip().lower() for line in f.readlines()]
    
def clean_data(jobs_raw):
    df = pd.json_normalize(jobs_raw)
    df = df[['title', 'company_name', 'location', 'description']].dropna()
    return df

def extract_skills(df, skills):
    df['skills'] = df['description'].str.lower().apply(
        lambda text: [skill for skill in skills if skill in text])
    return df

if __name__ == "__main__":
    # Load raw JSON data
    with open("data/jobs_raw.json", "r", encoding="utf-8") as f:
        jobs_raw = json.load(f)

    # Load skill keywords
    skills = load_skills("skills.txt")  # Make sure this file exists

    # Clean and enrich data
    df = clean_data(jobs_raw)
    df = extract_skills(df, skills)

    # Save cleaned data
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/jobs_cleaned.csv", index=False)

    print("✅ Cleaned data saved to data/jobs_cleaned.csv")

