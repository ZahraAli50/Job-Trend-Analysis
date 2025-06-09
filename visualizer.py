import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Ensure the output directory exists
os.makedirs("plots", exist_ok=True)

def heatmap_skills_by_city(df, output_path):
    skills_df = df.explode('skills')
    top_skills = (skills_df.groupby(['location', 'skills'])
                  .size().reset_index(name='count'))
    pivot = top_skills.pivot(index='skills', columns='location', values='count').fillna(0)

    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, annot=True, cmap='YlGnBu')
    plt.title('Top Skills by City')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()

def heatmap_skills_by_role(df, output_path):
    df['role'] = df['title'].apply(lambda x: 'Data Scientist' if 'data scientist' in x.lower() else 'Other')
    skills_df = df.explode('skills')
    grouped = skills_df.groupby(['role', 'skills']).size().reset_index(name='count')
    pivot = grouped.pivot(index='skills', columns='role', values='count').fillna(0)

    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, cmap='coolwarm')
    plt.title("Skills vs Role Matrix")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()

def barplot_top_skills(df, output_path):
    top_skills=df.explode('skills').groupby('skills').size().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10,6))
    sns.barplot(x=top_skills.values, y=top_skills.index, palette='viridis')
    plt.title('Top 10 In-Demand Skills Overall')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()
    





# ✅ Main logic: read data and call functions
if __name__ == "__main__":
    # Load cleaned CSV
    df = pd.read_csv("data/jobs_cleaned.csv")

    # Convert skill strings to actual Python lists (if needed)
    df['skills'] = df['skills'].apply(lambda x: eval(x) if isinstance(x, str) else x)

    heatmap_skills_by_city(df, "plots/heatmap_skills_by_city.png")
    heatmap_skills_by_role(df, "plots/heatmap_skills_by_role.png")
    barplot_top_skills(df, 'plots/top_10_skills.png')

    print("✅ Heatmaps saved in plots/ folder.")
    
