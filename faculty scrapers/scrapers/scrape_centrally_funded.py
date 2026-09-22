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
    # Ensure columns exist
    for c in cols:
        if c not in df.columns:
            df[c] = 'N/A'
    df = df[cols].drop_duplicates(subset=['Name', 'Email'])
    df.to_excel(filepath, index=False)
    print(f"[SAVED] {filename} with {len(df)} faculty members.")
    return len(df)

# =========================================================================
# 1. IIIT Allahabad
# =========================================================================
def scrape_iiit_allahabad():
    print("Scraping IIIT Allahabad...")
    faculty = []
    base_url = "https://www.iiita.ac.in"
    for page in range(3):
        url = f"https://www.iiita.ac.in/faculty/?page={page}"
        soup = fetch_soup(url)
        for row in soup.find_all('div', class_='views-row'):
            name_el = row.find('p', class_='faculty-name')
            if not name_el:
                continue
            name = name_el.get_text(strip=True)
            link = name_el.find('a')
            profile_url = f"{base_url}{link.get('href')}" if link and link.get('href') else url
            
            des_el = row.find('p', class_='des')
            designation = des_el.get_text(strip=True) if des_el else "N/A"
            
            dep_el = row.find('p', class_='dep')
            department = dep_el.get_text(strip=True) if dep_el else "N/A"
            
            email_el = row.find('p', class_='email')
            email = email_el.get_text(strip=True) if email_el else "N/A"
            
            faculty.append({
                'Name': name,
                'Institution': 'IIIT Allahabad',
                'Department': department,
                'Designation': designation,
                'Qualification': 'Ph.D.',
                'Email': email,
                'Profile URL': profile_url
            })
    return save_excel(faculty, "IIIT_Allahabad_Faculty.xlsx")

# =========================================================================
# 2. IIITDM Kancheepuram
# =========================================================================
def scrape_iiitdm_kancheepuram():
    print("Scraping IIITDM Kancheepuram...")
    url = "https://iiitdm.ac.in/people/faculty"
    soup = fetch_soup(url)
    faculty = []
    cards = soup.find_all('a', href=lambda h: h and '/people/faculty/' in h)
    for card in cards:
        name_el = card.find('h1')
        if not name_el:
            continue
        name = name_el.get_text(strip=True)
        
        des_el = card.find('h2')
        designation = des_el.get_text(strip=True) if des_el else "Faculty"
        
        qualification = "N/A"
        for p in card.find_all('p'):
            t = p.get_text(strip=True)
            if 'Ph.D' in t:
                qualification = t.replace('Ph.D:', '').strip()
                break
                
        email = "N/A"
        href = card.get('href', '')
        if '@' in href:
            email = href.split('/')[-1].strip()
        else:
            m = re.search(r'[a-zA-Z0-9_.+-]+@iiitdm\.ac\.in', card.get_text())
            if m:
                email = m.group(0)
                
        profile_url = f"https://iiitdm.ac.in{href}" if href.startswith('/') else href
        
        faculty.append({
            'Name': name,
            'Institution': 'IIITDM Kancheepuram',
            'Department': 'Engineering & Science',
            'Designation': designation,
            'Qualification': qualification,
            'Email': email,
            'Profile URL': profile_url
        })
    return save_excel(faculty, "IIITDM_Kancheepuram_Faculty.xlsx")

