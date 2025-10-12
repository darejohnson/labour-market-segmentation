# src/data_collection.py

import os
import requests
import pandas as pd
import math
from typing import List, Dict, Optional

def fetch_adzuna_jobs(what: str, category: str, app_id: str, app_key: str, 
                     country: str = "gb", results_per_page: int = 50, 
                     max_pages: int = 20, max_days_old: int = 60) -> List[Dict]:
    """
    Fetch job listings from Adzuna API with pagination handling.
    
    Args:
        what: Job title keywords to search for
        category: Adzuna job category (e.g., 'it-jobs')
        app_id: Adzuna application ID
        app_key: Adzuna application key
        country: Country code (default: 'gb' for UK)
        results_per_page: Number of results per page (max 50)
        max_pages: Maximum number of pages to fetch
        max_days_old: Maximum age of job postings in days
        
    Returns:
        List of job dictionaries
    """
    # Validate credentials
    if not app_id or not app_key:
        raise ValueError("Missing APP_ID or APP_KEY")
    
    jobs = []
    
    try:
        # First request to get total count
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": what,
            "category": category,
            "results_per_page": results_per_page,
            "max_days_old": max_days_old
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        total_count = data.get("count", 0)
        needed_pages = min(math.ceil(total_count / results_per_page), max_pages)
        
        # Collect first page results
        jobs.extend(data.get("results", []))
        
        # Fetch remaining pages
        for page in range(2, needed_pages + 1):
            url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
            response = requests.get(url, params=params, timeout=30)
            if response.status_code != 200:
                break
                
            page_data = response.json().get("results", [])
            if not page_data:
                break
                
            jobs.extend(page_data)
            
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        raise
        
    return jobs

def fetch_multiple_categories(queries: List[Dict], app_id: str, app_key: str) -> pd.DataFrame:
    """
    Fetch jobs from multiple categories and combine into a single DataFrame.
    
    Args:
        queries: List of query dictionaries with 'job_type', 'what', and 'category' keys
        app_id: Adzuna application ID
        app_key: Adzuna application key
        
    Returns:
        DataFrame with all jobs and their types
    """
    all_jobs = []
    
    for query in queries:
        print(f"Fetching {query['job_type']} jobs...")
        
        jobs = fetch_adzuna_jobs(
            what=query["what"],
            category=query["category"],
            app_id=app_id,
            app_key=app_key
        )
        
        # Add job type to each job
        for job in jobs:
            job["job_type"] = query["job_type"]
            
        all_jobs.extend(jobs)
    
    # Create DataFrame and remove duplicates
    df = pd.DataFrame(all_jobs)
    df = df.drop_duplicates(subset="id", keep="first").reset_index(drop=True)
    
    print(f"Fetched {len(df)} unique jobs across all categories")
    return df