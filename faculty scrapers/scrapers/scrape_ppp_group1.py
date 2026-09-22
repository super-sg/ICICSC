import os
import sys
import re
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fetcher import fetch_soup

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
# 1. IIIT Sri City
# =========================================================================
def scrape_iiit_sricity():
    print("Scraping IIIT Sri City...", flush=True)
    url = "https://www.iiits.ac.in/people/regular-faculty/"
    soup = fetch_soup(url)
    faculty = []
    
    for h in soup.find_all(['h3', 'h4', 'h5', 'h6']):
        t = h.get_text(strip=True)
        if not any(k in t for k in ['Dr.', 'Prof.']):
            continue
        name = t
        card = h.find_parent('div', class_=re.compile(r'panel-grid-cell|cell|box|col|item', re.I)) or h.parent
        text_lines = [line.strip() for line in card.get_text().split('\n') if line.strip()]
        
        desig = "Faculty"
        qual = "Ph.D."
        dept = "Computer Science & ECE"
        
        for idx, line in enumerate(text_lines):
            if any(d in line.lower() for d in ['professor', 'associate professor', 'assistant professor', 'director']):
                desig = line
            if 'Ph.' in line or 'PhD' in line:
                qual = line
            if 'ECE' in line:
                dept = "Electronics & Communication Engineering"
            elif 'CSE' in line or 'Computer' in line:
                dept = "Computer Science and Engineering"
                
        email = "N/A"
        m = re.search(r'[a-zA-Z0-9_.+-]+@iiits\.ac\.in', card.get_text())
        if m:
            email = m.group(0)
            
        a = card.find('a', href=lambda href: href and ('people' in href or 'faculty' in href))
        profile_url = a.get('href', url) if a else url
        
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Sri City',
            'Department': dept,
            'Designation': desig,
            'Qualification': qual,
            'Email': email,
            'Profile URL': profile_url
        })
        
    return save_excel(faculty, "IIIT_SriCity_Faculty.xlsx")

# =========================================================================
# 2. IIIT Guwahati
# =========================================================================
def scrape_iiit_guwahati():
    print("Scraping IIIT Guwahati...", flush=True)
    depts = [
        ("Computer Science and Engineering", "https://www.iiitg.ac.in/computer-science-and-engineering"),
        ("Electronics and Communication Engineering", "https://www.iiitg.ac.in/electronics-and-communication-engineering"),
        ("Science and Mathematics", "https://www.iiitg.ac.in/science-and-mathemetics")
    ]
    faculty = []
    
    for dept_name, u in depts:
        soup = fetch_soup(u)
        current_desig = "Faculty"
        for tag in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'p']):
            txt = tag.get_text(strip=True)
            if txt in ['Professors', 'Associate Professors', 'Assistant Professors', 'Visiting Faculty']:
                current_desig = txt.rstrip('s')
                continue
            if any(k in txt for k in ['Prof.', 'Dr.']) and len(txt) < 50:
                name = txt
                card = tag.find_parent('div', class_=True) or tag.parent
                email = "N/A"
                m = re.search(r'[a-zA-Z0-9_.+-]+@iiitg\.ac\.in', card.get_text())
                if m:
                    email = m.group(0)
                a = card.find('a', href=True)
                profile_url = a.get('href', u) if a else u
                
                faculty.append({
                    'Name': name,
                    'Institution': 'IIIT Guwahati',
                    'Department': dept_name,
                    'Designation': current_desig,
                    'Qualification': 'Ph.D.',
                    'Email': email,
                    'Profile URL': profile_url
                })
                
    return save_excel(faculty, "IIIT_Guwahati_Faculty.xlsx")

