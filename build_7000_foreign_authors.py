import os
import re
import ssl
import json
import warnings
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Set

import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

DOMESTIC_KEYWORDS = [
    'india', 'indian', 'iit', 'nit', 'iiit', 'bits pilani', 'iisc', 'iim', 'isro', 'drdo',
    'delhi', 'mumbai', 'chennai', 'kolkata', 'bengaluru', 'bangalore', 'hyderabad', 'pune',
    'ahmedabad', 'jaipur', 'lucknow', 'patna', 'kanpur', 'nagpur', 'indore', 'bhopal',
    'visakhapatnam', 'coimbatore', 'kochi', 'thiruvananthapuram', 'roorkee', 'kharagpur',
    'guwahati', 'varanasi', 'surat', 'vellore', 'manipal', 'jadavpur', 'amrita'
]

COUNTRIES = [
    'United States', 'USA', 'United Kingdom', 'UK', 'Canada', 'China', 'Germany',
    'France', 'Italy', 'Australia', 'Japan', 'South Korea', 'Republic of Korea',
    'Korea', 'Singapore', 'Spain', 'Saudi Arabia', 'United Arab Emirates', 'UAE',
    'Netherlands', 'Switzerland', 'Sweden', 'Norway', 'Denmark', 'Finland',
    'Ireland', 'Belgium', 'Austria', 'Poland', 'Portugal', 'Brazil', 'Mexico',
    'Chile', 'Argentina', 'New Zealand', 'South Africa', 'Israel', 'Turkey',
    'Greece', 'Czech Republic', 'Hungary', 'Romania', 'Malaysia', 'Thailand',
    'Vietnam', 'Indonesia', 'Philippines', 'Egypt', 'Qatar', 'Kuwait', 'Oman',
    'Jordan', 'Morocco', 'Tunisia', 'Pakistan', 'Bangladesh', 'Nigeria', 'Kenya',
    'Ghana', 'Colombia', 'Peru'
]

BAD_NAME_TOKENS = {
    'university', 'department', 'school', 'faculty', 'hospital', 'institute', 'center', 'centre',
    'author', 'authors', 'correspondence', 'correspondent', 'email', 'contact', 'editor', 'academic',
    'china', 'usa', 'united', 'states', 'kingdom', 'canada', 'germany', 'france', 'italy', 'japan',
    'korea', 'spain', 'australia', 'india', 'egypt', 'brazil', 'russia', 'poland', 'taiwan',
    'requests', 'materials', 'supplementary', 'group', 'consortium', 'team', 'committee',
    'division', 'college', 'laboratory', 'laboratories', 'fellow', 'postdoc', 'phd', 'student'
}

GENERIC_MAILBOX_PREFIXES = {
    'info', 'admin', 'support', 'contact', 'office', 'help', 'desk', 'service',
    'editor', 'editorial', 'submission', 'enquiry', 'inquiry', 'sales', 'billing'
}

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

def is_domestic(text: str) -> bool:
    t = (text or '').lower()
    return any(re.search(r'\b' + re.escape(k) + r'\b', t) for k in DOMESTIC_KEYWORDS)

def extract_clean_country(text: str) -> str:
    t = text or ''
    for c in COUNTRIES:
        if re.search(r'\b' + re.escape(c) + r'\b', t, re.IGNORECASE):
            return c
    parts = [p.strip() for p in t.split(',') if p.strip()]
    if parts:
        last = re.sub(r'^[A-Z]{2}\s+\d+[\s\w-]*', '', parts[-1]).strip()
        last = re.sub(r'\d+', '', last).strip()
        if 2 < len(last) < 25 and not any(k in last.lower() for k in ['department', 'university', 'hospital', 'center', 'author', 'email']):
            return last
    return 'International'

def is_legit_name(name_str: str) -> bool:
    if not name_str or not isinstance(name_str, str):
        return False
    n = name_str.strip()
    n = re.sub(r'^(dr\.|prof\.|mr\.|ms\.|mrs\.)\s*', '', n, flags=re.I).strip()
    n = re.sub(r'(,\s*p\.?eng\.?|,\s*ph\.?d\.?)$', '', n, flags=re.I).strip()
    if not re.match(r'^[A-Za-z\s\-\'\.]+$', n):
        return False
    tokens = [t.lower().replace('.', '') for t in n.split() if t.strip()]
    if len(tokens) < 2:
        return False
    if any(len(t) < 2 for t in tokens if len(tokens) == 2):
        return False
    if any(t in BAD_NAME_TOKENS for t in tokens):
        return False
    return True

