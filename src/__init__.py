# src/__init__.py
"""
Labor Market Segmentation - Core modules
"""

from .data_collection import fetch_adzuna_jobs, fetch_multiple_categories
from .preprocess_2 import load_data, clean_data, save_clean_data
from .visualize import create_cluster_map, create_pca_plot
from .config import SKILLS_LIST, CLUSTER_COLORS, UK_CENTER

__version__ = "1.0.0"
__author__ = "Dare Johnson"