# =========================================================================
# 3. IIIT Vadodara
# =========================================================================
def scrape_iiit_vadodara():
    print("Scraping IIIT Vadodara...", flush=True)
    depts = [
        ("Computer Science & Engineering", "http://iiitvadodara.ac.in/cse1.php"),
        ("Electronics & Communication Engineering", "http://iiitvadodara.ac.in/ece.php")
    ]
    faculty = []
    
    for dept_name, u in depts:
        soup = fetch_soup(u)
        for h in soup.find_all(['h3', 'h4', 'h5']):
            strong = h.find('strong')
            name = strong.get_text(strip=True) if strong else h.get_text(strip=True)
            if not name or len(name) < 3 or name in ['Computer Science & Engineering', 'Electronics & Communication Engineering', 'Areas of Interest']:
                continue
            card = h.find_parent('div', class_=re.compile(r'col', re.I)) or h.parent
            text = card.get_text(separator=' | ', strip=True)
            
            desig = "Faculty"
            m_desig = re.search(r'(Professor|Associate Professor|Assistant Professor)', text)
            if m_desig:
                desig = m_desig.group(0)
                
            qual = "Ph.D."
            m_qual = re.search(r'Ph\.?D\.?\s*\([^\)]+\)', text)
            if m_qual:
                qual = m_qual.group(0)
                
            email = "N/A"
            m_email = re.search(r'[a-zA-Z0-9_.+-]+@iiitvadodara\.ac\.in', text)
            if m_email:
                email = m_email.group(0)
                
            a = card.find('a', href=True)
            prof_url = a.get('href', u) if a else u
            
            faculty.append({
                'Name': name,
                'Institution': 'IIIT Vadodara',
                'Department': dept_name,
                'Designation': desig,
                'Qualification': qual,
                'Email': email,
                'Profile URL': prof_url
            })
            
    return save_excel(faculty, "IIIT_Vadodara_Faculty.xlsx")

# =========================================================================
# 4. IIIT Lucknow
# =========================================================================
def scrape_iiit_lucknow():
    print("Scraping IIIT Lucknow...", flush=True)
    url = "https://iiitl.ac.in/index.php/faculty/"
    soup = fetch_soup(url)
    faculty = []
    
    for item in soup.find_all('div', class_=re.compile(r'gdlr-core-personnel-list', re.I)):
        title_el = item.find(class_=re.compile(r'title', re.I))
        if not title_el:
            continue
        name = title_el.get_text(strip=True)
        a = title_el.find('a')
        prof_url = a.get('href', url) if a else url
        
        pos_el = item.find(class_=re.compile(r'position', re.I))
        desig = pos_el.get_text(strip=True) if pos_el else "Faculty"
        
        email = "N/A"
        m = re.search(r'[a-zA-Z0-9_.+-]+@iiitl\.ac\.in', item.get_text())
        if m:
            email = m.group(0)
            
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Lucknow',
            'Department': 'Information Technology & Computer Science',
            'Designation': desig,
            'Qualification': 'Ph.D.',
            'Email': email,
            'Profile URL': prof_url
        })
        
    return save_excel(faculty, "IIIT_Lucknow_Faculty.xlsx")

# =========================================================================
# 5. IIIT Dharwad
# =========================================================================
def scrape_iiit_dharwad():
    print("Scraping IIIT Dharwad...", flush=True)
    url = "https://iiitdwd.ac.in/academics/faculty/"
    soup = fetch_soup(url)
    faculty = []
    
    for h2 in soup.find_all('h2'):
        txt = h2.get_text(strip=True)
        if not any(k in txt for k in ['Dr.', 'Prof.']):
            continue
        name = txt
        card = h2.find_parent('div', class_=re.compile(r'flex', re.I)) or h2.parent
        p_tags = card.find_all('p')
        desig = p_tags[0].get_text(strip=True) if p_tags else "Faculty"
        
        email = "N/A"
        m = re.search(r'[a-zA-Z0-9_.+-]+@iiitdwd\.ac\.in', card.get_text())
        if m:
            email = m.group(0)
            
        a = card.find('a', href=True)
        prof_url = f"https://iiitdwd.ac.in{a['href']}" if a and a['href'].startswith('/') else (a['href'] if a else url)
        
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Dharwad',
            'Department': 'Computer Science & Data Science',
            'Designation': desig,
            'Qualification': 'Ph.D.',
            'Email': email,
            'Profile URL': prof_url
        })
        
    return save_excel(faculty, "IIIT_Dharwad_Faculty.xlsx")

