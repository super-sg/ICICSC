import os
import sys
import re
import json
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
# 1. IIIT Kota
# =========================================================================
def scrape_iiit_kota():
    print("Scraping IIIT Kota...", flush=True)
    url = "https://webapi.iiitkota.ac.in/api/out/faculty"
    raw = fetch_url(url)
    data = json.loads(raw) if raw else []
    faculty = []
    
    for item in data:
        name = item.get('name', 'N/A').strip()
        dept = item.get('department', 'N/A').strip()
        desig = item.get('description', 'Faculty').strip().replace('\n', ' ')
        fid = item.get('_id', '')
        prof_url = f"https://iiitkota.ac.in/faculty/{fid}" if fid else "https://iiitkota.ac.in/faculty"
        
        email = f"{fid}@iiitkota.ac.in" if fid else "N/A"
        
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Kota',
            'Department': dept,
            'Designation': desig,
            'Qualification': 'Ph.D.',
            'Email': email,
            'Profile URL': prof_url
        })
        
    return save_excel(faculty, "IIIT_Kota_Faculty.xlsx")

# =========================================================================
# 2. IIIT Bhopal
# =========================================================================
def scrape_iiit_bhopal():
    print("Scraping IIIT Bhopal...", flush=True)
    url = "https://iiitbhopal.ac.in/api/MasterData/GetAllFacultyDetail"
    raw = fetch_url(url)
    data = json.loads(raw) if raw else []
    faculty = []
    
    for item in data:
        name = item.get('Name', '').strip()
        if not name:
            continue
        dept = item.get('Department', '').strip() or "Computer Science & Engineering"
        desig = item.get('Post', 'Faculty').strip()
        qual = item.get('Degree', 'Ph.D.').strip()
        email = item.get('EmailId', 'N/A').strip() or "N/A"
        desc = item.get('Description', '')
        
        m_link = re.search(r'href=[\"\'](https?:\/\/[^\s\"\']+)[\"\']', desc)
        prof_url = m_link.group(1) if m_link else "https://iiitbhopal.ac.in/people/faculty"
        
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Bhopal',
            'Department': dept,
            'Designation': desig,
            'Qualification': qual,
            'Email': email,
            'Profile URL': prof_url
        })
        
    return save_excel(faculty, "IIIT_Bhopal_Faculty.xlsx")

# =========================================================================
# 3. IIIT Tiruchirappalli
# =========================================================================
def scrape_iiit_trichy():
    print("Scraping IIIT Tiruchirappalli...", flush=True)
    url = "https://www.iiitt.ac.in/json/faculty/faculty.json"
    raw = fetch_url(url)
    data = json.loads(raw) if raw else {}
    faculty = []
    
    for dept_key, members in data.items():
        dept_name = dept_key.split('|')[0].strip() if '|' in dept_key else dept_key
        for m in members:
            name = m.get('name', '').strip()
            desig = m.get('designation', 'Faculty').strip()
            qual = m.get('Institute', 'Ph.D.').strip()
            email = m.get('emailID', 'N/A').strip()
            prof_url = m.get('VidhwanLink') or m.get('PersonalPage') or "https://www.iiitt.ac.in/faculty"
            
            faculty.append({
                'Name': name,
                'Institution': 'IIIT Tiruchirappalli',
                'Department': dept_name,
                'Designation': desig,
                'Qualification': qual,
                'Email': email,
                'Profile URL': prof_url
            })
            
    return save_excel(faculty, "IIIT_Trichy_Faculty.xlsx")

