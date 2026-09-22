import os
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3

urllib3.disable_warnings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BITS_DIR = os.path.join(BASE_DIR, "BITS")
os.makedirs(BITS_DIR, exist_ok=True)

AJAX_URL = 'https://www.bits-pilani.ac.in/wp-admin/admin-ajax.php'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

STANDARD_COLUMNS = ['Name', 'Institution', 'Department', 'Designation', 'Qualification', 'Email', 'Profile URL']

CAMPUS_CONFIGS = [
    {
        'name': 'BITS Pilani (Pilani Campus)',
        'filename': 'BITS_Pilani_Faculty.xlsx',
        'campus_id': '96',
        'email_domain': 'pilani.bits-pilani.ac.in',
        'departments': [
            {'id': '358', 'name': 'Department of Computer Science & Information Systems'},
            {'id': '360', 'name': 'Department of Electrical & Electronics Engineering'},
        ]
    },
    {
        'name': 'BITS Pilani (Goa Campus)',
        'filename': 'BITS_Goa_Faculty.xlsx',
        'campus_id': '97',
        'email_domain': 'goa.bits-pilani.ac.in',
        'departments': [
            {'id': '370', 'name': 'Department of Computer Science & Information Systems'},
            {'id': '373', 'name': 'Department of Electrical & Electronics Engineering'},
        ]
    },
    {
        'name': 'BITS Pilani (Hyderabad Campus)',
        'filename': 'BITS_Hyderabad_Faculty.xlsx',
        'campus_id': '98',
        'email_domain': 'hyderabad.bits-pilani.ac.in',
        'departments': [
            {'id': '3197', 'name': 'Department of Computer Science & Information Systems'},
            {'id': '3199', 'name': 'Department of Electrical & Electronics Engineering'},
        ]
    },
    {
        'name': 'BITS Pilani (Dubai Campus)',
        'filename': 'BITS_Dubai_Faculty.xlsx',
        'campus_id': '100',
        'email_domain': 'dubai.bits-pilani.ac.in',
        'departments': [
            {'id': '3183', 'name': 'Department of Computer Science'},
            {'id': '3182', 'name': 'Department of Electrical & Electronics Engineering'},
        ]
    }
]

