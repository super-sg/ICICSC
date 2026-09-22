import os
import re
import ssl
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def fetch(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as res:
            return res.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Fetch error {url}: {e}")
        return ""

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', str(text))
    return text.strip()

# -------------------------------------------------------------
# 6. NIT Kurukshetra
# -------------------------------------------------------------
def scrape_nit_kurukshetra():
    print("--- Scraping NIT Kurukshetra ---")
    dept_urls = [
        ("https://nitkkr.ac.in/faculty-elec/", "Electrical Engineering"),
        ("https://nitkkr.ac.in/faculty-mec/", "Mechanical Engineering"),
        ("https://nitkkr.ac.in/faculty-2/", "Civil Engineering"),
        ("https://nitkkr.ac.in/faculty-4/", "Computer Engineering"),
        ("https://nitkkr.ac.in/faculty-6/", "Electronics and Communication Engineering"),
        ("https://nitkkr.ac.in/faculty-7/", "Physics"),
        ("https://nitkkr.ac.in/faculty-8/", "Chemistry"),
        ("https://nitkkr.ac.in/faculty-9/", "Humanities and Social Sciences"),
        ("https://nitkkr.ac.in/faculty-10/", "Mathematics"),
        ("https://nitkkr.ac.in/faculty-11/", "Business Administration"),
        ("https://nitkkr.ac.in/faculty-12/", "Computer Applications"),
        ("https://nitkkr.ac.in/faculty-14/", "School of VLSI Design and Embedded Systems")
    ]
    
    rows = []
    for url, dept_name in dept_urls:
        html = fetch(url, timeout=12)
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        
        # Each faculty member is inside a div with class 'ans_block' or containing fact-profile
        blocks = soup.find_all("div", class_="ans_block")
        if not blocks:
            blocks = soup.find_all("div", class_=lambda c: c and "fact-profile" in str(c))
            
        for b in blocks:
            b_text = b.get_text(separator="\n")
            if "@nitkkr.ac.in" not in b_text:
                continue
                
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@nitkkr\.ac\.in", b_text)
            if not emails:
                continue
            email = emails[0].lower()
            if email == "registrar@nitkkr.ac.in":
                continue
                
            h3 = b.find("h3") or b.find("h4") or b.find("h2")
            name = ""
            if h3:
                name = clean_text(h3.text)
                name = re.sub(r'\(.*?\)', '', name).strip()
                
            lines = [clean_text(x) for x in b_text.split("\n") if clean_text(x)]
            desig = "Faculty"
            qual = ""
            
            for line in lines:
                if not name and any(line.startswith(p) for p in ["Dr.", "Prof.", "Dr ", "Prof ", "Mr.", "Ms."]):
                    name = line
                if "Designation:" in line:
                    desig = clean_text(line.replace("Designation:", ""))
                if "Qualification:" in line:
                    qual = clean_text(line.replace("Qualification:", ""))
                    
            if not name and lines:
                name = lines[0]
                
            p_link = b.find("a", href=lambda h: h and "/author/" in h)
            profile_url = p_link.get("href") if p_link else url
            
            rows.append({
                "Name": name,
                "Institution": "National Institute of Technology Kurukshetra",
                "Department": dept_name,
                "Designation": desig,
                "Qualification": qual,
                "Email": email,
                "Profile URL": profile_url
            })
            
    df = pd.DataFrame(rows).drop_duplicates(subset=["Email", "Name"])
    out_path = os.path.join(OUTPUT_DIR, "NIT_Kurukshetra_Faculty.xlsx")
    df.to_excel(out_path, index=False)
    print(f"NIT Kurukshetra complete: {len(df)} faculty saved to {out_path}")
    return df

# -------------------------------------------------------------
# 7. NIT Srinagar
# -------------------------------------------------------------
def scrape_nit_srinagar():
    print("--- Scraping NIT Srinagar ---")
    depts = [
        ('ea', 'Chemical Engineering'),
        ('e', 'Mechanical Engineering'),
        ('c', 'Civil Engineering'),
        ('cs', 'Computer Science and Engineering'),
        ('g', 'Electrical Engineering'),
        ('ec', 'Electronics and Communication Engineering'),
        ('ee', 'Metallurgical Engineering'),
        ('i', 'Information Technology'),
        ('o', 'Mathematics'),
        ('q', 'Physics'),
        ('s', 'Chemistry'),
        ('eg', 'Humanities, Social Sciences and Management')
    ]
    
    rows = []
    for dept_id, dept_name in depts:
        url = f"https://nitsri.ac.in/Pages/FacultyList.aspx?nDeptID={dept_id}"
        html = fetch(url, timeout=12)
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        
        # Each faculty member is inside personnel container
        items = soup.find_all("div", class_=lambda c: c and "kingster-personnel-info-list kingster-type-email" in str(c))
        for item in items:
            email_text = clean_text(item.text)
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@nitsri\.ac\.in", email_text)
            if not emails:
                continue
            email = emails[0].lower()
            if email == "info@nitsri.ac.in":
                continue
                
            # Ascend to the personnel card
            card = item.find_parent("div", class_=lambda c: c and "gdlr-core-personnel-list" in str(c)) or item.find_parent("div", class_=lambda c: c and "personnel" in str(c))
            if not card:
                card = item.find_parent("div")
                
            name = ""
            h3 = card.find(["h3", "h2", "h4"])
            if h3:
                name = clean_text(h3.text)
                
            desig = "Faculty"
            pos_div = card.find("div", class_=lambda c: c and "position" in str(c))
            if pos_div:
                desig = clean_text(pos_div.text)
                
            content_div = card.find("div", class_=lambda c: c and "content" in str(c))
            qual = clean_text(content_div.text) if content_div else ""
            
            rows.append({
                "Name": name,
                "Institution": "National Institute of Technology Srinagar",
                "Department": dept_name,
                "Designation": desig,
                "Qualification": qual,
                "Email": email,
                "Profile URL": url
            })
            
    df = pd.DataFrame(rows).drop_duplicates(subset=["Email", "Name"])
    out_path = os.path.join(OUTPUT_DIR, "NIT_Srinagar_Faculty.xlsx")
    df.to_excel(out_path, index=False)
    print(f"NIT Srinagar complete: {len(df)} faculty saved to {out_path}")
    return df

# -------------------------------------------------------------
# 8. NIT Hamirpur
# -------------------------------------------------------------
def scrape_nit_hamirpur():
    print("--- Scraping NIT Hamirpur ---")
    dept_pages = [
        ("https://nith.ac.in/computer-science-engineering", "Computer Science & Engineering"),
        ("https://nith.ac.in/Departments/topic/130", "Civil Engineering"),
        ("https://nith.ac.in/chemical-engineering", "Chemical Engineering"),
        ("https://nith.ac.in/electronics-communication-engineering", "Electronics & Communication Engineering"),
        ("https://nith.ac.in/electrical-engineering", "Electrical Engineering"),
        ("https://nith.ac.in/mechanical-engineering", "Mechanical Engineering"),
        ("https://nith.ac.in/material-science-engineering", "Material Science & Engineering"),
        ("https://nith.ac.in/physics-photonics-science", "Physics & Photonics Science"),
        ("https://nith.ac.in/Departments/topic/287", "Architecture"),
        ("https://nith.ac.in/chemistry", "Chemistry"),
        ("https://nith.ac.in/mathematics-scientific-computing", "Mathematics & Scientific Computing"),
        ("https://nith.ac.in/humanities", "Humanities & Social Sciences"),
        ("https://nith.ac.in/management-studies", "Management Studies"),
        ("https://nith.ac.in/centre-for-energy-studies", "Centre For Energy Studies")
    ]
    
    rows = []
    for url, dept_name in dept_pages:
        html = fetch(url, timeout=12)
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        
        # Check all table rows or blocks with @nith.ac.in
        for container in soup.find_all(["tr", "div", "li"]):
            txt = container.get_text(separator="\n")
            if "@nith.ac.in" in txt and any(d in txt.lower() for d in ["professor", "faculty", "designation", "ph.d", "qualification"]):
                emails = re.findall(r"[a-zA-Z0-9_.+-]+@nith\.ac\.in", txt)
                if not emails:
                    continue
                email = emails[0].lower()
                if any(x in email for x in ["office.", "registrar", "head.", "webmaster"]):
                    continue
                    
                lines = [clean_text(x) for x in txt.split("\n") if clean_text(x)]
                name = ""
                desig = "Faculty"
                qual = ""
                
                for line in lines:
                    if not name and any(line.startswith(p) for p in ["Dr.", "Prof.", "Dr ", "Prof ", "Mr.", "Ms."]):
                        name = line
                    if any(d in line.lower() for d in ["professor", "assistant professor", "associate professor"]):
                        desig = line
                    if any(q in line.lower() for q in ["ph.d", "ph d", "m.tech", "b.tech", "m.sc"]):
                        qual = line
                        
                if not name and lines:
                    name = lines[0]
                    
                p_link = container.find("a", href=lambda h: h and "portfolio.nith.ac.in" in h)
                profile_url = p_link.get("href") if p_link else url
                
                rows.append({
                    "Name": name,
                    "Institution": "National Institute of Technology Hamirpur",
                    "Department": dept_name,
                    "Designation": desig,
                    "Qualification": qual,
                    "Email": email,
                    "Profile URL": profile_url
                })
                
    df = pd.DataFrame(rows).drop_duplicates(subset=["Email", "Name"])
    out_path = os.path.join(OUTPUT_DIR, "NIT_Hamirpur_Faculty.xlsx")
    df.to_excel(out_path, index=False)
    print(f"NIT Hamirpur complete: {len(df)} faculty saved to {out_path}")
    return df

# -------------------------------------------------------------
# 9. MANIT Bhopal
# -------------------------------------------------------------
def scrape_manit_bhopal():
    print("--- Scraping MANIT Bhopal ---")
    dept_urls = [
        ("https://www.manit.ac.in/computer-science-engineering-department-0", "Computer Science & Engineering"),
        ("https://www.manit.ac.in/civil-engineering-department", "Civil Engineering"),
        ("https://www.manit.ac.in/content/electrical-engineering", "Electrical Engineering"),
        ("https://www.manit.ac.in/content/electronics-communication-engineering", "Electronics & Communication Engineering"),
        ("https://www.manit.ac.in/content/mechanical-engineering", "Mechanical Engineering"),
        ("https://www.manit.ac.in/content/chemical-engineering-0", "Chemical Engineering"),
        ("https://www.manit.ac.in/content/materials-metallurgical-engineering", "Materials & Metallurgical Engineering"),
        ("https://www.manit.ac.in/content/biological-science-engineering", "Biological Science & Engineering"),
        ("https://www.manit.ac.in/content/chemistry-department", "Chemistry"),
        ("https://www.manit.ac.in/content/physics-department", "Physics"),
        ("https://www.manit.ac.in/content/computer-applications-department", "Computer Applications"),
        ("https://www.manit.ac.in/content/department-management-studies-dms", "Department of Management Studies")
    ]
    
    rows = []
    for url, dept_name in dept_urls:
        html = fetch(url, timeout=12)
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        
        # MANIT uses tables or div rows
        # Unobfuscate emails in HTML first
        # Pattern: username [at] (staff.)?manit [dot] ac [dot] in
        for container in soup.find_all(["tr", "div", "p", "li"]):
            c_html = str(container)
            c_text = container.get_text(separator="\n")
            
            emails = []
            obf = re.findall(r"([a-zA-Z0-9_.+-]+)\s*\[at\]\s*(?:staff\.)?manit\s*\[dot\]\s*ac\s*\[dot\]\s*in", c_html, re.I)
            for u in obf:
                emails.append(f"{u.lower()}@manit.ac.in")
            plain = re.findall(r"[a-zA-Z0-9_.+-]+@(?:staff\.)?manit\.ac\.in", c_text, re.I)
            for p in plain:
                emails.append(p.lower())
                
            if not emails:
                continue
            email = emails[0]
            if any(x in email for x in ["director", "pro@", "registrar", "office"]):
                continue
                
            lines = [clean_text(x) for x in c_text.split("\n") if clean_text(x)]
            name = ""
            desig = "Faculty"
            qual = ""
            
            for line in lines:
                if not name and any(line.startswith(p) for p in ["Dr.", "Prof.", "Dr ", "Prof ", "Mr.", "Ms.", "Shri "]):
                    name = line
                if "Designation" in line:
                    desig = clean_text(line.replace("Designation:", "").replace("Designation", ""))
                if "Qualification" in line:
                    qual = clean_text(line.replace("Qualification:", "").replace("Qualification", ""))
                    
            if not name and lines:
                name = lines[0]
                
            rows.append({
                "Name": name,
                "Institution": "Maulana Azad National Institute of Technology Bhopal",
                "Department": dept_name,
                "Designation": desig,
                "Qualification": qual,
                "Email": email,
                "Profile URL": url
            })
            
    df = pd.DataFrame(rows).drop_duplicates(subset=["Email", "Name"])
    out_path = os.path.join(OUTPUT_DIR, "MANIT_Bhopal_Faculty.xlsx")
    df.to_excel(out_path, index=False)
    print(f"MANIT Bhopal complete: {len(df)} faculty saved to {out_path}")
    return df

if __name__ == "__main__":
    scrape_nit_kurukshetra()
    scrape_nit_srinagar()
    scrape_nit_hamirpur()
    scrape_manit_bhopal()
