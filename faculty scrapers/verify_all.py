#!/usr/bin/env python3
"""
Master Verification Script for all 30 IIIT Faculty Workbooks
"""

import os
import glob
import pandas as pd

EXPECTED_COLUMNS = ['Name', 'Institution', 'Department', 'Designation', 'Qualification', 'Email', 'Profile URL']

IIIT_CATEGORIES = {
    "Centrally Funded (MoE)": [
        ("IIIT Allahabad", "IIIT_Allahabad_Faculty.xlsx"),
        ("IIITDM Kancheepuram", "IIITDM_Kancheepuram_Faculty.xlsx"),
        ("IIITDM Kurnool", "IIITDM_Kurnool_Faculty.xlsx"),
        ("IIITM Gwalior", "IIITM_Gwalior_Faculty.xlsx"),
        ("IIITDM Jabalpur", "IIITDM_Jabalpur_Faculty.xlsx"),
    ],
    "State / Autonomous": [
        ("IIIT Delhi", "IIIT_Delhi_Complete_Faculty.xlsx"),
        ("IIIT Bangalore", "IIIT_Bangalore_Faculty.xlsx"),
        ("IIIT Bhubaneswar", "IIIT_Bhubaneswar_Faculty.xlsx"),
        ("IIIT Hyderabad", "IIIT_Hyderabad_Faculty.xlsx"),
        ("IIIT Naya Raipur", "IIIT_Naya_Raipur_Faculty.xlsx"),
    ],
    "Public-Private Partnership (PPP)": [
        ("IIIT Sri City", "IIIT_SriCity_Faculty.xlsx"),
        ("IIIT Guwahati", "IIIT_Guwahati_Faculty.xlsx"),
        ("IIIT Vadodara", "IIIT_Vadodara_Faculty.xlsx"),
        ("IIIT Kota", "IIIT_Kota_Faculty.xlsx"),
        ("IIIT Tiruchirappalli (Trichy)", "IIIT_Trichy_Faculty.xlsx"),
        ("IIIT Lucknow", "IIIT_Lucknow_Faculty.xlsx"),
        ("IIIT Dharwad", "IIIT_Dharwad_Faculty.xlsx"),
        ("IIIT Kalyani", "IIIT_Kalyani_Faculty.xlsx"),
        ("IIIT Sonepat", "IIIT_Sonepat_Faculty.xlsx"),
        ("IIIT Manipur", "IIIT_Manipur_Faculty.xlsx"),
        ("IIIT Kottayam", "IIIT_Kottayam_Faculty.xlsx"),
        ("IIIT Pune", "IIIT_Pune_Faculty.xlsx"),
        ("IIIT Nagpur", "IIIT_Nagpur_Faculty.xlsx"),
        ("IIIT Ranchi", "IIIT_Ranchi_Faculty.xlsx"),
        ("IIIT Bhagalpur", "IIIT_Bhagalpur_Faculty.xlsx"),
        ("IIIT Bhopal", "IIIT_Bhopal_Faculty.xlsx"),
        ("IIIT Surat", "IIIT_Surat_Faculty.xlsx"),
        ("IIIT Agartala", "IIIT_Agartala_Faculty.xlsx"),
        ("IIIT Raichur", "IIIT_Raichur_Faculty.xlsx"),
        ("IIIT Una", "IIIT_Una_Faculty.xlsx"),
    ]
}

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    total_records = 0
    all_rows = []
    
    print(f"{'#':<3} | {'Category':<22} | {'Institution':<28} | {'Filename':<34} | {'Count':<6} | {'Status'}")
    print("-" * 110)
    
    idx = 1
    for category, institutions in IIIT_CATEGORIES.items():
        for name, filename in institutions:
            filepath = os.path.join(base_dir, filename)
            if not os.path.exists(filepath):
                print(f"{idx:<3} | {category:<22} | {name:<28} | {filename:<34} | {'MISSING':<6} | FAIL")
                idx += 1
                continue
            
            try:
                df = pd.read_excel(filepath)
                count = len(df)
                total_records += count
                # verify schema
                missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
                status = "OK" if not missing_cols else f"MISSING {missing_cols}"
                sample_name = str(df['Name'].dropna().iloc[0]) if count > 0 and 'Name' in df.columns else "N/A"
                print(f"{idx:<3} | {category:<22} | {name:<28} | {filename:<34} | {count:<6} | {status}")
                all_rows.append({
                    "Index": idx,
                    "Category": category,
                    "Institution": name,
                    "File": filename,
                    "Faculty Count": count,
                    "Sample Faculty": sample_name,
                    "Status": status
                })
            except Exception as e:
                print(f"{idx:<3} | {category:<22} | {name:<28} | {filename:<34} | {'ERROR':<6} | {e}")
            idx += 1
            
    print("-" * 110)
    print(f"Total Institutions Verified: {len(all_rows)} / 30")
    print(f"Total Faculty Profiles Extracted: {total_records}")

if __name__ == "__main__":
    main()
