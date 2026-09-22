import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3

# Suppress SSL verification warnings for university server cert chain
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# The main page listing all faculty members at IIIT-Delhi
url = "https://iiitd.ac.in/people/faculty"

# Add a standard user-agent so the request isn't blocked
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
 
print(f"Fetching faculty list from {url}...")
try:
    response = requests.get(url, headers=headers, verify=True, timeout=15)
except requests.exceptions.SSLError:
    # Fallback if local certificate bundle doesn't trust the server cert
    response = requests.get(url, headers=headers, verify=False, timeout=15)

response.raise_for_status()
soup = BeautifulSoup(response.content, 'html.parser')

faculty_data = []

# Department mapping based on IIIT-Delhi's official portal codes
dept_mapping = {
    '1': 'Computer Science and Engineering (CSE)',
    '2': 'Electronics and Communications Engineering (ECE)',
    '3': 'Computational Biology (CB)',
    '4': 'Mathematics',
    '5': 'Social Sciences and Humanities (SSH)',
    '6': 'Human Centered Design (HCD)',
    '7': 'Others'
}

def resolve_departments(dept_code):
    if not dept_code:
        return "N/A"
    names = [dept_mapping[ch] for ch in str(dept_code) if ch in dept_mapping]
    return ", ".join(names) if names else "N/A"

# Faculty members are represented by divs with class 'facultycard'
faculty_cards = soup.find_all('div', class_='facultycard')

for card in faculty_cards:
    post_card = card.find('div', class_='post-card')
    if not post_card:
        continue
    
    try:
        # Name
        title_el = post_card.find(class_='team-title') or post_card.find(['h2', 'h3'])
        name = title_el.get_text(strip=True) if title_el else "N/A"
        
        # Department
        dept_code = card.get('dept', '')
        department = resolve_departments(dept_code)
        
        # Omit faculty from Social Sciences and Humanities
        if "Social Sciences and Humanities" in department or "SSH" in department:
            continue
        
        # Designation
        desig_el = post_card.find(class_='team-subtitle')
        designation = desig_el.get_text(strip=True) if desig_el else "N/A"
        
        # Qualification / Description
        qualification = "N/A"
        desc_div = post_card.find('div', class_='team-description')
        if desc_div:
            p_tags = desc_div.find_all('p')
            if p_tags and 'mailto:' not in str(p_tags[0]):
                qualification = p_tags[0].get_text(strip=True)
        
        # Email
        email_tag = post_card.find('a', href=lambda href: href and "mailto:" in href)
        if email_tag:
            email = email_tag.get_text(strip=True) or email_tag.get('href', '').replace('mailto:', '').strip()
        else:
            email = "N/A"
            
        # Profile URL
        profile_url = "N/A"
        if title_el and title_el.find('a'):
            href = title_el.find('a').get('href', '')
            if href:
                profile_url = href if href.startswith('http') else f"https://iiitd.ac.in{href}"
        
        faculty_data.append({
            'Name': name,
            'Institution': 'IIIT Delhi',
            'Department': department,
            'Designation': designation,
            'Qualification': qualification,
            'Email': email,
            'Profile URL': profile_url
        })
    except Exception as e:
        print(f"Error parsing card: {e}")
        continue

# Create a dataframe and export to Excel
df = pd.DataFrame(faculty_data)
output_file = "IIITD_Complete_Faculty.xlsx"
df.to_excel(output_file, index=False)

print(f"Extraction complete! Found {len(df)} faculty members.")
print(f"Saved to {output_file}")