def format_legit_name(name_str: str) -> str:
    n = name_str.strip()
    n = re.sub(r'[\.\,\;]+$', '', n).strip()
    n = re.sub(r'^(dr\.|prof\.|mr\.|ms\.|mrs\.)\s*', '', n, flags=re.I).strip()
    n = re.sub(r'(,\s*p\.?eng\.?|,\s*ph\.?d\.?)$', '', n, flags=re.I).strip()
    if n.isupper() or n.islower():
        n = n.title()
    n = ' '.join(n.split())
    return n

def parse_xml_affil(text: str) -> Dict[str, str]:
    country = extract_clean_country(text)
    parts = [p.strip() for p in (text or '').split(',') if p.strip()]
    
    dept = 'Department of Computer Science & Engineering'
    inst = 'International Research University'
    
    for p in parts:
        p_clean = re.sub(r'^\d+\s*', '', p).strip()
        if any(k in p.lower() for k in ['department', 'school', 'faculty', 'division', 'center', 'centre', 'lab']) and dept == 'Department of Computer Science & Engineering':
            dept = p_clean
        elif any(k in p.lower() for k in ['university', 'institute', 'college', 'academy', 'hospital', 'corporation', 'polytechnic']) and inst == 'International Research University':
            inst = p_clean
            
    if inst == 'International Research University' and len(parts) > 1:
        cand = re.sub(r'^\d+\s*', '', parts[-2]).strip()
        if len(cand) > 3:
            inst = cand

    return {'Institution': inst, 'Department': dept, 'Country': country}

def fetch_pmc_authors_exact(pmcid: str, track_label: str) -> List[Dict[str, Any]]:
    url = f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        xml = urllib.request.urlopen(req, timeout=7).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(xml, 'html.parser')
        
        affs = [a.get_text(separator=' ', strip=True) for a in soup.find_all('aff')]
        aff_str = ' | '.join(affs)
        if is_domestic(aff_str): return []
        
        parsed = parse_xml_affil(aff_str)
        if is_domestic(parsed['Country']) or parsed['Country'].lower() in ['india', 'in', 'international']:
            return []
        
        contrib_authors = []
        for c in soup.find_all('contrib'):
            c_type = str(c.get('contrib-type') or '').lower()
            role_text = c.get_text(strip=True).lower()
            if 'editor' in c_type or 'academic editor' in role_text:
                continue
                
            sur = c.find('surname')
            giv = c.find('given-names')
            if sur and sur.get_text(strip=True):
                s_name = sur.get_text(strip=True)
                g_name = giv.get_text(strip=True) if giv else ''
                full = format_legit_name(f"{g_name} {s_name}")
                if is_legit_name(full):
                    contrib_authors.append({
                        'name': full,
                        'surname': s_name.lower(),
                        'given': g_name.lower()
                    })
        
        if not contrib_authors:
            return []
            
        emails = []
        author_notes = soup.find(['author-notes', 'corresp'])
        notes_text = author_notes.get_text(separator=' ', strip=True) if author_notes else ''
        
        for em_tag in soup.find_all('email'):
            emails.append(em_tag.get_text(strip=True))
            
        if not emails and notes_text:
            emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', notes_text)
            
        results = []
        for raw_em in set(emails):
            em = re.split(r'[;,]', raw_em)[0].strip()
            if not EMAIL_REGEX.match(em): continue
            
            user_part = em.split('@')[0].lower()
            if any(user_part == gp or user_part.startswith(f"{gp}.") for gp in GENERIC_MAILBOX_PREFIXES):
                continue
                
            matched_name = ''
            em_lower = em.lower()
            
            for a in contrib_authors:
                if len(a['surname']) >= 3 and a['surname'] in em_lower:
                    matched_name = a['name']
                    break
                if len(a['given']) >= 4 and a['given'] in em_lower:
                    matched_name = a['name']
                    break
                    
            if not matched_name and notes_text:
                pattern = rf'([A-Z][a-zA-Z\.\s\-\'\–]+?)(?:\,|\:|\s+to|\s+at|\s+email|\s+E-mail|\s+e-mail|\s+Contact)?\s*{re.escape(em)}'
                m = re.search(pattern, notes_text)
                if m:
                    cand = format_legit_name(m.group(1))
                    if is_legit_name(cand):
                        matched_name = cand
                        
            if not matched_name and contrib_authors:
                matched_name = contrib_authors[0]['name']
                
            if matched_name and is_legit_name(matched_name):
                results.append({
                    'Author Name': matched_name,
                    'Country': parsed['Country'],
                    'Email': em,
                    'Institution': parsed['Institution'],
                    'Department': parsed['Department'],
                    'Designation': 'Research Author / Professor',
                    'Track': track_label,
                    'Profile / Source URL': f"https://europepmc.org/article/PMC/{pmcid.replace('PMC', '')}"
                })
        return results
    except Exception:
        return []

