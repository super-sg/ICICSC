import os
import re
import ssl
import json
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
# 1. NIT Jalandhar (API-based, 100% structured)
# -------------------------------------------------------------
def scrape_nit_jalandhar():
    print("--- Scraping NIT Jalandhar ---")
    dept_map = {
        "it": "Information Technology",
        "cse": "Computer Science and Engineering",
        "bt": "Biotechnology",
        "ce": "Civil Engineering",
        "ch": "Chemical Engineering",
        "cy": "Chemistry",
        "ece": "Electronics and Communication Engineering",
        "ee": "Electrical Engineering",
        "hm": "Humanities and Management",
        "ipe": "Industrial and Production Engineering",
        "ice": "Instrumentation and Control Engineering",
        "ma": "Mathematics and Computing",
        "me": "Mechanical Engineering",
        "ph": "Physics",
        "tt": "Textile Technology"
    }
    
    rows = []
    for code, dept_name in dept_map.items():
        api_url = f"https://nitj.ac.in/api/dept/{code}/Faculty"
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as res:
                data = json.loads(res.read().decode('utf-8', errors='ignore'))
                for item in data:
                    f = item.get("ID", {})
                    name = clean_text(f.get("name", ""))
                    email = clean_text(f.get("email", "")).lower()
                    if not email and f.get("_id"):
                        continue
                    if email and not email.endswith("@nitj.ac.in") and "@" not in email:
                        email = f"{email}@nitj.ac.in"
                    
                    desig = clean_text(f.get("designation") or f.get("position") or "Faculty")
                    qual_list = f.get("education_qualification", [])
                    quals = []
                    if isinstance(qual_list, list):
                        for q in qual_list:
                            deg = q.get("degree")
                            field = q.get("field")
                            if deg and deg != "nan" and deg != "None":
                                quals.append(f"{deg} ({field})" if field else deg)
                    qual_str = "; ".join(quals) if quals else "Ph.D."
                    
                    profile_id = f.get("_id", "")
                    profile_url = f"https://departments.nitj.ac.in/dept/{code}/Faculty/{profile_id}" if profile_id else f"https://departments.nitj.ac.in/dept/{code}/Faculty"
                    
                    if name and email:
                        rows.append({
                            "Name": name,
                            "Institution": "National Institute of Technology Jalandhar",
                            "Department": dept_name,
                            "Designation": desig,
                            "Qualification": qual_str,
                            "Email": email,
                            "Profile URL": profile_url
                        })
        except Exception as e:
            print(f"NITJ {code} error: {e}")
            
    df = pd.DataFrame(rows).drop_duplicates(subset=["Email", "Name"])
    out_path = os.path.join(OUTPUT_DIR, "NIT_Jalandhar_Faculty.xlsx")
    df.to_excel(out_path, index=False)
    print(f"NIT Jalandhar complete: {len(df)} faculty saved to {out_path}")
    return df