# =========================================================================
# 6. IIIT Manipur
# =========================================================================
def scrape_iiit_manipur():
    print("Scraping IIIT Manipur...", flush=True)
    url = "http://iiitmanipur.ac.in/pages/people/staffTeaching.php"
    soup = fetch_soup(url)
    faculty = []
    
    for strong in soup.find_all('strong'):
        t = strong.get_text(strip=True)
        if not any(k in t for k in ['Dr.', 'Prof.']):
            continue
        name = t
        p = strong.find_parent('p') or strong.parent
        text = p.get_text(separator=' | ', strip=True)
        
        desig = "Faculty"
        m_des = re.search(r'(Assistant Professor|Associate Professor|Professor)', text, re.I)
        if m_des:
            desig = m_des.group(0)
            
        qual = "Ph.D."
        m_q = re.search(r'(PhD\s+from[^\;\|\<]+|Post-Doc[^\;\|\<]+)', text, re.I)
        if m_q:
            qual = m_q.group(0).strip()
            
        dept = "Computer Science & ECE"
        a_dept = p.find('a')
        if a_dept and len(a_dept.get_text(strip=True)) > 2:
            dept = a_dept.get_text(strip=True)
            
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Manipur',
            'Department': dept,
            'Designation': desig,
            'Qualification': qual,
            'Email': 'N/A',
            'Profile URL': url
        })
        
    return save_excel(faculty, "IIIT_Manipur_Faculty.xlsx")

# =========================================================================
# 7. IIIT Bhagalpur
# =========================================================================
def scrape_iiit_bhagalpur():
    print("Scraping IIIT Bhagalpur...", flush=True)
    url = "https://www.iiitbh.ac.in/faculty"
    soup = fetch_soup(url)
    faculty = []
    
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) < 2:
            continue
        text = tds[1].get_text(separator=' | ', strip=True)
        if not any(k in text for k in ['Dr.', 'Prof.']):
            continue
        parts = text.split(' | ')
        name = parts[0]
        desig = parts[1] if len(parts) > 1 else "Faculty"
        dept = parts[2] if len(parts) > 2 and 'Department' in parts[2] else "Engineering"
        
        email = "N/A"
        m = re.search(r'([a-zA-Z0-9_.]+(?:\[AT\]|@)[a-zA-Z0-9_.-]+)', text)
        if m:
            email = m.group(0).replace('[AT]', '@').replace('[at]', '@')
            
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Bhagalpur',
            'Department': dept,
            'Designation': desig,
            'Qualification': 'Ph.D.',
            'Email': email,
            'Profile URL': url
        })
        
    return save_excel(faculty, "IIIT_Bhagalpur_Faculty.xlsx")

# =========================================================================
# 8. IIIT Raichur
# =========================================================================
def scrape_iiit_raichur():
    print("Scraping IIIT Raichur...", flush=True)
    url = "https://iiitr.ac.in/faculty"
    soup = fetch_soup(url)
    faculty = []
    
    for card in soup.find_all('div', class_='faculty-card-col'):
        h5 = card.find('h5')
        if not h5:
            continue
        name = h5.get_text(strip=True)
        a = h5.find('a')
        href = a.get('href') if a else ""
        prof_url = f"https://iiitr.ac.in{href}" if href.startswith('/') else href
        
        dept_code = card.get('data-dept', 'CSE').upper()
        dept = f"Department of {dept_code}"
        
        h6s = card.find_all('h6')
        desig = h6s[0].get_text(strip=True) if len(h6s) > 0 else "Faculty"
        qual = h6s[1].get_text(strip=True) if len(h6s) > 1 else "Ph.D."
        
        faculty.append({
            'Name': name,
            'Institution': 'IIIT Raichur',
            'Department': dept,
            'Designation': desig,
            'Qualification': qual,
            'Email': 'N/A',
            'Profile URL': prof_url
        })
        
    return save_excel(faculty, "IIIT_Raichur_Faculty.xlsx")

if __name__ == '__main__':
    scrape_iiit_sricity()
    scrape_iiit_guwahati()
    scrape_iiit_vadodara()
    scrape_iiit_lucknow()
    scrape_iiit_dharwad()
    scrape_iiit_manipur()
    scrape_iiit_bhagalpur()
    scrape_iiit_raichur()