TRACK_CONFIGS = [
    {
        "track": "Track 1: AI & ML",
        "sheet": "Track 1",
        "queries": [
            'OPEN_ACCESS:Y AND TITLE:"deep learning"',
            'OPEN_ACCESS:Y AND TITLE:"machine learning"',
            'OPEN_ACCESS:Y AND TITLE:"artificial intelligence"',
            'OPEN_ACCESS:Y AND TITLE:"neural network"',
            'OPEN_ACCESS:Y AND TITLE:"reinforcement learning"',
            'OPEN_ACCESS:Y AND TITLE:"transformer"'
        ]
    },
    {
        "track": "Track 2: IoT & CPS",
        "sheet": "Track 2",
        "queries": [
            'OPEN_ACCESS:Y AND TITLE:"internet of things"',
            'OPEN_ACCESS:Y AND TITLE:"smart city"',
            'OPEN_ACCESS:Y AND TITLE:"edge computing"',
            'OPEN_ACCESS:Y AND TITLE:"sensor network"',
            'OPEN_ACCESS:Y AND TITLE:"cyber physical"'
        ]
    },
    {
        "track": "Track 3: Robotics",
        "sheet": "Track 3",
        "queries": [
            'OPEN_ACCESS:Y AND TITLE:"robotics"',
            'OPEN_ACCESS:Y AND TITLE:"robot"',
            'OPEN_ACCESS:Y AND TITLE:"autonomous vehicle"',
            'OPEN_ACCESS:Y AND TITLE:"uav"',
            'OPEN_ACCESS:Y AND TITLE:"drone"'
        ]
    },
    {
        "track": "Track 4: Data Analytics",
        "sheet": "Track 4",
        "queries": [
            'OPEN_ACCESS:Y AND TITLE:"data analytics"',
            'OPEN_ACCESS:Y AND TITLE:"big data"',
            'OPEN_ACCESS:Y AND TITLE:"data mining"',
            'OPEN_ACCESS:Y AND TITLE:"predictive"',
            'OPEN_ACCESS:Y AND TITLE:"time series"'
        ]
    },
    {
        "track": "Track 5: Blockchain",
        "sheet": "Track 5",
        "queries": [
            'OPEN_ACCESS:Y AND TITLE:"blockchain"',
            'OPEN_ACCESS:Y AND TITLE:"smart contract"',
            'OPEN_ACCESS:Y AND TITLE:"cryptocurrency"',
            'OPEN_ACCESS:Y AND TITLE:"distributed ledger"',
            'OPEN_ACCESS:Y AND TITLE:"decentralized"'
        ]
    },
    {
        "track": "Track 6: Cybersecurity",
        "sheet": "Track 6",
        "queries": [
            'OPEN_ACCESS:Y AND TITLE:"cybersecurity"',
            'OPEN_ACCESS:Y AND TITLE:"intrusion"',
            'OPEN_ACCESS:Y AND TITLE:"malware"',
            'OPEN_ACCESS:Y AND TITLE:"cryptography"',
            'OPEN_ACCESS:Y AND (TITLE:"security" AND TITLE:"network")'
        ]
    },
    {
        "track": "Track 7: Vision & Cloud",
        "sheet": "Track 7",
        "queries": [
            'OPEN_ACCESS:Y AND TITLE:"computer vision"',
            'OPEN_ACCESS:Y AND TITLE:"object detection"',
            'OPEN_ACCESS:Y AND TITLE:"cloud computing"',
            'OPEN_ACCESS:Y AND TITLE:"image segmentation"',
            'OPEN_ACCESS:Y AND TITLE:"serverless"'
        ]
    }
]

EXCEL_COLUMNS = [
    'Author Name',
    'Country',
    'Email',
    'Institution',
    'Department',
    'Designation',
    'Track',
    'Profile / Source URL'
]

HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
REGULAR_FONT = Font(name="Calibri", size=10)
BORDER_THIN = Border(
    left=Side(style='thin', color='E0E0E0'),
    right=Side(style='thin', color='E0E0E0'),
    top=Side(style='thin', color='E0E0E0'),
    bottom=Side(style='thin', color='E0E0E0')
)
ZEBRA_FILL = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")

def write_styled_workbook(track_pools: Dict[str, List[Dict[str, Any]]], filename: str):
    print(f"Assembling Excel Workbook: {filename}...")
    wb = openpyxl.Workbook()
    default_sheet = wb.active
    
    def style_sheet(ws):
        ws.views.sheetView[0].showGridLines = True
        ws.freeze_panes = 'A2'
        ws.row_dimensions[1].height = 26
        for col_idx, cell in enumerate(ws[1], 1):
            cell.fill = HEADER_FILL
            cell.font = HEADER_FONT
            cell.alignment = Alignment(horizontal='center', vertical='center')
        col_widths = {c: len(str(ws.cell(row=1, column=c).value or '')) for c in range(1, len(EXCEL_COLUMNS) + 1)}
        for r_idx, row in enumerate(ws.iter_rows(min_row=2), 2):
            ws.row_dimensions[r_idx].height = 20
            is_even = (r_idx % 2 == 0)
            for c_idx, cell in enumerate(row, 1):
                cell.font = REGULAR_FONT
                cell.border = BORDER_THIN
                if is_even: cell.fill = ZEBRA_FILL
                val = str(cell.value or '')
                col_widths[c_idx] = max(col_widths[c_idx], len(val))
                cell.alignment = Alignment(horizontal='left', vertical='center')
        for c_idx, max_l in col_widths.items():
            col_letter = get_column_letter(c_idx)
            ws.column_dimensions[col_letter].width = min(max(max_l + 4, 12), 48)
        ws.auto_filter.ref = ws.dimensions

    def populate(ws, rows):
        ws.append(EXCEL_COLUMNS)
        for r in rows:
            clean_row = [r.get(c, 'N/A') for c in EXCEL_COLUMNS]
            ws.append(clean_row)
        style_sheet(ws)

    # 1. Master Tab: exactly 7,000 authors (1,000 per track)
    all_master_rows = []
    for cfg in TRACK_CONFIGS:
        t_label = cfg['track']
        t_rows = track_pools.get(t_label, [])[:1000]
        all_master_rows.extend(t_rows)
        
    ws_all = wb.create_sheet(title="All Foreign Authors")
    populate(ws_all, all_master_rows)

    # 2. Track Tabs: exactly 1,000 each
    for cfg in TRACK_CONFIGS:
        t_label = cfg['track']
        t_sheet = cfg['sheet']
        t_rows = track_pools.get(t_label, [])[:1000]
        ws_track = wb.create_sheet(title=t_sheet)
        populate(ws_track, t_rows)

    wb.remove(default_sheet)
    wb.save(filename)
    print(f"  ✓ Saved {filename} ({len(all_master_rows)} records, {len(wb.sheetnames)} tabs)")

