#!/usr/bin/env python3
"""
Scraper / Generator for IIIT Nagpur Faculty Directory
Generates faculty scrapers/IIIT_Nagpur_Faculty.xlsx
"""

import os
import pandas as pd

def get_nagpur_faculty():
    faculty_list = [
        # Leadership
        {
            "Name": "Prof. Prem Lal Patel",
            "Institution": "IIIT Nagpur",
            "Department": "Administration / Civil & Environmental",
            "Designation": "Director (Additional Charge) & Professor",
            "Qualification": "Ph.D., IIT Roorkee",
            "Email": "director@iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/director.php"
        },
        # Computer Science & Engineering (CSE)
        {
            "Name": "Dr. Milind R. Penurkar",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor & Head of Department",
            "Qualification": "Ph.D., VNIT Nagpur",
            "Email": "milind.penurkar@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Mayuri A. Digalwar",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor & Ph.D. Coordinator",
            "Qualification": "Ph.D., VNIT Nagpur",
            "Email": "mayuri.digalwar@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Jitendra V. Tembhurne",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D., VNIT Nagpur",
            "Email": "jitendra.tembhurne@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Nishat A. Ansari",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D., VNIT Nagpur",
            "Email": "nishat.ansari@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Mukesh Kumar Giluka",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D., IIT Hyderabad",
            "Email": "mukesh.giluka@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Nidhi Lal",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D., MANIT Bhopal",
            "Email": "nidhi.lal@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Richa K. Makhijani",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "richa.makhijani@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Kaushlendra Sharma",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "kaushlendra.sharma@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Rahul Semwal",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "rahul.semwal@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Khushboo A. Jain",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "khushboo.jain@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Shishupal Kumar",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "shishupal.kumar@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Anil Kumar Kushwah",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "anil.kushwah@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Aishwarya Sagar Anand Ukey",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "aishwarya.ukey@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Vrinda Yadav",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "vrinda.yadav@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Jagdish Chakole",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "jagdish.chakole@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Nileshchandra Pikle",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "nileshchandra.pikle@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Amol Bhopale",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "amol.bhopale@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Suvra Jyoti Choudhury",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "suvrajyoti.choudhury@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Neha R. Kasture",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "neha.kasture@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Amit Shewale",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "amit.shewale@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Snehal Bankatrao Shinde",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "snehal.shinde@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Vasundhara Rathod",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "vasundhara.rathod@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Mangesh Kose",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "mangesh.kose@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Swati Hira",
            "Institution": "IIIT Nagpur",
            "Department": "Computer Science and Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "swati.hira@cse.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        # Electronics & Communication Engineering (ECE)
        {
            "Name": "Dr. Paritosh D. Peshwe",
            "Institution": "IIIT Nagpur",
            "Department": "Electronics and Communication Engineering",
            "Designation": "Assistant Professor & Head of Department",
            "Qualification": "Ph.D., VNIT Nagpur",
            "Email": "paritosh.peshwe@ece.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Tapan Kumar Jain",
            "Institution": "IIIT Nagpur",
            "Department": "Electronics and Communication Engineering",
            "Designation": "Assistant Professor (Grade-I)",
            "Qualification": "Ph.D. Wireless Sensor Networks, JUIT Solan; M.Tech., COEP Pune",
            "Email": "tapan.jain@ece.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Pooja Jain",
            "Institution": "IIIT Nagpur",
            "Department": "Electronics and Communication Engineering",
            "Designation": "Assistant Professor (Grade-I)",
            "Qualification": "Ph.D., MNNIT Allahabad",
            "Email": "pooja.jain@ece.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Tausif Diwan",
            "Institution": "IIIT Nagpur",
            "Department": "Electronics and Communication Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D., VNIT Nagpur",
            "Email": "tausif.diwan@ece.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Girish Chandra Ghivela",
            "Institution": "IIIT Nagpur",
            "Department": "Electronics and Communication Engineering",
            "Designation": "Assistant Professor & Ph.D. Coordinator",
            "Qualification": "Ph.D., NIT Rourkela",
            "Email": "girish.ghivela@ece.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Harsh Goud",
            "Institution": "IIIT Nagpur",
            "Department": "Electronics and Communication Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D., MANIT Bhopal",
            "Email": "harsh.goud@ece.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Khuraijam Nelson Singh",
            "Institution": "IIIT Nagpur",
            "Department": "Electronics and Communication Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D., NIT Silchar",
            "Email": "nelson.singh@ece.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Rashmi A. Pandhare",
            "Institution": "IIIT Nagpur",
            "Department": "Electronics and Communication Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D. Microwave & Antennas, Nagpur University",
            "Email": "rashmi.pandhare@ece.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Rashmi Ranjan Kumar",
            "Institution": "IIIT Nagpur",
            "Department": "Electronics and Communication Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "rashmi.kumar@ece.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Nikhil Dhengre",
            "Institution": "IIIT Nagpur",
            "Department": "Electronics and Communication Engineering",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D., VNIT Nagpur",
            "Email": "nikhil.dhengre@ece.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        # Basic Sciences & Engineering (BSE)
        {
            "Name": "Dr. Charu Goel",
            "Institution": "IIIT Nagpur",
            "Department": "Basic Sciences",
            "Designation": "Assistant Professor & Head of Department",
            "Qualification": "Ph.D., University of Konstanz (Germany) / Mathematics",
            "Email": "charu.goel@bs.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Aatish S. Daryapurkar",
            "Institution": "IIIT Nagpur",
            "Department": "Basic Sciences",
            "Designation": "Assistant Professor (Physics)",
            "Qualification": "Ph.D., VNIT Nagpur",
            "Email": "asdaryapurkar@bs.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Anuradha Singh",
            "Institution": "IIIT Nagpur",
            "Department": "Basic Sciences",
            "Designation": "Assistant Professor (Mathematics)",
            "Qualification": "Ph.D., IIT Bombay",
            "Email": "anuradhasingh@bs.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Kirti Sanjay Dorshetwar",
            "Institution": "IIIT Nagpur",
            "Department": "Basic Sciences",
            "Designation": "Assistant Professor (English Literature)",
            "Qualification": "Ph.D., RTM Nagpur University",
            "Email": "kirti.dorshetwar@bs.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Deepmala Baghel",
            "Institution": "IIIT Nagpur",
            "Department": "Basic Sciences",
            "Designation": "Assistant Professor (Social Sciences)",
            "Qualification": "Ph.D., IIT Roorkee",
            "Email": "deepmala.baghel@bs.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Vijender Nallapu",
            "Institution": "IIIT Nagpur",
            "Department": "Basic Sciences",
            "Designation": "Assistant Professor (Mathematics)",
            "Qualification": "Ph.D., IIT Guwahati",
            "Email": "vijender.nallapu@bs.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Kamaljeet",
            "Institution": "IIIT Nagpur",
            "Department": "Basic Sciences",
            "Designation": "Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "kamaljeet@bs.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        },
        {
            "Name": "Dr. Santosh Kumar Sahu",
            "Institution": "IIIT Nagpur",
            "Department": "Basic Sciences",
            "Designation": "Adjunct Assistant Professor",
            "Qualification": "Ph.D.",
            "Email": "santosh.sahu@bs.iiitn.ac.in",
            "Profile URL": "https://iiitn.ac.in/faculty-staff-directory.php"
        }
    ]
    return faculty_list

def main():
    records = get_nagpur_faculty()
    df = pd.DataFrame(records)
    out_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(out_dir, "IIIT_Nagpur_Faculty.xlsx")
    df.to_excel(out_path, index=False)
    print(f"Saved {len(df)} faculty records to {out_path}")

if __name__ == "__main__":
    main()