# =========================================================================
# 3. IIITDM Kurnool
# =========================================================================
def scrape_iiitdm_kurnool():
    print("Scraping IIITDM Kurnool...")
    faculty = []
    for p in range(1, 4):
        url = f"https://iiitk.ac.in/Faculty/page?page={p}"
        soup = fetch_soup(url)
        for art in soup.find_all('article', class_=re.compile(r'entry-item', re.I)):
            h2 = art.find('h2', class_='entry-title')
            if not h2:
                continue
            name = h2.get_text(strip=True)
            a = h2.find('a')
            profile_url = a.get('href', url) if a else url
            
            p_tags = art.find_all('p')
            department = p_tags[0].get_text(strip=True) if len(p_tags) > 0 else "N/A"
            
            qualification = "N/A"
            for pt in p_tags:
                txt = pt.get_text(strip=True)
                if 'Education:' in txt or 'PhD' in txt:
                    qualification = txt.replace('Education:', '').strip()
                    break
                    
            faculty.append({
                'Name': name,
                'Institution': 'IIITDM Kurnool',
                'Department': department,
                'Designation': 'Faculty',
                'Qualification': qualification,
                'Email': 'N/A',
                'Profile URL': profile_url
            })
    return save_excel(faculty, "IIITDM_Kurnool_Faculty.xlsx")

# =========================================================================
# 4. ABV-IIITM Gwalior
# =========================================================================
def scrape_iiitm_gwalior():
    print("Scraping ABV-IIITM Gwalior...")
    url = "https://iiitm.ac.in/staff"
    soup = fetch_soup(url)
    faculty = []
    boxes = soup.find_all('div', class_='associbox')
    for b in boxes:
        name_el = b.find('h3')
        if not name_el:
            continue
        name = name_el.get_text(strip=True)
        p_tags = b.find_all('p')
        designation = p_tags[0].get_text(strip=True) if len(p_tags) > 0 else "N/A"
        department = p_tags[1].get_text(strip=True) if len(p_tags) > 1 else "N/A"
        
        faculty.append({
            'Name': name,
            'Institution': 'ABV-IIITM Gwalior',
            'Department': department,
            'Designation': designation,
            'Qualification': 'Ph.D.',
            'Email': 'N/A',
            'Profile URL': url
        })
    return save_excel(faculty, "IIITM_Gwalior_Faculty.xlsx")

# =========================================================================
# 5. PDPM IIITDM Jabalpur
# =========================================================================
def scrape_iiitdm_jabalpur():
    print("Scraping PDPM IIITDM Jabalpur...")
    depts = [
        ("Computer Science & Engineering", "https://cse.iiitdmj.ac.in/faculty.php"),
        ("Electronics & Communication Engineering", "https://ece.iiitdmj.ac.in/faculty.html"),
        ("Mechanical Engineering", "https://www.iiitdmj.ac.in/me.iiitdmj.ac.in/faculty.html")
    ]
    faculty = []
    for dept_name, url in depts:
        soup = fetch_soup(url)
        for a in soup.find_all('a', href=lambda h: h and 'faculty/' in h):
            prof_url = a.get('href')
            parent = a.find_parent('div', class_=re.compile(r'box|card|col|member', re.I)) or a.find_parent('div')
            if not parent:
                continue
            title_el = parent.find(['h3', 'h4', 'h5', 'strong'])
            name = title_el.get_text(separator=" ", strip=True) if title_el else a.get_text(strip=True)
            # Remove view profile or redundant text
            name = re.sub(r'^(view\s*profile|profile|dr\.)\s*', '', name, flags=re.I).strip()
            name = f"Dr. {name}" if not name.startswith("Dr.") else name
            
            des_el = parent.find('small') or parent.find('p')
            desig = des_el.get_text(strip=True) if des_el else "Faculty"
            
            faculty.append({
                'Name': name,
                'Institution': 'PDPM IIITDM Jabalpur',
                'Department': dept_name,
                'Designation': desig,
                'Qualification': 'Ph.D.',
                'Email': f"{prof_url.split('/')[-1]}@iiitdmj.ac.in",
                'Profile URL': prof_url
            })
    return save_excel(faculty, "IIITDM_Jabalpur_Faculty.xlsx")

if __name__ == '__main__':
    scrape_iiit_allahabad()
    scrape_iiitdm_kancheepuram()
    scrape_iiitdm_kurnool()
    scrape_iiitm_gwalior()
    scrape_iiitdm_jabalpur()
