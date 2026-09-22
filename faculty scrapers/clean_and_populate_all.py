import os
import re
import glob
import json
import time
import urllib.parse
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
    
    # Exclude non-computing and non-circuit branches
    exclude_keywords = [
        'civil', 'mechanical', 'chemical', 'biotech', 'bio eng', 'bio tech', 'biological', 'bioscience', 'biomedical',
        'mining', 'metallurg', 'material', 'ceramic', 'textile', 'architecture', 'arch.', 'planning', 'town',
        'geology', 'earth', 'life science', 'food', 'production', 'aerospace', 'applied mechanics', 'ocean',
        'water resources', 'physics', 'chemistry', 'humanit', 'management', 'business', 'english',
        'social science', 'education', 'disaster', 'community science', 'applied science',
        'ashm', 'hss', 'shm', 'hmas', 'hbs', 'basic science', 'ceesat', 'engineering sciences',
        'science and mathematics', 'bioinformatics', 'cognitive science'
    ]
    for ex in exclude_keywords:
        if ex in d:
            return False
            
    if d == 'engineering':
        return False
        
    # Computational biology (only keep if joint with CSE/ECE)
    if 'computational biology' in d and not any(k in d for k in ['cse', 'ece', 'computer', 'electronic']):
        return False

    # Check mathematics: pure math is excluded; only keep if computing/computational/scientific computing or joint with CSE/ECE
    if 'math' in d:
        if not any(k in d for k in ['comput', 'cse', 'ece', 'data']):
            return False

    # Retain circuit & computing keywords using regex word boundaries / patterns
    keep_patterns = [
        r'comput', r'\bcse\b', r'\bcs\b', r'information\s*tech', r'\bit\b', r'\bict\b',
        r'software', r'electr', r'\bee\b', r'\beee\b', r'\bece\b', r'electronic',
        r'telecom', r'communicat', r'instrument', r'\bice\b', r'\beie\b',
        r'\bai\b', r'artificial\s*intelligence', r'data\s*science', r'machine\s*learning',
        r'\bdsai\b', r'\baide\b', r'vlsi', r'robot', r'mechatron', r'signal\s*processing',
        r'\bmca\b', r'c\.a\.', r'\bca\b'
    ]
    
    for pat in keep_patterns:
        if re.search(pat, d):
            return True
            
    return False

def clean_df(df):
    for col in STANDARD_COLUMNS:
        if col not in df.columns:
            df[col] = "N/A"
    return df[STANDARD_COLUMNS]

# ==========================================
# 1. NIT PROCESSORS
# ==========================================

def process_nit_delhi():
    fpath = os.path.join(NIT_DIR, "NIT_Delhi_Faculty.xlsx")
    df = pd.read_excel(fpath)
    
    delhi_map = {}
    for dept_name, sub in [
        ('Computer Science and Engineering', 'cse'),
        ('Electronics and Communication Engineering', 'ece'),
        ('Electrical Engineering', 'ee')
    ]:
        try:
            r = requests.get(f'https://{sub}.nitdelhi.ac.in/faculty/', headers=HEADERS, verify=False, timeout=8)
            soup = BeautifulSoup(r.text, 'html.parser')
            for a in soup.find_all('a', href=re.compile(r'mailto:.*@nitdelhi\.ac\.in', re.I)):
                raw = a.get('href').replace('mailto:', '').strip().lower()
                emails = re.findall(r'[a-zA-Z0-9_.+-]+@nitdelhi\.ac\.in', raw)
                for em in emails:
                    delhi_map[em] = dept_name
        except Exception as e:
            print(f"Error fetching NIT Delhi {sub}: {e}")
            
    filtered_rows = []
    for _, row in df.iterrows():
        em = str(row['Email']).strip().lower()
        if em in delhi_map:
            r = row.to_dict()
            r['Department'] = delhi_map[em]
            filtered_rows.append(r)
            
    out_df = clean_df(pd.DataFrame(filtered_rows))
    out_df.to_excel(fpath, index=False)
    print(f"[NIT Delhi] Retained {len(out_df)} circuit faculty.")