# -------------------------------------------------------------
# 2. MNIT Jaipur
# -------------------------------------------------------------
def scrape_mnit_jaipur():
    print("--- Scraping MNIT Jaipur ---")
    depts = [
        ('/dept_aide/', 'Artificial Intelligence and Data Engineering'),
        ('/dept_arch/', 'Architecture and Planning'),
        ('/dept_chemical/', 'Chemical Engineering'),
        ('/dept_chemistry/', 'Chemistry'),
        ('/dept_civil/', 'Civil Engineering'),
        ('/dept_cse/', 'Computer Science and Engineering'),
        ('/dept_dms/', 'Management Studies'),
        ('/dept_ece/', 'Electronics and Communication Engineering'),
        ('/dept_ee/', 'Electrical Engineering'),
        ('/dept_hss/', 'Humanities and Social Sciences'),
        ('/dept_math/', 'Mathematics'),
        ('/dept_mech/', 'Mechanical Engineering'),
        ('/dept_mme/', 'Metallurgical and Materials Engineering'),
        ('/dept_physics/', 'Physics')
    ]
    
    rows = []
    for path, dept_name in depts:
        url = f"https://mnit.ac.in{path}people.php"
        html = fetch(url, timeout=12)
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        
        # Each faculty block contains a mailto: email ending with @mnit.ac.in
        for a in soup.find_all("a", href=re.compile(r"mailto:.*@mnit\.ac\.in", re.I)):
            raw_email = a.get("href").replace("mailto:", "").strip().lower()
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@mnit\.ac\.in", raw_email)
            if not emails:
                continue
            email = emails[0]
            
            # Find the card or container
            parent = a.find_parent("div", class_=lambda c: c and any(x in str(c).lower() for x in ["item", "card", "member", "faculty", "box"])) or a.find_parent("div")
            if not parent:
                continue
                
            text_lines = [clean_text(x) for x in parent.get_text(separator="\n").split("\n") if clean_text(x)]
            if not text_lines:
                continue
                
            # Usually line 0 is name, line 1 is designation, line 2 is qualification
            name = text_lines[0]
            if len(name) > 60 or "faculty" in name.lower() or "department" in name.lower():
                # try to find line containing Dr. or Prof. or Mr.
                for l in text_lines:
                    if any(l.startswith(prefix) for prefix in ["Dr", "Prof", "Mr", "Ms"]):
                        name = l
                        break
                        
            desig = "Faculty"
            qual = ""
            for idx, l in enumerate(text_lines):
                if any(d in l.lower() for d in ["professor", "lecturer"]):
                    desig = l
                    if idx + 1 < len(text_lines) and any(q in text_lines[idx+1].lower() for q in ["ph.d", "m.tech", "b.e", "b.tech", "m.sc"]):
                        qual = text_lines[idx+1]
                    break
                    
            profile_link = ""
            p_tag = parent.find("a", href=re.compile(r"profile\.php\?fid=", re.I))
            if p_tag and p_tag.get("href"):
                profile_link = f"https://mnit.ac.in{path}" + p_tag.get("href").lstrip("/")
            else:
                profile_link = url
                
            rows.append({
                "Name": name,
                "Institution": "Malaviya National Institute of Technology Jaipur",
                "Department": dept_name,
                "Designation": desig,
                "Qualification": qual,
                "Email": email,
                "Profile URL": profile_link
            })
            
    df = pd.DataFrame(rows).drop_duplicates(subset=["Email", "Name"])
    out_path = os.path.join(OUTPUT_DIR, "MNIT_Jaipur_Faculty.xlsx")
    df.to_excel(out_path, index=False)
    print(f"MNIT Jaipur complete: {len(df)} faculty saved to {out_path}")
    return df

# -------------------------------------------------------------
# 3. NIT Delhi
# -------------------------------------------------------------
def scrape_nit_delhi():
    print("--- Scraping NIT Delhi ---")
    url = "https://faculty.nitdelhi.ac.in"
    html = fetch(url, timeout=12)
    if not html:
        print("Failed to fetch NIT Delhi")
        return pd.DataFrame()
        
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    
    # Locate all faculty cards/boxes
    for a in soup.find_all("a", href=re.compile(r"mailto:.*@nitdelhi\.ac\.in", re.I)):
        raw_email = a.get("href").replace("mailto:", "").strip().lower()
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@nitdelhi\.ac\.in", raw_email)
        if not emails:
            continue
        email = emails[0]
        
        # Parent container
        parent = a.find_parent("div", class_=lambda c: c and any(k in str(c).lower() for k in ["card", "member", "faculty", "box", "team", "col"])) or a.find_parent("div")
        if not parent:
            continue
            
        lines = [clean_text(x) for x in parent.get_text(separator="\n").split("\n") if clean_text(x)]
        name = ""
        desig = "Faculty"
        dept = "National Institute of Technology Delhi"
        qual = ""
        
        for l in lines:
            if not name and any(l.startswith(p) for p in ["Dr.", "Prof.", "Dr ", "Prof ", "Mr.", "Ms."]):
                name = l
            elif any(d in l.lower() for d in ["assistant professor", "associate professor", "professor"]):
                desig = l
            elif any(d in l.lower() for d in ["computer science", "electronics", "electrical", "mechanical", "civil", "applied sciences", "humanities"]):
                dept = l
            elif any(q in l.lower() for q in ["ph.d", "ph d", "m.tech", "b.tech", "m.sc"]):
                qual = l
                
        if not name and lines:
            name = lines[0]
            
        # Profile link
        p_link = a.get("href")
        card_link = parent.find("a", href=lambda h: h and "/faculty/" in h)
        profile_url = card_link.get("href") if card_link else url
        
        rows.append({
            "Name": name,
            "Institution": "National Institute of Technology Delhi",
            "Department": dept,
            "Designation": desig,
            "Qualification": qual,
            "Email": email,
            "Profile URL": profile_url
        })
        
    df = pd.DataFrame(rows).drop_duplicates(subset=["Email", "Name"])
    out_path = os.path.join(OUTPUT_DIR, "NIT_Delhi_Faculty.xlsx")
    df.to_excel(out_path, index=False)
    print(f"NIT Delhi complete: {len(df)} faculty saved to {out_path}")
    return df

