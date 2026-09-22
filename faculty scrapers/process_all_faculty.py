import os
import re
import glob
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NIT_DIR = BASE_DIR
IIIT_DIR = os.path.join(BASE_DIR, "IIITs")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

STANDARD_COLUMNS = ['Name', 'Institution', 'Department', 'Designation', 'Qualification', 'Email', 'Profile URL']

def is_target_department(dept_str):
    if not dept_str or pd.isna(dept_str):
        return False
    d = str(dept_str).strip().lower()
    
    # Exclude basic sciences, humanities, management, other engineering
    exclude_keywords = [
        'civil', 'mechanical', 'chemical', 'biotech', 'bio eng', 'bio tech', 'biological', 'bioscience', 'biomedical',
        'mining', 'metallurg', 'material', 'ceramic', 'textile', 'architecture', 'arch.', 'planning', 'town',
        'geology', 'earth', 'life science', 'food', 'production', 'aerospace', 'applied mechanics', 'ocean',
        'water resources', 'physics', 'chemistry', 'humanit', 'management', 'business', 'english',
        'social science', 'education', 'disaster', 'community science', 'applied sciences (chemistry)',
        'applied sciences (physics)', 'applied sciences (mathematics)', 'ashm', 'hss', 'shm', 'hmas', 'hbs', 'basic science'
    ]
    
    # Pure mathematics vs mathematics and computing
    if 'math' in d:
        if not any(k in d for k in ['comput', 'cse', 'cs', 'data']):
            return False

    for ex in exclude_keywords:
        if ex in d:
            return False
            
    # Retain circuit & computing keywords
    keep_keywords = [
        'comput', 'cse', 'cs', 'information tech', 'it', 'software',
        'electr', 'ee', 'eee', 'ece', 'electronic', 'telecom', 'communicat',
        'instrument', 'ice', 'eie', 'ai', 'artificial intelligence', 'data science',
        'machine learning', 'dsai', 'aide', 'vlsi', 'robot', 'mechatron',
        'signal processing', 'mca', 'c.a.', 'ca'
    ]
    
    return any(k in d for k in keep_keywords)

print("process_all_faculty module initialized.")