def process_nit_patna():
    fpath = os.path.join(NIT_DIR, "NIT_Patna_Faculty.xlsx")
    scratch_path = os.path.join(os.path.expanduser("~"), ".gemini/antigravity-ide/brain/5c2efcf1-222d-4409-ba85-11a8561c0760/browser/scratchpad_146hhpt8.md")
    
    patna_members = []
    current_dept = None
    with open(scratch_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("- CSE:"):
                current_dept = "Computer Science and Engineering"
            elif line.startswith("- ECE:"):
                current_dept = "Electronics and Communication Engineering"
            elif line.startswith("- EE:"):
                current_dept = "Electrical Engineering"
            elif line.startswith("- Mechatronics:"):
                current_dept = "Mechatronics and Automation Engineering"
            elif current_dept and re.match(r'^\d+\.\s+', line):
                m = re.search(r'^\d+\.\s+(.*?)\s+\(([a-zA-Z0-9_.+-]+@nitp\.ac\.in)\)', line)
                if m:
                    name = m.group(1).strip()
                    email = m.group(2).strip()
                    patna_members.append({
                        'Name': name,
                        'Institution': 'National Institute of Technology Patna',
                        'Department': current_dept,
                        'Designation': 'Professor' if 'Prof' in name else 'Assistant Professor',
                        'Qualification': 'Ph.D.',
                        'Email': email,
                        'Profile URL': f"https://www.nitp.ac.in/profile/{email}"
                    })
                    
    # Also grab qualifications from existing file if possible
    existing_df = pd.read_excel(fpath)
    qual_map = {}
    desig_map = {}
    for _, row in existing_df.iterrows():
        em = str(row['Email']).strip().lower()
        if pd.notna(row['Qualification']):
            qual_map[em] = row['Qualification']
        if pd.notna(row['Designation']):
            desig_map[em] = row['Designation']
            
    for mem in patna_members:
        em = mem['Email'].lower()
        if em in qual_map:
            mem['Qualification'] = qual_map[em]
        if em in desig_map:
            mem['Designation'] = desig_map[em]
            
    out_df = clean_df(pd.DataFrame(patna_members))
    out_df.to_excel(fpath, index=False)
    print(f"[NIT Patna] Retained {len(out_df)} circuit faculty.")

def process_nit_arunachal():
    fpath = os.path.join(NIT_DIR, "NIT_Arunachal_Pradesh_Faculty.xlsx")
    df = pd.read_excel(fpath)
    
    rows = []
    for _, row in df.iterrows():
        dept = str(row['Department']).strip()
        desig = str(row['Designation']).strip()
        name = str(row['Name']).strip()
        
        # Check if shifted
        if dept == '[email\xa0protected]' or dept == '[email protected]':
            dept = desig
            desig = 'Assistant Professor'
            
        if name == 'Dr. Koj Sambyo':
            dept = 'Computer Science & Engineering'
        elif name == 'Dr Nabam Rich':
            dept = 'Civil Engineering'
            
        if is_target_department(dept):
            r = row.to_dict()
            r['Department'] = dept
            r['Designation'] = desig
            rows.append(r)
            
    out_df = clean_df(pd.DataFrame(rows))
    out_df.to_excel(fpath, index=False)
    print(f"[NIT Arunachal Pradesh] Retained {len(out_df)} circuit faculty.")

def process_standard_nits():
    nit_files = sorted(glob.glob(os.path.join(NIT_DIR, "*.xlsx")))
    for f in nit_files:
        fname = os.path.basename(f)
        if fname in ["NIT_Delhi_Faculty.xlsx", "NIT_Patna_Faculty.xlsx", "NIT_Arunachal_Pradesh_Faculty.xlsx"]:
            continue
            
        df = pd.read_excel(f)
        if fname == "NIT_Trichy_Faculty.xlsx":
            for idx, row in df.iterrows():
                if 'director office' in str(row['Department']).lower():
                    df.at[idx, 'Department'] = 'Computer Science and Engineering'
        # Filter target departments
        filtered = df[df['Department'].apply(is_target_department)].copy()
        
        # Check NIT Warangal non-emails (the 3 rows were in non-circuit Biotech/Mech anyway)
        # Clean emails
        filtered['Email'] = filtered['Email'].astype(str).str.strip()
        filtered = filtered[~filtered['Email'].isin(['nan', 'None', '', '-', '0'])]
        filtered = filtered[filtered['Email'].str.contains('@')]
        
        out_df = clean_df(filtered)
        out_df.to_excel(f, index=False)
        print(f"[{fname}] Filtered to {len(out_df)} circuit faculty.")

# ==========================================
# 2. IIIT PROCESSORS
# ==========================================

def process_iiit_allahabad():
    fpath = os.path.join(IIIT_DIR, "IIIT_Allahabad_Faculty.xlsx")
    df = pd.read_excel(fpath)
    
    def deobfuscate(e):
        if pd.isna(e): return ""
        s = str(e).strip()
        s = re.sub(r'\(\)', '@', s, count=1)
        s = s.replace('()', '.')
        s = re.sub(r'\[at\]', '@', s, flags=re.I)
        s = re.sub(r'\[dot\]', '.', s, flags=re.I)
        return s
        
    df['Email'] = df['Email'].apply(deobfuscate)
    filtered = df[df['Department'].apply(is_target_department)].copy()
    filtered = filtered[filtered['Email'].str.contains('@')]
    
    out_df = clean_df(filtered)
    out_df.to_excel(fpath, index=False)
    print(f"[IIIT Allahabad] Retained {len(out_df)} circuit faculty.")

def process_iiit_naya_raipur():
    fpath = os.path.join(IIIT_DIR, "IIIT_Naya_Raipur_Faculty.xlsx")
    df = pd.read_excel(fpath)
    
    def deobfuscate(e):
        if pd.isna(e): return ""
        s = str(e).strip()
        s = re.sub(r'\[at\]', '@', s, flags=re.I)
        s = re.sub(r'\[dot\]', '.', s, flags=re.I)
        return s
        
    df['Email'] = df['Email'].apply(deobfuscate)
    for idx, row in df.iterrows():
        if 'ruhul' in str(row['Name']).lower():
            df.at[idx, 'Email'] = 'ruhul@iiitnr.edu.in'
            
    filtered = df[df['Department'].apply(is_target_department)].copy()
    filtered = filtered[filtered['Email'].str.contains('@')]
    
    out_df = clean_df(filtered)
    out_df.to_excel(fpath, index=False)
    print(f"[IIIT Naya Raipur] Retained {len(out_df)} circuit faculty.")

def process_iiit_sricity():
    fpath = os.path.join(IIIT_DIR, "IIIT_SriCity_Faculty.xlsx")
    url = "https://www.iiits.ac.in/people/regular-faculty/"
    r = requests.get(url, headers=HEADERS, verify=False, timeout=12)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    profile_links = set([a.get('href') for a in soup.find_all('a', href=True) if '/people/regular-faculty/' in a.get('href') and a.get('href') != url])
    
    rows = []
    for link in sorted(profile_links):
        try:
            rp = requests.get(link, headers=HEADERS, verify=False, timeout=8)
            sp = BeautifulSoup(rp.text, 'html.parser')
            
            # Name
            h1 = sp.find('h1') or sp.find(['h2', 'h3'])
            name = h1.get_text(strip=True) if h1 else link.rstrip('/').split('/')[-1].replace('-', ' ').title()
            
            # Email
            emails = re.findall(r'[a-zA-Z0-9_.+-]+@iiits\.in', rp.text)
            emails = [e for e in emails if not any(x in e for x in ['contact', 'info', 'career'])]
            email = emails[0] if emails else "N/A"
            
            # Department / Designation
            text = sp.get_text()
            dept = "Computer Science & Engineering"
            if "electronics and communication" in text.lower() or "ece" in text.lower():
                dept = "Electronics and Communication Engineering"
            elif "basic science" in text.lower() or "humanities" in text.lower() or "mathematics" in text.lower():
                dept = "Basic Sciences and Humanities"
                
            desig = "Assistant Professor"
            for d in ["Professor", "Associate Professor", "Assistant Professor", "Director"]:
                if d in text:
                    desig = d
                    break
                    
            if is_target_department(dept) and '@' in email:
                rows.append({
                    'Name': name,
                    'Institution': 'IIIT Sri City',
                    'Department': dept,
                    'Designation': desig,
                    'Qualification': 'Ph.D.',
                    'Email': email,
                    'Profile URL': link
                })
        except Exception as e:
            pass
            
    out_df = clean_df(pd.DataFrame(rows)).drop_duplicates(subset=['Email'])
    out_df.to_excel(fpath, index=False)
    print(f"[IIIT Sri City] Scraped and retained {len(out_df)} circuit faculty.")

def process_iiitdm_kurnool():
    fpath = os.path.join(IIIT_DIR, "IIITDM_Kurnool_Faculty.xlsx")
    
    kurnool_faculty = [
        {'Name': 'Dr. SHOUNAK CHAKRABORTY', 'Institution': 'IIITDM Kurnool', 'Department': 'Computer Science and Engineering', 'Designation': 'Assistant Professor', 'Qualification': 'Ph.D. IIIT Guwahati', 'Email': 'shounak@iiitk.ac.in', 'Profile URL': 'https://iiitk.ac.in/faculty'},
        {'Name': 'Dr. P. Ranga Babu', 'Institution': 'IIITDM Kurnool', 'Department': 'Electronics and Communication Engineering', 'Designation': 'Associate Professor', 'Qualification': 'Ph.D. University of Hyderabad', 'Email': 'p.rangababu@iiitk.ac.in', 'Profile URL': 'https://iiitk.ac.in/faculty'},
        {'Name': 'Dr. NARESH BABU MUPPALANENI', 'Institution': 'IIITDM Kurnool', 'Department': 'Computer Science and Engineering', 'Designation': 'Associate Professor', 'Qualification': 'Ph.D.', 'Email': 'nareshbabu@iiitk.ac.in', 'Profile URL': 'https://iiitk.ac.in/faculty'},
        {'Name': 'Prof. V. Siva Rama Krishnaiah', 'Institution': 'IIITDM Kurnool', 'Department': 'Computer Science and Engineering', 'Designation': 'Professor', 'Qualification': 'Ph.D. IIT Delhi', 'Email': 'vsrk@iiitk.ac.in', 'Profile URL': 'https://iiitk.ac.in/faculty'},
        {'Name': 'Dr. Valluri Siva Prasad', 'Institution': 'IIITDM Kurnool', 'Department': 'Electronics and Communication Engineering', 'Designation': 'Assistant Professor & HOD', 'Qualification': 'Ph.D.', 'Email': 'vsp@iiitk.ac.in', 'Profile URL': 'https://iiitk.ac.in/faculty'},
        {'Name': 'Dr. Anil Kumar R', 'Institution': 'IIITDM Kurnool', 'Department': 'Computer Science and Engineering', 'Designation': 'Assistant Professor', 'Qualification': 'Ph.D.', 'Email': 'anilkumar.r@iiitk.ac.in', 'Profile URL': 'https://iiitk.ac.in/faculty'},
        {'Name': 'Dr. K. Nagaraju', 'Institution': 'IIITDM Kurnool', 'Department': 'Computer Science and Engineering', 'Designation': 'Assistant Professor', 'Qualification': 'Ph.D.', 'Email': 'knagaraju@iiitk.ac.in', 'Profile URL': 'https://iiitk.ac.in/faculty'},
        {'Name': 'Dr. R. Praneetha Sree', 'Institution': 'IIITDM Kurnool', 'Department': 'Computer Science and Engineering', 'Designation': 'Assistant Professor', 'Qualification': 'Ph.D. NIT Warangal', 'Email': 'rpraneethasree.it@nitrr.ac.in', 'Profile URL': 'https://iiitk.ac.in/faculty'},
        {'Name': 'Dr. K. Krishna Naik', 'Institution': 'IIITDM Kurnool', 'Department': 'Electronics and Communication Engineering', 'Designation': 'Assistant Professor', 'Qualification': 'Ph.D.', 'Email': 'krishnanaik@iiitk.ac.in', 'Profile URL': 'https://iiitk.ac.in/faculty'},
        {'Name': 'Dr. Eswaramoorthy K. V.', 'Institution': 'IIITDM Kurnool', 'Department': 'Electronics and Communication Engineering', 'Designation': 'Assistant Professor', 'Qualification': 'Ph.D.', 'Email': 'eswaramoorthykv@iiitk.ac.in', 'Profile URL': 'https://iiitk.ac.in/faculty'},
        {'Name': 'Dr. Mohamed Asan Basiri M.', 'Institution': 'IIITDM Kurnool', 'Department': 'Electronics and Communication Engineering', 'Designation': 'Assistant Professor', 'Qualification': 'Ph.D.', 'Email': 'asan@iiitk.ac.in', 'Profile URL': 'https://iiitk.ac.in/faculty'}
    ]
    
    out_df = clean_df(pd.DataFrame(kurnool_faculty))
    out_df.to_excel(fpath, index=False)
    print(f"[IIITDM Kurnool] Populated and retained {len(out_df)} circuit faculty.")

def process_iiit_dharwad():
    fpath = os.path.join(IIIT_DIR, "IIIT_Dharwad_Faculty.xlsx")
    url = "https://iiitdwd.ac.in/academics/faculty/"
    try:
        r = requests.get(url, headers=HEADERS, verify=False, timeout=12)
        soup = BeautifulSoup(r.text, 'html.parser')
        cards = soup.find_all('div', class_=lambda c: c and 'rounded-lg' in c and 'shadow-sm' in c)
    except Exception as e:
        print(f"Error fetching IIIT Dharwad: {e}")
        cards = []
        
    rows = []
    for card in cards:
        parts = [p.strip() for p in card.get_text(separator=' | ', strip=True).split('|') if p.strip()]
        if not parts:
            continue
        name = parts[0]
        
        dept = None
        for p in parts:
            if 'Computer Science' in p:
                dept = 'Computer Science & Engineering'
                break
            elif 'Electronics' in p:
                dept = 'Electronics and Communication Engineering'
                break
            elif 'Data Science' in p:
                dept = 'Data Science and Artificial Intelligence'
                break
                
        if not dept:
            continue
            
        desig = "Assistant Professor"
        for p in parts:
            if any(t in p.lower() for t in ['assistant professor', 'associate professor', 'professor', 'director']):
                desig = p
                break
        
        email = ""
        mailto = card.find('a', href=re.compile(r'mailto:.*@iiitdwd\.ac\.in', re.I))
        if mailto:
            email = mailto.get('href').replace('mailto:', '').strip().lower()
        if not email:
            for p in parts:
                em = re.findall(r'[a-zA-Z0-9_.+-]+@iiitdwd\.ac\.in', p)
                if em:
                    email = em[0].lower()
                    break
            
        qual = "Ph.D."
        for p in parts:
            if 'Ph.D' in p or 'PhD' in p:
                qual = p
                break
                
        profile_link = url
        site_link = card.find('a', href=re.compile(r'sites\.google\.com|iiitdwd\.ac\.in'))
        if site_link:
            profile_link = site_link.get('href')
            
        if is_target_department(dept) and '@' in email:
            rows.append({
                'Name': name,
                'Institution': 'IIIT Dharwad',
                'Department': dept,
                'Designation': desig,
                'Qualification': qual,
                'Email': email,
                'Profile URL': profile_link
            })
            
    if rows:
        out_df = clean_df(pd.DataFrame(rows)).drop_duplicates(subset=['Email'])
        out_df.to_excel(fpath, index=False)
        print(f"[IIIT Dharwad] Scraped and retained {len(out_df)} circuit faculty.")

def process_iiit_kottayam():
    fpath = os.path.join(IIIT_DIR, "IIIT_Kottayam_Faculty.xlsx")
    js_url = "https://www.iiitkottayam.ac.in/scripts/controllers/faculty.ctrl.js"
    t = requests.get(js_url, headers=HEADERS, verify=False, timeout=10).text
    
    # Extract faculty items using regex matching
    pattern = re.compile(r"\{\s*name:\s*['\"]([^'\"]+)['\"].*?keypoint:\s*['\"]([^'\"]*)['\"].*?designation:\s*['\"]([^'\"]*)['\"].*?email:\s*['\"]([^'\"]+)['\"]", re.DOTALL)
    
    rows = []
    for match in pattern.finditer(t):
        name = match.group(1).strip()
        keypoint = match.group(2).strip()
        desig = match.group(3).strip()
        raw_email = match.group(4).strip()
        
        email = raw_email.replace(' at ', '@').replace(' dot ', '.').strip()
        
        # Determine department based on designation, keypoint, or area
        dept = "Computer Science and Engineering"
        full_blob = t[max(0, match.start()-100):min(len(t), match.end()+300)].lower()
        if any(k in full_blob for k in ['electronic', 'ece', 'signal', 'vlsi', 'communication']):
            dept = "Electronics and Communication Engineering"
        elif any(k in full_blob for k in ['humanities', 'physics', 'chemistry', 'english', 'mathematics']):
            dept = "Basic Sciences & Humanities"
            
        if is_target_department(dept) and '@' in email:
            rows.append({
                'Name': name,
                'Institution': 'IIIT Kottayam',
                'Department': dept,
                'Designation': desig if desig else 'Faculty',
                'Qualification': keypoint if keypoint else 'Ph.D.',
                'Email': email,
                'Profile URL': 'https://www.iiitkottayam.ac.in/#!/faculty'
            })
            
    out_df = clean_df(pd.DataFrame(rows)).drop_duplicates(subset=['Email'])
    out_df.to_excel(fpath, index=False)
    print(f"[IIIT Kottayam] Parsed and retained {len(out_df)} circuit faculty.")

def process_iiit_lucknow():
    fpath = os.path.join(IIIT_DIR, "IIIT_Lucknow_Faculty.xlsx")
    url = "https://iiitl.ac.in/index.php/faculty/"
    r = requests.get(url, headers=HEADERS, verify=False, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    def decode_cf(cf_str):
        k = int(cf_str[:2], 16)
        return ''.join([chr(int(cf_str[i:i+2], 16) ^ k) for i in range(2, len(cf_str), 2)])
        
    cards = soup.find_all('div', class_=lambda c: c and 'personnel' in str(c).lower()) or soup.find_all('div', class_='team-member')
    if not cards:
        # Parent containers of data-cfemail
        cards = [cf.find_parent('div', class_=lambda c: c and any(k in str(c).lower() for k in ['card', 'item', 'box', 'col', 'member'])) for cf in soup.find_all(attrs={'data-cfemail': True})]
        
    rows = []
    cf_elements = soup.find_all(attrs={'data-cfemail': True})
    for cf in cf_elements:
        email = decode_cf(cf.get('data-cfemail')).strip().lower()
        parent = cf.find_parent('div', class_=lambda c: c and any(k in str(c).lower() for k in ['content', 'inner', 'card', 'box', 'member'])) or cf.find_parent('div')
        
        name = "Faculty"
        desig = "Assistant Professor"
        qual = "Ph.D."
        profile_url = url
        
        if parent:
            title_el = parent.find(['h2', 'h3', 'h4', 'h5', 'a', 'strong'])
            if title_el:
                name = title_el.get_text(strip=True)
            link = parent.find('a', href=re.compile(r'/personnel/'))
            if link:
                profile_url = link.get('href')
                if not name or name == 'Faculty':
                    name = link.get_text(strip=True)
                    
        dept = "Information Technology & Computer Science"
        if '@' in email and is_target_department(dept):
            rows.append({
                'Name': name,
                'Institution': 'IIIT Lucknow',
                'Department': dept,
                'Designation': desig,
                'Qualification': qual,
                'Email': email,
                'Profile URL': profile_url
            })
            
    out_df = clean_df(pd.DataFrame(rows)).drop_duplicates(subset=['Email'])
    out_df.to_excel(fpath, index=False)
    print(f"[IIIT Lucknow] Decoded and retained {len(out_df)} circuit faculty.")

def process_iiit_vadodara():
    fpath = os.path.join(IIIT_DIR, "IIIT_Vadodara_Faculty.xlsx")
    cache_path = os.path.join(BASE_DIR, "cache", "3b63c85a595fd49c62ee59cc42bc835a.html")
    with open(cache_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    rows = []
    for p in soup.find_all('p', class_=lambda c: c and 'display-8' in str(c)):
        t = p.get_text()
        if any(k in t for k in ['[at]', '[dot]', '@']):
            email = t.replace('Contact', '').strip()
            email = email.replace('[under score]', '_').replace('[underscore]', '_')
            email = email.replace('[at]', '@').replace('[dot]', '.').replace(' ', '').strip().lower()
            
            # Parent card
            card = p.find_parent('div', class_=lambda c: c and 'card' in str(c).lower()) or p.find_parent('div')
            name = "Faculty"
            desig = "Assistant Professor"
            qual = "Ph.D."
            dept = "Computer Science & Engineering"
            
            if card:
                card_text = card.get_text(separator=' | ', strip=True)
                title = card.find(['h2', 'h3', 'h4', 'h5'])
                if title:
                    name = title.get_text(strip=True)
                if 'electronics' in card_text.lower() or 'ece' in card_text.lower():
                    dept = "Electronics & Communication Engineering"
                    
            if is_target_department(dept) and '@' in email:
                rows.append({
                    'Name': name,
                    'Institution': 'IIIT Vadodara',
                    'Department': dept,
                    'Designation': desig,
                    'Qualification': qual,
                    'Email': email,
                    'Profile URL': 'https://iiitvadodara.ac.in/faculty.php'
                })
                
    out_df = clean_df(pd.DataFrame(rows)).drop_duplicates(subset=['Email'])
    out_df.to_excel(fpath, index=False)
    print(f"[IIIT Vadodara] Deobfuscated and retained {len(out_df)} circuit faculty.")

def process_iiit_una():
    fpath = os.path.join(IIIT_DIR, "IIIT_Una_Faculty.xlsx")
    api_url = "https://api.iiitu.ac.in/api/faculty/allData"
    r = requests.get(api_url, headers=HEADERS, verify=False, timeout=10)
    data = r.json()
    
    rows = []
    for item in data:
        dept = str(item.get('department', '')).upper()
        if dept in ['SOC', 'SOE', 'CSE', 'ECE', 'IT']:
            dept_full = "School of Computing (CSE)" if dept in ['SOC', 'CSE'] else "School of Electronics (ECE)"
            rows.append({
                'Name': item.get('name', 'Faculty'),
                'Institution': 'IIIT Una',
                'Department': dept_full,
                'Designation': item.get('designation', 'Assistant Professor'),
                'Qualification': 'Ph.D.',
                'Email': item.get('email', '').strip().lower(),
                'Profile URL': f"https://iiitu.ac.in/schools/{dept}/faculty/{item.get('_id', '')}"
            })
            
    out_df = clean_df(pd.DataFrame(rows)).drop_duplicates(subset=['Email'])
    out_df.to_excel(fpath, index=False)
    print(f"[IIIT Una] Extracted and retained {len(out_df)} circuit faculty from API.")

def process_iiit_sonepat():
    fpath = os.path.join(IIIT_DIR, "IIIT_Sonepat_Faculty.xlsx")
    api_url = "http://www.iiitsonepat.ac.in/api/faculty"
    r = requests.get(api_url, headers=HEADERS, timeout=10)
    data = r.json()
    
    rows = []
    for item in data:
        raw_email = str(item.get('email', ''))
        email = raw_email.replace('[at]', '@').replace('[dot]', '.').strip().lower()
        dept = item.get('department', 'Computer Science and Engineering')
        if is_target_department(dept) and '@' in email:
            rows.append({
                'Name': item.get('name', 'Faculty'),
                'Institution': 'IIIT Sonepat',
                'Department': dept,
                'Designation': item.get('designation', 'Assistant Professor'),
                'Qualification': 'Ph.D.',
                'Email': email,
                'Profile URL': 'http://www.iiitsonepat.ac.in'
            })
            
    out_df = clean_df(pd.DataFrame(rows)).drop_duplicates(subset=['Email'])
    out_df.to_excel(fpath, index=False)
    print(f"[IIIT Sonepat] Extracted and retained {len(out_df)} circuit faculty from API.")

def process_iiitm_gwalior():
    fpath = os.path.join(IIIT_DIR, "IIITM_Gwalior_Faculty.xlsx")
    url = "https://iiitm.ac.in/staff"
    r = requests.get(url, headers=HEADERS, verify=False, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    links = [a.get('href') for a in soup.find_all('a', href=True) if '/staff/faculty/' in a.get('href')]
    links = sorted(list(set(links)))
    
    existing_df = pd.read_excel(fpath)
    # Filter out Management and Engineering Sciences
    filtered_existing = existing_df[existing_df['Department'].apply(is_target_department)].copy()
    
    # Scrape email for each faculty profile
    email_map = {}
    for link in links:
        try:
            full_link = link if link.startswith('http') else f"https://iiitm.ac.in{link}"
            rp = requests.get(full_link, headers=HEADERS, verify=False, timeout=6)
            emails = re.findall(r'[a-zA-Z0-9_.+-]+@iiitm\.ac\.in', rp.text)
            emails = [e.lower() for e in emails if e.lower() not in ['wim@iiitm.ac.in', 'info@iiitm.ac.in', 'director@iiitm.ac.in']]
            if emails:
                slug = link.rstrip('/').split('/')[-1]
                email_map[slug] = emails[0]
        except Exception:
            pass
            
    rows = []
    for _, row in filtered_existing.iterrows():
        name = row['Name']
        r = row.to_dict()
        # match slug
        for slug, em in email_map.items():
            clean_slug = slug.replace('prof-', '').replace('dr-', '').replace('-', ' ')
            if any(part in clean_slug for part in name.lower().split()[-2:]):
                r['Email'] = em
                r['Profile URL'] = f"https://iiitm.ac.in/staff/faculty/{slug}"
                break
        if '@' in str(r.get('Email', '')):
            rows.append(r)
            
    out_df = clean_df(pd.DataFrame(rows)).drop_duplicates(subset=['Email', 'Name'])
    out_df.to_excel(fpath, index=False)
    print(f"[IIITM Gwalior] Populated and retained {len(out_df)} circuit faculty.")

def process_iiit_manipur():
    fpath = os.path.join(IIIT_DIR, "IIIT_Manipur_Faculty.xlsx")
    url = "http://iiitmanipur.ac.in/pages/people/staffTeaching.php"
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    rows = []
    items = soup.find_all('div', class_='itemN')
    for item in items:
        text = item.get_text(separator=' | ', strip=True)
        m_email = re.search(r'([a-zA-Z0-9_.+-]+\[at\]iiitmanipur\[dot\]ac\[dot\]in)', text, re.I)
        if m_email:
            email = m_email.group(1).replace('[at]', '@').replace('[dot]', '.').strip().lower()
            strong = item.find('strong')
            name = strong.get_text(strip=True) if strong else "Faculty"
            dept = "Computer Science & Engineering"
            if "ece" in text.lower():
                dept = "Electronics and Communication Engineering"
            elif "hbs" in text.lower() or "physics" in text.lower() or "mathematics" in text.lower():
                dept = "Basic Sciences and Humanities"
                
            if is_target_department(dept) and '@' in email:
                rows.append({
                    'Name': name,
                    'Institution': 'IIIT Manipur',
                    'Department': dept,
                    'Designation': 'Assistant Professor',
                    'Qualification': 'Ph.D.',
                    'Email': email,
                    'Profile URL': url
                })
                
    out_df = clean_df(pd.DataFrame(rows)).drop_duplicates(subset=['Email'])
    out_df.to_excel(fpath, index=False)
    print(f"[IIIT Manipur] Deobfuscated and retained {len(out_df)} circuit faculty.")

def process_iiit_raichur():
    fpath = os.path.join(IIIT_DIR, "IIIT_Raichur_Faculty.xlsx")
    df = pd.read_excel(fpath)
    
    rows = []
    for _, row in df.iterrows():
        dept = str(row['Department']).strip()
        url = str(row['Profile URL']).strip()
        if is_target_department(dept):
            r = row.to_dict()
            try:
                rp = requests.get(url, headers=HEADERS, verify=False, timeout=6)
                emails = re.findall(r'[a-zA-Z0-9_.+-]+@iiitr\.ac\.in', rp.text)
                emails = [e.lower() for e in emails if e.lower() not in ['info@iiitr.ac.in', 'director@iiitr.ac.in']]
                if emails:
                    r['Email'] = emails[0]
            except Exception:
                pass
            if '@' in str(r.get('Email', '')):
                rows.append(r)
                
    out_df = clean_df(pd.DataFrame(rows)).drop_duplicates(subset=['Email'])
    out_df.to_excel(fpath, index=False)
    print(f"[IIIT Raichur] Populated and retained {len(out_df)} circuit faculty.")

def process_iiit_agartala():
    fpath = os.path.join(IIIT_DIR, "IIIT_Agartala_Faculty.xlsx")
    df = pd.read_excel(fpath)
    
    agartala_map = {
        'Ashim Saha': 'ashim.saha.cse@faculty.nita.ac.in',
        'Mrinal Kanti Deb Barma': 'mrinal.barma.cse@faculty.nita.ac.in',
        'Ranjita Das': 'ranjita.das.cse@faculty.nita.ac.in',
        'Awnish Kumar': 'awnish.kumar.cse@faculty.nita.ac.in',
        'Kamanasish Bhattacharjee': 'kamanasish.bhattacharjee.cse@faculty.nita.ac.in',
        'Rajesh Basak': 'rajesh.basak.cse@faculty.nita.ac.in',
        'Abhishek Hazra': 'abhishek.hazra.cse@faculty.nita.ac.in',
        'Sushmita Sharma': 'sushmita.sharma@iiitagartala.ac.in',
        'Syeda Zeenat Marshoodulla': 'syeda.zeenat@gmail.com',
        'Prarthana Dutta': 'prarthana.dutta01@gmail.com'
    }
    
    rows = []
    for _, row in df.iterrows():
        r = row.to_dict()
        for k, em in agartala_map.items():
            if k in r['Name']:
                r['Email'] = em
                break
        rows.append(r)
        
    out_df = clean_df(pd.DataFrame(rows))
    out_df.to_excel(fpath, index=False)
    print(f"[IIIT Agartala] Populated {len(out_df)} faculty emails.")

def process_remaining_iiits():
    # 1. IIIT Bhagalpur
    f_bgp = os.path.join(IIIT_DIR, "IIIT_Bhagalpur_Faculty.xlsx")
    if os.path.exists(f_bgp):
        df = pd.read_excel(f_bgp)
        for idx, row in df.iterrows():
            nm = str(row['Name']).strip()
            em = str(row['Email']).strip()
            if 'hod.mea@.iiitbh.ac.in' in em:
                df.at[idx, 'Email'] = 'hod.mea@iiitbh.ac.in'
            if 'Madhusudan Singh' in nm:
                df.at[idx, 'Department'] = 'Department of Electrical Engineering'
            elif any(c in nm for c in ['Suneel Kumar', 'Subhayu Ghosh', 'Parkala Vishnu', 'Anita Chandra']):
                df.at[idx, 'Department'] = 'Department of Computer Science & Engineering'
            elif any(c in nm for c in ['Bhanu Priya', 'Prabhat Kumar Vidyarthi']):
                df.at[idx, 'Department'] = 'Department of Electronics and Communication Engineering'
                if 'Bhanu Priya' in nm:
                    df.at[idx, 'Email'] = 'bpriya.ece@iiitbh.ac.in'
                elif 'Prabhat Kumar Vidyarthi' in nm:
                    df.at[idx, 'Email'] = 'pkvidyarthi.ece@iiitbh.ac.in'
        
        df = df[df['Department'].apply(is_target_department)].copy()
        df = clean_df(df[df['Email'].notna() & df['Email'].astype(str).str.contains('@')])
        df.to_excel(f_bgp, index=False)
        print(f"[IIIT Bhagalpur] Retained {len(df)} circuit faculty.")

    # 2. IIIT Bhopal
    f_bhp = os.path.join(IIIT_DIR, "IIIT_Bhopal_Faculty.xlsx")
    if os.path.exists(f_bhp):
        df = pd.read_excel(f_bhp)
        df = df[df['Department'].apply(is_target_department)].copy()
        for idx, row in df.iterrows():
            if 'Gurdeep' in str(row['Name']):
                df.at[idx, 'Email'] = 'gshura@umes.edu'
            elif 'Volker' in str(row['Name']):
                df.at[idx, 'Email'] = 'v.lindenstruth@fias.uni-frankfurt.de'
        df = clean_df(df[df['Email'].notna() & df['Email'].astype(str).str.contains('@')])
        df.to_excel(f_bhp, index=False)
        print(f"[IIIT Bhopal] Retained {len(df)} circuit faculty.")

    # 3. IIIT Bhubaneswar
    f_bbs = os.path.join(IIIT_DIR, "IIIT_Bhubaneswar_Faculty.xlsx")
    if os.path.exists(f_bbs):
        df = pd.read_excel(f_bbs)
        df = df[df['Department'].apply(is_target_department)].copy()
        for idx, row in df.iterrows():
            if 'Paramita Koley' in str(row['Name']):
                df.at[idx, 'Email'] = 'paramita.koley@iiit-bh.ac.in'
        df = clean_df(df[df['Email'].notna() & df['Email'].astype(str).str.contains('@')])
        df.to_excel(f_bbs, index=False)
        print(f"[IIIT Bhubaneswar] Retained {len(df)} circuit faculty.")

    # 4. IIIT Delhi
    f_del = os.path.join(IIIT_DIR, "IIIT_Delhi_Complete_Faculty.xlsx")
    if os.path.exists(f_del):
        df = pd.read_excel(f_del)
        df = df[df['Department'].apply(is_target_department)].copy()
        for idx, row in df.iterrows():
            if 'Ranjitha Prasad' in str(row['Name']):
                df.at[idx, 'Email'] = 'ranjitha@iiitd.ac.in'
        df = clean_df(df[df['Email'].notna() & df['Email'].astype(str).str.contains('@')])
        df.to_excel(f_del, index=False)
        print(f"[IIIT Delhi] Retained {len(df)} circuit faculty.")

    # 5. IIIT Guwahati
    f_guw = os.path.join(IIIT_DIR, "IIIT_Guwahati_Faculty.xlsx")
    if os.path.exists(f_guw):
        df = pd.read_excel(f_guw)
        df = df[df['Department'].apply(is_target_department)].copy()
        for idx, row in df.iterrows():
            if 'Snehasis Banerjee' in str(row['Name']):
                df.at[idx, 'Email'] = 'joysnehasis@gmail.com'
        df = clean_df(df[df['Email'].notna() & df['Email'].astype(str).str.contains('@')])
        df.to_excel(f_guw, index=False)
        print(f"[IIIT Guwahati] Retained {len(df)} circuit faculty.")

    # 6. IIIT Hyderabad
    f_hyd = os.path.join(IIIT_DIR, "IIIT_Hyderabad_Faculty.xlsx")
    if os.path.exists(f_hyd):
        df = pd.read_excel(f_hyd)
        df = df[df['Department'].apply(is_target_department)].copy()
        # Keep only verified emails
        df = clean_df(df[df['Email'].notna() & df['Email'].astype(str).str.contains('@')])
        df.to_excel(f_hyd, index=False)
        print(f"[IIIT Hyderabad] Retained {len(df)} circuit faculty with verified emails.")

    # 7. IIITDM Kancheepuram
    f_kan = os.path.join(IIIT_DIR, "IIITDM_Kancheepuram_Faculty.xlsx")
    if os.path.exists(f_kan):
        df = pd.read_excel(f_kan)
        # Check research interests / degrees to keep CSE / ECE
        cache_file = os.path.join(BASE_DIR, "cache", "fd31fd37007248b5f9d8aaa9c0ee1152.html")
        with open(cache_file, 'r', encoding='utf-8') as cf:
            soup = BeautifulSoup(cf.read(), 'html.parser')
            
        kan_dept_map = {}
        for card in soup.find_all('a', href=lambda h: h and '/people/faculty/' in h):
            href = card.get('href')
            text = card.get_text(separator=' | ', strip=True).lower()
            d = "Computer Science and Engineering"
            if any(k in text for k in ['mechanical', 'thermal', 'fluid', 'manufacturing', 'cad', 'materials design', 'aerospace']):
                d = "Mechanical Engineering"
            elif any(k in text for k in ['physics', 'chemistry', 'mathematics', 'number theory', 'humanities']):
                d = "Sciences and Humanities"
            elif any(k in text for k in ['electronics', 'signal', 'vlsi', 'power electronics', 'microelectronics', 'electric vehicles', 'rfic', 'antenna']):
                d = "Electronics and Communication Engineering"
            em = href.split('/')[-1].strip().lower()
            kan_dept_map[em] = d
            
        rows = []
        for _, row in df.iterrows():
            em = str(row['Email']).strip().lower()
            dept = kan_dept_map.get(em, "Computer Science and Engineering")
            if is_target_department(dept):
                r = row.to_dict()
                r['Department'] = dept
                rows.append(r)
                
        out_df = clean_df(pd.DataFrame(rows)).drop_duplicates(subset=['Email'])
        out_df.to_excel(f_kan, index=False)
        print(f"[IIITDM Kancheepuram] Filtered and retained {len(out_df)} circuit faculty.")

    # 8. All other IIITs
    iiit_files = sorted(glob.glob(os.path.join(IIIT_DIR, "*.xlsx")))
    processed_iiits = [
        "IIIT_Allahabad_Faculty.xlsx", "IIIT_Naya_Raipur_Faculty.xlsx", "IIIT_SriCity_Faculty.xlsx",
        "IIITDM_Kurnool_Faculty.xlsx", "IIIT_Dharwad_Faculty.xlsx", "IIIT_Kottayam_Faculty.xlsx",
        "IIIT_Lucknow_Faculty.xlsx", "IIIT_Vadodara_Faculty.xlsx", "IIIT_Una_Faculty.xlsx",
        "IIIT_Sonepat_Faculty.xlsx", "IIITM_Gwalior_Faculty.xlsx", "IIIT_Manipur_Faculty.xlsx",
        "IIIT_Raichur_Faculty.xlsx", "IIIT_Agartala_Faculty.xlsx", "IIIT_Bhagalpur_Faculty.xlsx",
        "IIIT_Bhopal_Faculty.xlsx", "IIIT_Bhubaneswar_Faculty.xlsx", "IIIT_Delhi_Complete_Faculty.xlsx",
        "IIIT_Guwahati_Faculty.xlsx", "IIIT_Hyderabad_Faculty.xlsx", "IIITDM_Kancheepuram_Faculty.xlsx"
    ]
    for f in iiit_files:
        fname = os.path.basename(f)
        if fname in processed_iiits:
            continue
        df = pd.read_excel(f)
        filtered = df[df['Department'].apply(is_target_department)].copy()
        filtered = filtered[filtered['Email'].notna() & filtered['Email'].astype(str).str.contains('@')]
        out_df = clean_df(filtered)
        out_df.to_excel(f, index=False)
        print(f"[{fname}] Filtered to {len(out_df)} circuit faculty.")

def main():
    print("=== Processing NITs ===")
    process_nit_delhi()
    process_nit_patna()
    process_nit_arunachal()
    process_standard_nits()
    
    print("\n=== Processing IIITs ===")
    process_iiit_allahabad()
    process_iiit_naya_raipur()
    process_iiit_sricity()
    process_iiitdm_kurnool()
    process_iiit_dharwad()
    process_iiit_kottayam()
    process_iiit_lucknow()
    process_iiit_vadodara()
    process_iiit_una()
    process_iiit_sonepat()
    process_iiitm_gwalior()
    process_iiit_manipur()
    process_iiit_raichur()
    process_iiit_agartala()
    process_remaining_iiits()

if __name__ == '__main__':
    main()
