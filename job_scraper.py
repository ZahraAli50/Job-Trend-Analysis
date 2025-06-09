import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def fetch_jobs(keywords, location, pages=2):
    all_jobs=[]
    next_token = None
    for page in range(pages):
        params={
            'engine': 'google_jobs',
            'q': keywords,
            'location': location,
            'api_key' : SERPAPI_API_KEY,
            #'start': pages * 25

        }
        if next_token:
            params["next_page_token"] = next_token
        print("Request params:", params)

        res=requests.get('https://serpapi.com/search', params=params)
        data=res.json()
        print("Raw API response keys:", data.keys())
        if "error" in data:
            print("API error:", data["error"])
            return []

        jobs=data.get('jobs_results', [])
        print(f"Page {page+1} jobs fetched: {len(jobs)}")
        all_jobs.extend(jobs)

    # Create folder if not exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Write JSON to file
    with open('data/jobs_raw.json', 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, indent=2)
    
    return all_jobs

if __name__ == "__main__":
    jobs = fetch_jobs("Engineer", "New York", pages=1)
    print(f"Fetched {len(jobs)} jobs.")


   