# src/config.py
"""
Configuration settings for the Labor Market Segmentation project
"""

# API Settings (loaded from environment variables)
ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"
COUNTRIES = {
    "gb": "United Kingdom",
    "us": "United States"
}

# Job Categories to analyze
JOB_CATEGORIES = [
    {"job_type": "data", "what": "data", "category": "it-jobs"},
    {"job_type": "ai", "what": "ai", "category": "it-jobs" },
    {"job_type": "healthcare", "what": "", "category": "healthcare-nursing-jobs"},
]

# Skills to extract from job descriptions
"""SKILLS_LIST = [
    "python", "sql", "machine learning", "excel", "tableau", "power bi",
    "java", "tensorflow", "pytorch", "nursing", "patient care",
    "healthcare", "data analysis", "statistics", "cloud", "aws", "azure"
    "care", "nurse", "clinical", "medication", "empathy", "communication"
] """

TECH_SKILLS = [
    "python", "sql", "machine learning", "excel", "tableau", "power bi",
    "java", "tensorflow", "pytorch", "data analysis", "statistics", 
    "cloud", "aws", "azure", "r programming", "spark", "hadoop" , 
    "automation", "agent", "artificial intelligence", "ai", "big data", "api",
    "data mining", "data science", "deep learning", "docker", "git", "kubernetes",
    "linux", "nosql", "pandas", "numpy", "scikit-learn", "visualization", "etl", 
    "RAG", "LLM", "large language model", "gpt"
]

HEALTHCARE_SKILLS = [
    "nursing", "patient care", "healthcare", "clinical", "medication",
    "empathy", "communication", "healthcare", "medical", "patient safety",
    "health education", "patient assessment"
]

# Combine all skills for general use
SKILLS_LIST = TECH_SKILLS + HEALTHCARE_SKILLS

# Context words that help identify if a skill is being used in a professional context
TECH_CONTEXT_WORDS = ["programming", "development", "software", "code", "algorithm", "data"]
HEALTHCARE_CONTEXT_WORDS = ["patient", "clinical", "medical", "healthcare", "nursing", "hospital"]


# Clustering parameters
DEFAULT_K = 4
DBSCAN_EPS = 0.5
DBSCAN_MIN_SAMPLES = 5

# Visualization settings
CLUSTER_COLORS = ["red", "blue", "green", "purple", "orange", "darkred"]
UK_CENTER = [54.5, -3]  # Approximate UK center
MAP_ZOOM = 6

# File paths
RAW_DATA_PATH = "data/raw/jobs_raw_full.csv"
SAMPLE_DATA_PATH = "data/raw/jobs_raw_sample.csv"
CLEAN_DATA_PATH = "data/processed/jobs_clean.csv"
CLEAN_SAMPLE_PATH = "data/processed/jobs_clean_sample.csv"
CLUSTER_RESULTS_PATH = "data/processed/jobs_with_clusters.csv"