import pandas as pd
import re
import ast
from src.config import TECH_SKILLS, HEALTHCARE_SKILLS, TECH_CONTEXT_WORDS, HEALTHCARE_CONTEXT_WORDS

def extract_skills_advanced(description):
    """
    Advanced skill extraction using multiple techniques
    """
    if pd.isna(description):
        return ""
    
    description_lower = description.lower()
    found_skills = []
    
    # Technique 1: Direct phrase matching for multi-word skills
    for skill in TECH_SKILLS + HEALTHCARE_SKILLS:
        if len(skill.split()) > 1:  # Multi-word skills
            if skill in description_lower:
                found_skills.append(skill)
    
    # Technique 2: Context-aware single word matching
    words = re.findall(r'\b[a-z]+\b', description_lower)  # Extract all words
    
    for word in words:
        # Check if word is a tech skill with tech context
        if word in TECH_SKILLS and any(context in description_lower for context in TECH_CONTEXT_WORDS):
            found_skills.append(word)
        
        # Check if word is a healthcare skill with healthcare context
        if word in HEALTHCARE_SKILLS and any(context in description_lower for context in HEALTHCARE_CONTEXT_WORDS):
            found_skills.append(word)
    
    # Technique 3: Special handling for ambiguous terms
    # Handle "r" specifically - only count if it appears with programming context
    if ' r ' in description_lower or ' r,' in description_lower or 'r/' in description_lower:
        if any(context in description_lower for context in TECH_CONTEXT_WORDS):
            found_skills.append('r programming')
    
    # Remove duplicates and return
    return ' '.join(list(set(found_skills)))

def categorize_job_by_title(title):
    """
    Fallback: Categorize jobs based on title keywords if skill extraction fails
    """
    if pd.isna(title):
        return "unknown"
        
    title_lower = title.lower()
    
    tech_keywords = ["data", "software", "developer", "engineer", "analyst", "python", "java", "programmer", "IT", "technology"]
    healthcare_keywords = ["nurse", "nursing", "care", "health", "medical", "patient", "clinical", "healthcare", "hospital", "doctor"]
    
    tech_count = sum(1 for keyword in tech_keywords if keyword in title_lower)
    healthcare_count = sum(1 for keyword in healthcare_keywords if keyword in title_lower)
    
    if tech_count > healthcare_count:
        return "tech"
    elif healthcare_count > tech_count:
        return "healthcare"
    else:
        return "unknown"

def enhanced_skill_extraction(df):
    """
    Complete skill extraction with fallback
    """
    # First pass with advanced extraction
    print("Performing advanced skill extraction...")
    df['skills_extracted'] = df['description'].apply(extract_skills_advanced)
    
    # Identify rows with no skills found
    no_skills_mask = df['skills_extracted'].str.len() == 0
    print(f"Jobs with no skills after first pass: {no_skills_mask.sum()}")
    
    # Fallback: Use job title categorization for jobs with no skills
    print("Applying fallback categorization...")
    df.loc[no_skills_mask, 'job_category'] = df.loc[no_skills_mask, 'title'].apply(categorize_job_by_title)
    
    # Add default skills based on category
    df.loc[(no_skills_mask) & (df['job_category'] == 'tech'), 'skills_extracted'] = 'general tech skills'
    df.loc[(no_skills_mask) & (df['job_category'] == 'healthcare'), 'skills_extracted'] = 'general healthcare skills'
    df.loc[(no_skills_mask) & (df['job_category'] == 'unknown'), 'skills_extracted'] = 'general skills'
    
    # Clean up temporary column
    if 'job_category' in df.columns:
        df.drop('job_category', axis=1, inplace=True)
    
    print(f"Jobs with no skills after fallback: {(df['skills_extracted'].str.len() == 0).sum()}")
    return df

# Update your clean_data function to use the enhanced skill extraction
def clean_data(df):
    """
    Clean and preprocess the job data with enhanced skill extraction
    """
    # 1. Select only the columns we need
    columns_to_keep = ['title', 'description', 'salary_min', 'salary_max', 'location', 'latitude', 'longitude']
    df = df[columns_to_keep].copy()
    
    # 2. Remove rows with missing values in key columns
    df = df.dropna(subset=['salary_min', 'salary_max', 'latitude', 'longitude'])
    
    # 3. Calculate salary midpoint
    df['salary_mid'] = (df['salary_min'] + df['salary_max']) / 2
    

    # 4. Extract location details
    def extract_location_info(location_str):
        """Extract country, region, county, city from location string"""
        try:
            # Convert string to dictionary
            location_dict = ast.literal_eval(location_str)
            area_list = location_dict.get('area', [])
            
            # Extract values based on position in the list
            country = area_list[0] if len(area_list) > 0 else 'Unknown'
            region = area_list[1] if len(area_list) > 1 else 'Unknown'
            county = area_list[2] if len(area_list) > 2 else 'Unknown'
            city = area_list[3] if len(area_list) > 3 else 'Unknown'
            
            return pd.Series({
                'country': country,
                'region': region,
                'county': county,
                'city': city
            })
        except:
            # If parsing fails, return unknown values
            return pd.Series({
                'country': 'Unknown',
                'region': 'Unknown',
                'county': 'Unknown',
                'city': 'Unknown'
            })

    # Apply the function to extract location info
    location_info = df['location'].apply(extract_location_info)
    
    # 5. Combine the location info with the original dataframe
    df = pd.concat([df, location_info], axis=1)
    
    # 6. Drop the original location column
    df = df.drop('location', axis=1)
    
    # 7. Enhanced skill extraction (NEW)
    df = enhanced_skill_extraction(df)
    
    # 8. Reset index
    df = df.reset_index(drop=True)
    
    return df



def save_clean_data(df, file_path, sample_size=None):
    """Save the cleaned data to a CSV file"""
    if sample_size:
        df = df.sample(n=min(sample_size, len(df)))
    
    df.to_csv(file_path, index=False)