# -------------------------------------------------------------
# 4. NIT Uttarakhand
# -------------------------------------------------------------
def scrape_nit_uttarakhand():
    print("--- Scraping NIT Uttarakhand ---")
    dept_urls = [
        ("https://nituk.ac.in/computer-science-engineering/peoples", "Computer Science and Engineering"),
        ("https://nituk.ac.in/electronics-engineering/peoples", "Electronics Engineering"),
        ("https://nituk.ac.in/electrical-engineering/peoples", "Electrical Engineering"),
        ("https://nituk.ac.in/mechanical-engineering/peoples", "Mechanical Engineering"),
        ("https://nituk.ac.in/civil-engineering/peoples", "Civil Engineering"),
        ("https://nituk.ac.in/mathematics/peoples", "Mathematics"),
        ("https://nituk.ac.in/humanities-and-social-science/peoples", "Humanities and Social Sciences")
    ]
    
    rows = []
    for url, dept_name in dept_urls:
        html = fetch(url, timeout=10)
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        
        # Each faculty member is inside a td or table row containing their email
        for td in soup.find_all(["td", "div"]):
            td_text = td.get_text(separator="\n")
            if "@nituk.ac.in" in td_text and "Designation" in td_text:
                emails = re.findall(r"[a-zA-Z0-9_.+-]+@nituk\.ac\.in", td_text)
                if not emails:
                    continue
                email = emails[0].lower()
                if email in ["nituttarakhand@nituk.ac.in", "registrar@nituk.ac.in"]:
                    continue
                    
                lines = [clean_text(x) for x in td_text.split("\n") if clean_text(x)]
                name = ""
                desig = "Faculty"
                qual = ""
                
                # Extract strong tag for name if available
                strong_tag = td.find("strong")
                if strong_tag and clean_text(strong_tag.text):
                    name = clean_text(strong_tag.text)
                    
                for idx, line in enumerate(lines):
                    if not name and any(line.startswith(p) for p in ["Dr.", "Prof.", "Dr ", "Prof ", "Mr.", "Ms."]):
                        name = line
                    if "Designation :" in line or "Designation:" in line:
                        desig = clean_text(line.split(":")[-1])
                    if "Expertise :" in line or "Expertise:" in line:
                        qual = clean_text(line.split(":")[-1])
                        
                if not name and lines:
                    name = lines[0]
                    
                rows.append({
                    "Name": name,
                    "Institution": "National Institute of Technology Uttarakhand",
                    "Department": dept_name,
                    "Designation": desig,
                    "Qualification": qual,
                    "Email": email,
                    "Profile URL": url
                })
                
    df = pd.DataFrame(rows).drop_duplicates(subset=["Email", "Name"])
    out_path = os.path.join(OUTPUT_DIR, "NIT_Uttarakhand_Faculty.xlsx")
    df.to_excel(out_path, index=False)
    print(f"NIT Uttarakhand complete: {len(df)} faculty saved to {out_path}")
    return df