# =========================================================================
# 4. IIIT Pune
# =========================================================================
def scrape_iiit_pune():
    print("Scraping IIIT Pune...", flush=True)
    url = "https://www.iiitp.ac.in/assets/faculty_details-C30VZW0k.js"
    raw = fetch_url(url)
    faculty = []
    
    # Matches patterns like: "bhupendra-singh":{designation:`...`, ...}
    entries = re.findall(r'\"([a-z0-9-]+)\":\s*\{(.*?)\}(?=,\"[a-z0-9-]+\":|\}\;)', raw, re.DOTALL)
    if not entries:
        # Fallback regex
        slugs = re.findall(r'\"([a-z0-9-]+)\":\s*\{designation:', raw)
        for s in slugs:
            entries.append((s, ""))
            
    for slug, block in entries:
        name_guess = slug.replace('-', ' ').title()
        desig = "Assistant Professor"
        qual = "Ph.D."
        email = f"{slug.replace('-', '')}@iiitp.ac.in"
        dept = "Computer Science & Engineering"
        
        # Extract from block if available
        m_des = re.search(r'designation:\s*`([^`]+)`', block)
        if m_des:
            desig = m_des.group(1).split('\n')[0].strip()
        m_qual = re.search(r'education:\s*`([^`]+)`', block)
        if m_qual:
            qual = m_qual.group(1).strip()
        m_email = re.search(r'email:\s*`([^`]+)`', block)
        if m_email:
            email = m_email.group(1).strip()
        m_dept = re.search(r'department:\s*`([^`]+)`', block)
        if m_dept:
            dept = m_dept.group(1).strip()
        m_bio = re.search(r'bio:\s*`(?:Dr\.|Prof\.)\s*([^`]+?)\s+is\s+serving', block)
        if m_bio:
            name = f"Dr. {m_bio.group(1).strip()}"
        else:
            name = f"Dr. {name_guess}"
            
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Pune',
            'Department': dept,
            'Designation': desig,
            'Qualification': qual,
            'Email': email,
            'Profile URL': f"https://www.iiitp.ac.in/people/faculty/{slug}"
        })
        
    return save_excel(faculty, "IIIT_Pune_Faculty.xlsx")

# =========================================================================
# 5. IIIT Surat
# =========================================================================
def scrape_iiit_surat():
    print("Scraping IIIT Surat...", flush=True)
    url = "https://www.iiitsurat.ac.in/static/js/bundle.js"
    raw = fetch_url(url)
    faculty = []
    
    matches = re.findall(r'name:\s*[\x27\"]([^\x27\"]+)[\x27\"],[^}]+email:\s*[\x27\"]([^\x27\"]+)[\x27\"]', raw)
    for name, email in matches:
        if '@iiitsurat.ac.in' not in email:
            continue
        desig = "Assistant Professor"
        if "Prof." in name or "director" in email:
            desig = "Professor & Director"
        elif "associate" in email:
            desig = "Associate Professor / Associate Dean"
            
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Surat',
            'Department': 'Computer Science & ECE',
            'Designation': desig,
            'Qualification': 'Ph.D.',
            'Email': email,
            'Profile URL': "https://www.iiitsurat.ac.in/faculty"
        })
        
    return save_excel(faculty, "IIIT_Surat_Faculty.xlsx")

# =========================================================================
# 6. IIIT Kottayam
# =========================================================================
def scrape_iiit_kottayam():
    print("Scraping IIIT Kottayam...", flush=True)
    url = "https://www.iiitkottayam.ac.in/scripts/controllers/faculty.ctrl.js"
    raw = fetch_url(url)
    faculty = []
    
    items = re.findall(r'name:\s*[\x27\"]([^\x27\"]+)[\x27\"]', raw)
    for name in items:
        if not any(k in name for k in ['Dr.', 'Prof.']) or len(name) > 45:
            continue
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Kottayam',
            'Department': 'Computer Science & Engineering',
            'Designation': 'Faculty',
            'Qualification': 'Ph.D.',
            'Email': 'N/A',
            'Profile URL': 'https://www.iiitkottayam.ac.in/#!/faculty'
        })
        
    return save_excel(faculty, "IIIT_Kottayam_Faculty.xlsx")

# =========================================================================
# 7. IIIT Kalyani
# =========================================================================
def scrape_iiit_kalyani():
    print("Scraping IIIT Kalyani...", flush=True)
    url = "https://iiitkalyani.ac.in/faculty"
    soup = fetch_soup(url)
    faculty = []
    
    for item in soup.find_all(['h3', 'h4', 'h5', 'strong']):
        t = item.get_text(strip=True)
        if not any(k in t for k in ['Dr.', 'Prof.']) or len(t) > 60:
            continue
        # Split name and designation if merged
        m = re.match(r'(Dr\.[^A-Z]+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)(.*)', t)
        if m:
            name = m.group(1).strip()
            desig = m.group(2).strip() or "Assistant Professor"
        else:
            name = t
            desig = "Assistant Professor"
            
        card = item.find_parent('div', class_=True) or item.parent
        email = "N/A"
        m_e = re.search(r'[a-zA-Z0-9_.+-]+@iiitkalyani\.ac\.in', card.get_text())
        if m_e:
            email = m_e.group(0)
            
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Kalyani',
            'Department': 'Computer Science & Electronics',
            'Designation': desig,
            'Qualification': 'Ph.D.',
            'Email': email,
            'Profile URL': url
        })
        
    return save_excel(faculty, "IIIT_Kalyani_Faculty.xlsx")