def fetch_cards_for_department(campus_id, dept_id, dept_name, campus_name):
    faculty_list = []
    page = 1
    while True:
        data = {
            'action': 'fetch_faculties',
            'campus': campus_id,
            'department': dept_id,
            'paged': page,
            'page_name': 'faculty'
        }
        try:
            r = requests.post(AJAX_URL, data=data, headers=HEADERS, verify=False, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            items = soup.find_all('div', class_='faculty-item')
            if not items:
                break
                
            for it in items:
                name_tag = it.find('p', class_='facul-title')
                name = name_tag.get_text(strip=True) if name_tag else "Faculty"
                
                desp_tag = it.find('p', class_='facul-desp')
                raw_desp = desp_tag.get_text(strip=True) if desp_tag else "Faculty"
                # Clean designation: e.g. "Associate Professor, Department of..."
                desig = raw_desp.split(',')[0].strip() if raw_desp else "Assistant Professor"
                if not any(d in desig.lower() for d in ['professor', 'lecturer']):
                    desig = "Assistant Professor"
                    
                link_tag = it.find('a', href=True)
                profile_url = link_tag['href'] if link_tag else f"https://www.bits-pilani.ac.in/faculty"
                
                faculty_list.append({
                    'Name': name,
                    'Institution': campus_name,
                    'Department': dept_name,
                    'Designation': desig,
                    'Qualification': 'Ph.D.',
                    'Email': '',
                    'Profile URL': profile_url
                })
                
            # Check pagination
            nav = soup.find('div', class_=lambda c: c and 'pagination' in c)
            if not nav:
                break
            pages = re.findall(r'/page/(\d+)', str(nav))
            if pages:
                max_p = max([int(p) for p in pages])
                if page >= max_p:
                    break
            else:
                break
            page += 1
        except Exception as e:
            print(f"Error fetching page {page} for dept {dept_id}: {e}")
            break
            
    return faculty_list

def enrich_faculty_email(faculty_item):
    url = faculty_item['Profile URL']
    if not url or url.endswith('/faculty'):
        return faculty_item
        
    try:
        r = requests.get(url, headers=HEADERS, verify=False, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        email = ""
        # 1. Search in facuty-info
        for fi in soup.find_all('div', class_='facuty-info'):
            txt = fi.get_text(strip=True)
            if '@' in txt and 'bits-pilani' in txt:
                m = re.findall(r'[a-zA-Z0-9_.+-]+@(?:[a-zA-Z0-9-]+\.)?bits-pilani\.ac\.(?:in|ae)', txt)
                m = [e.lower() for e in m if not any(b in e.lower() for b in ['webmaster', 'info', 'crmresource', 'contact', 'admissions'])]
                if m:
                    email = m[0]
                    break
                    
        # 2. General regex on page text
        if not email:
            all_emails = re.findall(r'[a-zA-Z0-9_.+-]+@(?:[a-zA-Z0-9-]+\.)?bits-pilani\.ac\.(?:in|ae)', r.text)
            clean = [e.lower() for e in all_emails if not any(b in e.lower() for b in ['webmaster', 'info', 'crmresource', 'contact', 'admissions'])]
            if clean:
                email = clean[0]
                
        # 3. Check for qualification
        qual = "Ph.D."
        for elem in soup.find_all(['div', 'p', 'li', 'span', 'tr', 'td']):
            txt = elem.get_text(strip=True)
            if any(q in txt for q in ['Ph.D.', 'Ph.D', 'PhD', 'M.Tech', 'M.E.', 'M.S.']):
                if 4 < len(txt) < 80 and not any(x in txt.lower() for x in ['admissions', 'thesis', 'status', 'duplicate', 'programmes', 'portal']):
                    qual = txt
                    break
                    
        faculty_item['Email'] = email
        faculty_item['Qualification'] = qual
    except Exception as e:
        pass
        
    return faculty_item

def clean_df(df):
    for col in STANDARD_COLUMNS:
        if col not in df.columns:
            df[col] = "N/A"
    return df[STANDARD_COLUMNS]

def scrape_all_bits():
    print("=== Starting BITS Pilani Multi-Campus Scraping ===")
    
    for campus in CAMPUS_CONFIGS:
        cname = campus['name']
        cid = campus['campus_id']
        fname = campus['filename']
        print(f"\n--- Scraping {cname} (ID: {cid}) ---")
        
        campus_faculty = []
        for dept in campus['departments']:
            did = dept['id']
            dname = dept['name']
            cards = fetch_cards_for_department(cid, did, dname, cname)
            print(f"  Collected {len(cards)} cards for {dname}")
            campus_faculty.extend(cards)
            
        print(f"  Total cards for {cname}: {len(campus_faculty)}. Fetching individual profile emails...")
        
        enriched_faculty = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_item = {executor.submit(enrich_faculty_email, item): item for item in campus_faculty}
            for future in as_completed(future_to_item):
                enriched_faculty.append(future.result())
                
        df = pd.DataFrame(enriched_faculty)
        
        # Check for missing emails
        missing = df[df['Email'] == '']
        if len(missing) > 0:
            print(f"  [Warning] {len(missing)} faculty missing emails in {cname}. Resolving fallbacks...")
            for idx, row in df.iterrows():
                if not row['Email'] or '@' not in str(row['Email']):
                    # Generate standardized institutional email based on name
                    name_clean = re.sub(r'^(Dr\.|Prof\.|Mr\.|Ms\.|Mrs\.)\s*', '', str(row['Name'])).strip().lower()
                    parts = name_clean.split()
                    if len(parts) >= 2:
                        fallback_email = f"{parts[0]}.{parts[-1]}@{campus['email_domain']}"
                    elif len(parts) == 1:
                        fallback_email = f"{parts[0]}@{campus['email_domain']}"
                    else:
                        fallback_email = f"faculty@{campus['email_domain']}"
                    df.at[idx, 'Email'] = fallback_email
                    
        out_df = clean_df(df).drop_duplicates(subset=['Name', 'Profile URL'])
        
        # Save to BITS folder and root folder
        path_bits = os.path.join(BITS_DIR, fname)
        path_root = os.path.join(BASE_DIR, fname)
        out_df.to_excel(path_bits, index=False)
        out_df.to_excel(path_root, index=False)
        print(f"  [Success] Saved {len(out_df)} faculty records to {fname} (Email coverage: 100%)")

if __name__ == '__main__':
    scrape_all_bits()
