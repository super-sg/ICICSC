import os
import sys
import re
import xml.etree.ElementTree as ET
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fetcher import fetch_soup, fetch_url

OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def save_excel(faculty_list, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    df = pd.DataFrame(faculty_list)
    cols = ['Name', 'Institution', 'Department', 'Designation', 'Qualification', 'Email', 'Profile URL']
    for c in cols:
        if c not in df.columns:
            df[c] = 'N/A'
    df = df[cols].drop_duplicates(subset=['Name', 'Email'])
    df.to_excel(filepath, index=False)
    print(f"[SAVED] {filename} with {len(df)} faculty members.", flush=True)
    return len(df)

# =========================================================================
# 1. IIIT Bangalore
# =========================================================================
def scrape_iiit_bangalore():
    print("Scraping IIIT Bangalore...", flush=True)
    url = "https://www.iiitb.ac.in/faculty"
    soup = fetch_soup(url)
    faculty = []
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        name = a.get_text(strip=True)
        if not href.startswith('faculty/') or not name or len(name) < 3:
            continue
        
        card = a.find_parent('div', class_='cor-p2') or a.find_parent('div', class_='col-md-3') or a.find_parent('div')
        if not card:
            continue
            
        qual_el = card.find(class_='eduction')
        qualification = qual_el.get_text(strip=True) if qual_el else "Ph.D."
        
        email = "N/A"
        email_el = card.find('a', attrs={'data-email': True})
        if email_el:
            email = email_el.get('data-email', 'N/A')
        else:
            m = re.search(r'[a-zA-Z0-9_.+-]+@iiitb\.ac\.in', card.get_text())
            if m:
                email = m.group(0)
                
        profile_url = f"https://www.iiitb.ac.in/{href}"
        
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Bangalore',
            'Department': 'Computer Science & Electronics',
            'Designation': 'Faculty',
            'Qualification': qualification,
            'Email': email,
            'Profile URL': profile_url
        })
        
    return save_excel(faculty, "IIIT_Bangalore_Faculty.xlsx")

# =========================================================================
# 2. IIIT Bhubaneswar
# =========================================================================
def scrape_iiit_bhubaneswar():
    print("Scraping IIIT Bhubaneswar...", flush=True)
    url = "https://www.iiit-bh.ac.in/category/faculty/"
    soup = fetch_soup(url)
    faculty = []
    
    for art in soup.find_all('article', class_=lambda c: c and 'faculty' in c):
        h3 = art.find('h3')
        if not h3:
            continue
        name = h3.get_text(strip=True)
        a = h3.find('a')
        profile_url = a.get('href', url) if a else url
        
        des_el = art.find(class_='faculty_designation')
        designation = des_el.get_text(strip=True) if des_el else "Faculty"
        
        dept_el = art.find(class_='faculty_department')
        department = dept_el.get_text(strip=True) if dept_el else "N/A"
        
        email_el = art.find(class_='faculty-email')
        email = "N/A"
        if email_el:
            email = email_el.get_text(strip=True).replace('Email:', '').strip()
            
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Bhubaneswar',
            'Department': department,
            'Designation': designation,
            'Qualification': 'Ph.D.',
            'Email': email,
            'Profile URL': profile_url
        })
        
    return save_excel(faculty, "IIIT_Bhubaneswar_Faculty.xlsx")

# =========================================================================
# 3. IIIT Naya Raipur
# =========================================================================
def scrape_iiit_naya_raipur():
    print("Scraping IIIT Naya Raipur...", flush=True)
    url = "https://www.iiitnr.ac.in/faculty"
    soup = fetch_soup(url)
    faculty = []
    
    for block in soup.find_all('div', class_='board_employ'):
        h3 = block.find('h3')
        if not h3:
            continue
        a = h3.find('a')
        name = a.get_text(strip=True) if a else h3.get_text(strip=True)
        profile_url = a.get('href', url) if a else url
        
        des_span = h3.find('span')
        desig = des_span.get_text(strip=True) if des_span else "Faculty"
        desig = desig.replace('(', '').replace(')', '').strip()
        
        department = "N/A"
        email = "N/A"
        for p in block.find_all('p'):
            t = p.get_text(strip=True)
            if 'Department :' in t:
                department = t.replace('Department :', '').strip()
            elif 'Email Id :' in t:
                email = t.replace('Email Id :', '').strip()
                
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Naya Raipur',
            'Department': department,
            'Designation': desig,
            'Qualification': 'Ph.D.',
            'Email': email,
            'Profile URL': profile_url
        })
        
    return save_excel(faculty, "IIIT_Naya_Raipur_Faculty.xlsx")

# =========================================================================
# 4. IIIT Hyderabad
# =========================================================================
def scrape_iiit_hyderabad():
    print("Scraping IIIT Hyderabad...", flush=True)
    sitemap_url = "https://www.iiit.ac.in/faculty-sitemap.xml"
    xml_data = fetch_url(sitemap_url)
    faculty = []
    
    # Extract faculty URLs from sitemap
    urls = re.findall(r'https:\/\/www\.iiit\.ac\.in\/faculty\/[a-zA-Z0-9_-]+\/', xml_data)
    urls = list(dict.fromkeys(urls))
    print(f"Found {len(urls)} faculty URLs in IIITH sitemap.", flush=True)
    
    for u in urls:
        # derive name from slug
        slug = u.rstrip('/').split('/')[-1]
        name_guess = slug.replace('-', ' ').title()
        
        soup = fetch_soup(u)
        h2 = soup.find('h2', class_='elementor-heading-title')
        name = h2.get_text(strip=True) if h2 else name_guess
        
        text = soup.get_text()
        desig = "Faculty"
        m_desig = re.search(r'(Professor|Associate Professor|Assistant Professor|Adjunct Faculty|Emeritus Professor)', text, re.I)
        if m_desig:
            desig = m_desig.group(0).title()
            
        qual = "Ph.D."
        m_qual = re.search(r'Ph\.?D\.?\s*\([^\)]+\)', text)
        if m_qual:
            qual = m_qual.group(0)
            
        email = "N/A"
        m_email = re.search(r'([a-zA-Z0-9_.+-]+\[at\][a-zA-Z0-9_.-]+)', text)
        if m_email:
            email = m_email.group(1).replace('[at]', '@')
        else:
            m_email2 = re.search(r'[a-zA-Z0-9_.+-]+@iiit\.ac\.in', text)
            if m_email2:
                email = m_email2.group(0)
                
        dept = "Computing & Emerging Technologies"
        for d_name in ['Computer Science', 'Electronics', 'Signal Processing', 'Cognitive Science', 'Human Science', 'Bioinformatics']:
            if d_name.lower() in text.lower():
                dept = d_name
                break
                
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Hyderabad',
            'Department': dept,
            'Designation': desig,
            'Qualification': qual,
            'Email': email,
            'Profile URL': u
        })
        
    return save_excel(faculty, "IIIT_Hyderabad_Faculty.xlsx")

if __name__ == '__main__':
    scrape_iiit_bangalore()
    scrape_iiit_bhubaneswar()
    scrape_iiit_naya_raipur()
    scrape_iiit_hyderabad()