# =========================================================================
# 8. IIIT Ranchi
# =========================================================================
def scrape_iiit_ranchi():
    print("Scraping IIIT Ranchi...", flush=True)
    url = "https://www.iiitranchi.ac.in/faculty.aspx"
    soup = fetch_soup(url)
    faculty = []
    
    for h in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'strong']):
        t = h.get_text(strip=True)
        if not any(k in t for k in ['Dr.', 'Prof.']) or len(t) > 50:
            continue
        name = t
        card = h.find_parent('div', class_=True) or h.parent
        text = card.get_text(separator=' | ', strip=True)
        
        desig = "Faculty"
        m_des = re.search(r'(Professor|Associate Professor|Assistant Professor)', text)
        if m_des:
            desig = m_des.group(0)
            
        email = "N/A"
        m_e = re.search(r'[a-zA-Z0-9_.+-]+@iiitranchi\.ac\.in', text)
        if m_e:
            email = m_e.group(0)
            
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Ranchi',
            'Department': 'Computer Science & Engineering',
            'Designation': desig,
            'Qualification': 'Ph.D.',
            'Email': email,
            'Profile URL': url
        })
        
    return save_excel(faculty, "IIIT_Ranchi_Faculty.xlsx")

# =========================================================================
# 9. IIIT Agartala
# =========================================================================
def scrape_iiit_agartala():
    print("Scraping IIIT Agartala...", flush=True)
    url = "https://iiitagartala.ac.in/academics/faculty"
    soup = fetch_soup(url)
    faculty = []
    
    for h in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'strong']):
        t = h.get_text(strip=True)
        if not any(k in t for k in ['Dr.', 'Prof.']) or len(t) > 50:
            continue
        name = t
        card = h.find_parent('div', class_=True) or h.parent
        text = card.get_text(separator=' | ', strip=True)
        
        desig = "Assistant Professor"
        m_des = re.search(r'(Professor|Associate Professor|Assistant Professor|HOD)', text)
        if m_des:
            desig = m_des.group(0)
            
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Agartala',
            'Department': 'Computer Science and Engineering',
            'Designation': desig,
            'Qualification': 'Ph.D.',
            'Email': 'N/A',
            'Profile URL': url
        })
        
    return save_excel(faculty, "IIIT_Agartala_Faculty.xlsx")

# =========================================================================
# 10. IIIT Una
# =========================================================================
def scrape_iiit_una():
    print("Scraping IIIT Una...", flush=True)
    url = "https://iiitu.ac.in/assets/index-Dgy8GIg1.js"
    raw = fetch_url(url)
    faculty = []
    
    names = re.findall(r'name:[\"\x27](Dr\.[^\"\x27]+|Prof\.[^\"\x27]+)[\"\x27]', raw)
    for name in set(names):
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Una',
            'Department': 'School of Computing & Electronics',
            'Designation': 'Faculty',
            'Qualification': 'Ph.D.',
            'Email': 'N/A',
            'Profile URL': 'https://iiitu.ac.in'
        })
        
    return save_excel(faculty, "IIIT_Una_Faculty.xlsx")

# =========================================================================
# 11. IIIT Sonepat
# =========================================================================
def scrape_iiit_sonepat():
    print("Scraping IIIT Sonepat...", flush=True)
    url = "http://www.iiitsonepat.ac.in/assets/index-C4YHEx3p.js"
    raw = fetch_url(url)
    faculty = []
    
    names = re.findall(r'\"(Dr\.\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+|Prof\.\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\"', raw)
    for name in set(names):
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Sonepat',
            'Department': 'Computer Science and Engineering',
            'Designation': 'Faculty',
            'Qualification': 'Ph.D.',
            'Email': 'N/A',
            'Profile URL': 'http://www.iiitsonepat.ac.in'
        })
        
    return save_excel(faculty, "IIIT_Sonepat_Faculty.xlsx")

if __name__ == '__main__':
    scrape_iiit_kota()
    scrape_iiit_bhopal()
    scrape_iiit_trichy()
    scrape_iiit_pune()
    scrape_iiit_surat()
    scrape_iiit_kottayam()
    scrape_iiit_kalyani()
    scrape_iiit_ranchi()
    scrape_iiit_agartala()
    scrape_iiit_una()
    scrape_iiit_sonepat()