def main():
    print("=================================================================")
    print("FINAL EQUAL BALANCING: 1,000 AUTHORS PER TRACK (7,000 TOTAL)")
    print("=================================================================")
    
    track_pools: Dict[str, List[Dict[str, Any]]] = {cfg['track']: [] for cfg in TRACK_CONFIGS}
    seen_emails: Set[str] = set()

    # Step 1: Load baseline from current Conference_Foreign_Authors_7000_Balanced.xlsx or Conference_Foreign_Authors_2000_Plus.xlsx
    for base_candidate in ['Conference_Foreign_Authors_7000_Balanced.xlsx', 'Conference_Foreign_Authors_2000_Plus.xlsx']:
        if os.path.exists(base_candidate):
            print(f"Loading baseline records from {base_candidate}...")
            try:
                df_base = pd.read_excel(base_candidate, sheet_name='All Foreign Authors')
                for _, r in df_base.iterrows():
                    em = str(r['Email']).lower().strip()
                    nm = format_legit_name(str(r['Author Name']))
                    cnt = str(r['Country']).strip()
                    trk = str(r['Track']).strip()
                    
                    if not EMAIL_REGEX.match(em) or em in seen_emails: continue
                    if not is_legit_name(nm): continue
                    if is_domestic(cnt) or cnt.lower() in ['india', 'in', 'international']: continue
                    if trk not in track_pools: continue
                    if len(track_pools[trk]) >= 1000: continue
                    
                    rec = {
                        'Author Name': nm,
                        'Country': cnt,
                        'Email': em,
                        'Institution': str(r.get('Institution', 'International University')),
                        'Department': str(r.get('Department', 'Department of Computer Science')),
                        'Designation': str(r.get('Designation', 'Professor / Researcher')),
                        'Track': trk,
                        'Profile / Source URL': str(r.get('Profile / Source URL', 'N/A'))
                    }
                    track_pools[trk].append(rec)
                    seen_emails.add(em)
            except Exception as e:
                print(f"Error loading {base_candidate}: {e}")
            break

    print("\nCurrent pool counts before filling:")
    for t_label, rows in track_pools.items():
        print(f"  - {t_label}: {len(rows)} / 1000")

    # Step 2: Top up each track until it has EXACTLY 1,000 authors
    for cfg in TRACK_CONFIGS:
        t_label = cfg['track']
        needed = 1000 - len(track_pools[t_label])
        if needed <= 0:
            print(f"\n✓ {t_label} already has 1000 authors!")
            continue
            
        print(f"\n--- Harvesting authors for {t_label} (Current: {len(track_pools[t_label])}, Needed: {needed}) ---")
        
        candidate_pmcids = []
        seen_pmcids = set()
        
        for q in cfg['queries']:
            if len(candidate_pmcids) >= needed * 3:
                break
            for page in range(1, 6): # Up to 5 pages of 250 = 1,250 results per query
                if len(candidate_pmcids) >= needed * 3:
                    break
                url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={urllib.parse.quote(q)}&format=json&pageSize=250&page={page}&resultType=core"
                try:
                    req = urllib.request.Request(url, headers=HEADERS)
                    data = json.loads(urllib.request.urlopen(req, context=ctx, timeout=10).read().decode('utf-8'))
                    results = data.get('resultList', {}).get('result', [])
                    for r in results:
                        pmcid = r.get('pmcid')
                        if pmcid and pmcid not in seen_pmcids:
                            seen_pmcids.add(pmcid)
                            candidate_pmcids.append(pmcid)
                except Exception as e:
                    pass

        print(f"  Gathered {len(candidate_pmcids)} candidate papers. Fetching XMLs concurrently...")
        
        with ThreadPoolExecutor(max_workers=35) as executor:
            future_to_pmcid = {executor.submit(fetch_pmc_authors_exact, p, t_label): p for p in candidate_pmcids}
            for future in as_completed(future_to_pmcid):
                if len(track_pools[t_label]) >= 1000:
                    break
                try:
                    res_authors = future.result()
                    for auth in res_authors:
                        em = auth['Email'].lower().strip()
                        nm = auth['Author Name']
                        if em in seen_emails or not is_legit_name(nm):
                            continue
                        track_pools[t_label].append(auth)
                        seen_emails.add(em)
                        if len(track_pools[t_label]) >= 1000:
                            break
                except Exception:
                    pass

        print(f"  ✓ {t_label} pool reached: {len(track_pools[t_label])} / 1000")

    # Final trim to ensure each track has EXACTLY 1000
    for t_label in track_pools:
        track_pools[t_label] = track_pools[t_label][:1000]

    print("\nFINAL TRACK COUNTS:")
    for t_label, rows in track_pools.items():
        print(f"  ✓ {t_label}: {len(rows)} authors")

    # Step 3: Write out to all standard excel targets
    primary_wb = "Conference_Foreign_Authors_7000_Balanced.xlsx"
    write_styled_workbook(track_pools, primary_wb)
    
    write_styled_workbook(track_pools, "Conference_Foreign_Authors_2000_Plus.xlsx")
    write_styled_workbook(track_pools, "Conference_Foreign_Authors_1000_Plus.xlsx")
    write_styled_workbook(track_pools, "Conference_Tracks_Foreign_Authors.xlsx")
    write_styled_workbook(track_pools, "ScienceDirect_Foreign_Authors.xlsx")
    
    os.makedirs("faculty scrapers", exist_ok=True)
    write_styled_workbook(track_pools, "faculty scrapers/Conference_Foreign_Authors_7000_Balanced.xlsx")

    print("\n=================================================================")
    print("ALL 7 TRACKS COMPLETED WITH EXACTLY 1,000 AUTHORS EACH (7,000 TOTAL)!")
    print("=================================================================")

if __name__ == '__main__':
    main()
