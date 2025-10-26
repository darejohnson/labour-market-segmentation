# main.py - The single entry point for the whole project

from src.data_collection import fetch_multiple_categories
from src.preprocess import clean_data, save_clean_data
from src.config import JOB_CATEGORIES, CLEAN_DATA_PATH
import pandas as pd

def run_full_pipeline():
    """Run the complete data pipeline"""
    print("Step 1: Fetching data from API...")
    df_raw = fetch_multiple_categories(JOB_CATEGORIES, APP_ID, APP_KEY)
    
    print("Step 2: Cleaning and preprocessing data...")
    df_clean = clean_data(df_raw)
    
    print("Step 3: Saving cleaned data...")
    save_clean_data(df_clean, CLEAN_DATA_PATH)
    
    print("Pipeline completed successfully!")
    return df_clean

if __name__ == "__main__":
    df = run_full_pipeline()