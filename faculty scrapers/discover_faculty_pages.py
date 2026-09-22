import requests
import urllib3
import re
from bs4 import BeautifulSoup
import json

urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

candidates = {
    "IIIT_Allahabad": [
        "https://www.iiita.ac.in/faculty/",
        "https://it.iiita.ac.in/?pg=faculty",
        "https://ece.iiita.ac.in/?pg=faculty",
        "https://as.iiita.ac.in/?pg=faculty"
    ],
    "IIITM_Gwalior": [
        "https://www.iiitm.ac.in/index.php/faculty-list",
        "https://www.iiitm.ac.in/index.php/en/faculty",
        "https://www.iiitm.ac.in/index.php/en/academics/faculty",
        "https://www.iiitm.ac.in/index.php/en/"
    ],
    "IIITDM_Jabalpur": [
        "https://iiitdmj.ac.in/faculty.php",
        "https://iiitdmj.ac.in/cse/faculty.php",
        "https://iiitdmj.ac.in/ece/faculty.php",
        "https://iiitdmj.ac.in/me/faculty.php"
    ],
    "IIITDM_Kancheepuram": [
        "https://www.iiitdm.ac.in/people/faculty",
        "https://www.iiitdm.ac.in/faculty"
    ],
    "IIITDM_Kurnool": [
        "https://iiitk.ac.in/Faculty/page"
    ],
    "IIIT_Hyderabad": [
        "https://www.iiit.ac.in/people/faculty/"
    ],
    "IIIT_Bangalore": [
        "https://www.iiitb.ac.in/faculty-members",
        "https://www.iiitb.ac.in/faculty",
        "https://iiitb.ac.in/people/faculty"
    ],
    "IIIT_Bhubaneswar": [
        "https://www.iiit-bh.ac.in/faculty",
        "https://www.iiit-bh.ac.in/faculty-members",
        "https://iiit-bh.ac.in/people/faculty"
    ],
    "IIIT_Naya_Raipur": [
        "https://www.iiitnr.ac.in/faculty",
        "https://www.iiitnr.ac.in/content/faculty"
    ],
    "IIIT_SriCity": [
        "https://www.iiits.ac.in/people/regular-faculty/"
    ],
    "IIIT_Guwahati": [
        "https://www.iiitg.ac.in/faculty.php",
        "https://iiitg.ac.in/faculty"
    ],
    "IIIT_Vadodara": [
        "http://iiitvadodara.ac.in/faculty.php"
    ],
    "IIIT_Kota": [
        "https://iiitkota.ac.in/faculty"
    ],
    "IIIT_Trichy": [
        "https://www.iiitt.ac.in/faculty"
    ],
    "IIIT_Una": [
        "https://iiitu.ac.in/faculty/",
        "https://iiitu.ac.in/school-of-computing/faculty",
        "https://iiitu.ac.in/faculty-profile"
    ],
    "IIIT_Sonepat": [
        "http://www.iiitsonepat.ac.in/faculty",
        "http://www.iiitsonepat.ac.in/faculty-members"
    ],
    "IIIT_Kalyani": [
        "http://iiitkalyani.ac.in/faculty.html"
    ],
    "IIIT_Lucknow": [
        "https://iiitl.ac.in/faculty/",
        "https://www.iiitl.ac.in/faculty/"
    ],
    "IIIT_Dharwad": [
        "https://iiitdwd.ac.in/Faculty.php",
        "https://iiitdwd.ac.in/people.php",
        "https://iiitdwd.ac.in/faculty"
    ],
    "IIIT_Kottayam": [
        "https://www.iiitkottayam.ac.in/#!/faculty",
        "https://www.iiitkottayam.ac.in/faculty",
        "https://iiitkottayam.ac.in/people/faculty"
    ],
    "IIIT_Manipur": [
        "http://www.iiitmanipur.ac.in/faculty.html",
        "http://www.iiitmanipur.ac.in/faculty",
        "http://iiitmanipur.ac.in"
    ],
    "IIIT_Nagpur": [
        "https://www.iiitn.ac.in/faculty.php",
        "https://iiitn.ac.in/faculty",
        "https://www.iiitn.ac.in/people/faculty"
    ],
    "IIIT_Pune": [
        "https://www.iiitp.ac.in/faculty"
    ],
    "IIIT_Ranchi": [
        "https://www.iiitranchi.ac.in/faculty",
        "https://iiitranchi.ac.in/Faculty.php",
        "http://iiitranchi.ac.in"
    ],
    "IIIT_Bhagalpur": [
        "https://www.iiitbh.ac.in/faculty"
    ],
    "IIIT_Bhopal": [
        "https://iiitbhopal.ac.in/faculty"
    ],
    "IIIT_Surat": [
        "https://www.iiitsurat.ac.in/faculty",
        "https://www.iiitsurat.ac.in/faculty.php"
    ],
    "IIIT_Agartala": [
        "http://www.iiitagartala.ac.in/faculty",
        "http://iiitagartala.ac.in"
    ],
    "IIIT_Raichur": [
        "https://iiitr.ac.in/faculty"
    ]
}

results = {}

for inst, urls in candidates.items():
    found_url = None
    for u in urls:
        try:
            r = requests.get(u, headers=headers, verify=False, timeout=6)
            if r.status_code == 200 and len(r.text) > 1000:
                print(f"[FOUND] {inst} -> {u} ({len(r.text)} chars)", flush=True)
                found_url = u
                results[inst] = {"url": u, "length": len(r.text)}
                break
            else:
                print(f"[{r.status_code}] {inst} -> {u}", flush=True)
        except Exception as e:
            print(f"[FAIL] {inst} -> {u}: {e}", flush=True)
    if not found_url:
        print(f"[NOT FOUND] {inst}", flush=True)
        results[inst] = {"url": None}

with open("endpoint_map.json", "w") as f:
    json.dump(results, f, indent=2)
print("Saved endpoint_map.json", flush=True)