# -------------------------------------------------------------
# 5. MNNIT Allahabad
# -------------------------------------------------------------
def scrape_mnnit_allahabad():
    print("--- Scraping MNNIT Allahabad ---")
    dept_pages = [
        ("https://www.mnnit.ac.in/index.php/department/engineering/am/appmecfp", "Applied Mechanics"),
        ("https://www.mnnit.ac.in/index.php/department/engineering/biotech/biotechfp", "Biotechnology"),
        ("https://www.mnnit.ac.in/index.php/department/engineering/ce/cefp", "Civil Engineering"),
        ("https://www.mnnit.ac.in/index.php/department/engineering/cm", "Chemical Engineering"),
        ("https://www.mnnit.ac.in/index.php/department/engineering/csed", "Computer Science and Engineering"),
        ("https://www.mnnit.ac.in/index.php/department/engineering/ece/ecefp", "Electronics and Communication Engineering"),
        ("https://www.mnnit.ac.in/index.php/department/engineering/ee/eefp", "Electrical Engineering"),
        ("https://www.mnnit.ac.in/index.php/department/engineering/me/mefpa", "Mechanical Engineering"),
        ("https://www.mnnit.ac.in/index.php/department/hss/hssfp", "Humanities and Social Sciences"),
        ("https://www.mnnit.ac.in/index.php/department/mgmt-studies/mgmt-studiesfp", "School of Management Studies"),
        ("https://www.mnnit.ac.in/index.php/department/sciences/chem/chemfp", "Chemistry"),
        ("https://www.mnnit.ac.in/index.php/department/sciences/maths/mathsfp", "Mathematics"),
        ("https://www.mnnit.ac.in/index.php/department/sciences/physics/physicsfp", "Physics"),
        ("https://www.mnnit.ac.in/index.php/department/others/gis-cell", "GIS Cell")
    ]
    
    rows = []
    
    def process_dept(args):
        url, dept_name = args
        html = fetch(url, timeout=12)
        if not html:
            return []
        soup = BeautifulSoup(html, "html.parser")
        dept_rows = []
        
        # Profile links follow pattern /profile/<username>
        profile_links = soup.find_all("a", href=re.compile(r"/profile/[a-zA-Z0-9_\.]+", re.I))
        seen_users = set()
        
        for pl in profile_links:
            href = pl.get("href")
            match = re.search(r"/profile/([a-zA-Z0-9_\.]+)", href)
            if not match:
                continue
            username = match.group(1).lower()
            if username in seen_users or username in ["index", "home"]:
                continue
            seen_users.add(username)
            
            profile_url = f"https://www.mnnit.ac.in/profile/{username}"
            email = f"{username}@mnnit.ac.in"
            
            # Fetch profile page to get full details (name, designation, education)
            prof_html = fetch(profile_url, timeout=8)
            name = ""
            desig = "Faculty"
            qual = ""
            
            if prof_html:
                p_soup = BeautifulSoup(prof_html, "html.parser")
                h1 = p_soup.find("h1")
                if h1 and clean_text(h1.text):
                    name = clean_text(h1.text)
                
                # Check lines
                full_txt = p_soup.get_text(separator="\n")
                lines = [clean_text(x) for x in full_txt.split("\n") if clean_text(x)]
                for idx, line in enumerate(lines):
                    if not name and any(line.startswith(p) for p in ["Dr.", "Prof.", "Dr ", "Prof ", "Mr.", "Ms."]):
                        name = line
                    if any(d in line.lower() for d in ["professor", "assistant professor", "associate professor"]):
                        desig = line
                    if "education" in line.lower() and idx + 1 < len(lines):
                        qual = lines[idx+1]
                        
                # Check for unobfuscated email in profile text if different
                emails_found = re.findall(r"([a-zA-Z0-9_.+-]+)\[at\]mnnit\[dot\]ac\[dot\]in", prof_html)
                if emails_found:
                    email = f"{emails_found[0]}@mnnit.ac.in"
            
            if not name:
                name = pl.get_text(strip=True) or username.capitalize()
                
            dept_rows.append({
                "Name": name,
                "Institution": "Motilal Nehru National Institute of Technology Allahabad",
                "Department": dept_name,
                "Designation": desig,
                "Qualification": qual,
                "Email": email,
                "Profile URL": profile_url
            })
        return dept_rows
        
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(process_dept, dept_pages)
        for r in results:
            rows.extend(r)
            
    df = pd.DataFrame(rows).drop_duplicates(subset=["Email", "Name"])
    out_path = os.path.join(OUTPUT_DIR, "MNNIT_Allahabad_Faculty.xlsx")
    df.to_excel(out_path, index=False)
    print(f"MNNIT Allahabad complete: {len(df)} faculty saved to {out_path}")
    return df

if __name__ == "__main__":
    scrape_nit_jalandhar()
    scrape_mnit_jaipur()
    scrape_nit_delhi()
    scrape_nit_uttarakhand()
    scrape_mnnit_allahabad()
