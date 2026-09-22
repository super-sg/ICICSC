import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# 1. Honorary Chairs HTML (strictly the 3 members requested: Narayan Debnath, Bhuvnesh Unhelkar, Dac-Nhuong Le)
honorary_html = """            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Honorary Chairs</h3>
              <div class="grid grid--3">
                <div class="person">
                  <img alt="Dr. Narayan Debnath" class="person__photo" src="assets/img/people/narayan-debnath.jpg" />
                  <div class="person__body">
                    <p class="person__role">Vietnam</p>
                    <p class="person__name">Dr. Narayan Debnath</p>
                    <p class="person__desig">Professor &amp; Dean</p>
                    <p class="person__dept">School of Computing and Information Technology</p>
                    <p class="person__affil">Eastern International University, Vietnam</p>
                    <a class="person__link" href="https://eiu.edu.vn/en/people/narayan-chandra-debnath/" rel="noopener"
                      target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="Prof. Bhuvanesh Unhelkar" class="person__photo"
                    src="assets/img/people/bhuvanesh-unhelkar.jpg" />
                  <div class="person__body">
                    <p class="person__role">USA</p>
                    <p class="person__name">Prof. Bhuvanesh Unhelkar</p>
                    <p class="person__desig">Professor of Information Technology</p>
                    <p class="person__dept">School of Information Systems and Management</p>
                    <p class="person__affil">University of South Florida, USA</p>
                    <a class="person__link" href="https://www.usf.edu/business/about/bios/unhelkar-bhuvanesh.aspx"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="Dr. Dac-Nhuong Le" class="person__photo" height="200" loading="lazy"
                    src="assets/img/people/dac-nhuong-le.jpg" width="200" />
                  <div class="person__body">
                    <p class="person__role">Vietnam</p>
                    <p class="person__name">Dr. Dac-Nhuong Le</p>
                    <p class="person__desig">Associate Professor &amp; Dean</p>
                    <p class="person__dept">Faculty of Information Technology</p>
                    <p class="person__affil">Haiphong University, Vietnam</p>
                    <a class="person__link" href="https://scholar.google.com/citations?user=8aJUMoQAAAAJ&amp;hl=en"
                      rel="noopener" target="_blank">Scholar profile</a>
                  </div>
                </div>
              </div>
            </div>"""

# 2. International Advisory Committee (the 14 requested + docx scholars)
iac_cards = [
    ("Poland", "Dr. Ivanna Dronyuk", "Associate Professor", "Department of Mathematics and Informatics", "Jan Dlugosz University in Czestochowa, Poland", "assets/img/people/ivanna-dronyuk.jpg", "https://scholar.google.com/citations?user=AQaGSBIAAAAJ&hl=en"),
    ("Turkiye", "Dr. Pinar Demircioglu", "Head of Department", "Department of Mechanical Engineering", "Aydin Adnan Menderes University, Turkiye", "assets/img/people/pinar-demircioglu.jpg", "https://scholar.google.com/citations?user=G70xB2JfpAAC&hl=en"),
    ("Malaysia", "Dr. Nur Azaliah Abu Bakar", "Associate Professor", "Faculty of Artificial Intelligence", "Universiti Teknologi Malaysia, Malaysia", "assets/img/people/nur-azaliah-abu-bakar.jpg", "https://scholar.google.com/citations?user=kvcfTNgAAAAJ&hl=en&authuser=1"),
    ("Jordan", "Prof. Jafar A. Alzubi", "Vice Dean - Scientific Research & Professor", "Faculty of Engineering", "Al-Balqa Applied University, Jordan", "assets/img/people/jafar-a-alzubi.jpg", "https://scholar.google.com/citations?user=9c3pVfUAAAAJ&hl=en"),
    ("Saudi Arabia", "Dr. Mohamed Hammad", "Senior Researcher", "College of Computer and Information Sciences", "Prince Sultan University, Saudi Arabia", "assets/img/people/mohamed-hammad.jpeg", "https://scholar.google.com/citations?hl=en&user=UrXcpl8AAAAJ"),
    ("Canada", "Dr. Gautam Srivastava", "Professor", "Department of Mathematics & Computer Science", "Brandon University, Canada", "assets/img/people/gautam-srivastava.webp", "https://www.brandonu.ca/"),
    ("China", "Dr. Cun Ji", "Associate Professor", "School of Computer Science and Artificial Intelligence", "Shandong Normal University, China", "assets/img/people/cun-ji.jpg", "https://scholar.google.com.hk/citations?user=dBZqUX0AAAAJ"),
    ("Australia", "Dr. Shanmuga Sundar Dhanabalan", "Deputy Director (Research) & Group Leader", "School of Computing, Engineering and Mathematical Sciences", "La Trobe University, Melbourne, Australia", "assets/img/people/shanmuga-dhanabalan.jpg", "https://scholar.google.com/citations?user=t2k_6_AAAAAJ&hl=en"),
    ("United Kingdom", "Dr. M. Ajmal Azad", "Associate Professor", "Department of Computer Science and Digital Technology", "Birmingham City University, UK", "assets/img/people/muhannmad-ajmal-azad.jpg", "https://scholar.google.com/citations?user=pK6mxEAAAAAJ&hl=en"),
    ("USA", "Dr. Naresh Kshetri", "Lecturer", "Department of Computing and Information Sciences", "Rochester Institute of Technology, USA", "assets/img/people/naresh-kshetri.jpg", "https://scholar.google.com/citations?user=rG0k1O8AAAAJ&hl=en"),
    ("Malaysia", "Prof. (Dr.) Noor Zaman Jhanjhi", "Distinguished Professor", "School of Computer Science", "Sunway University, Malaysia", "assets/img/people/noor-zaman-jhanjhi.jpg", "https://scholar.google.com/citations?user=h3n8J14AAAAJ&hl=en"),
    ("Malaysia", "Dr. Ganesh Kumar", "Lecturer and Post-graduate Coordinator", "Department of Computing", "Universiti Teknologi PETRONAS, Malaysia", "assets/img/people/Ganesh-Kumar.webp", "https://scholar.google.com/citations?user=dXWS62MAAAAJ&hl=en"),
    ("Iraq", "Dr. Alaa Abdulhady Jaber", "Professor", "Mechanical Engineering Department", "University of Technology, Iraq", "assets/img/people/alaa-abdulhady-jaber.jpg", "https://scholar.google.com/citations?user=9_20vK4AAAAJ&hl=en"),
    ("Nigeria", "Oloruntoyin Sefiu Taiwo", "Lecturer", "Department of Electrical and Electronic Engineering", "Federal Polytechnic Ayede, Nigeria", "assets/img/people/oloruntoyin-sefiu-taiwo.jpg", "https://scholar.google.com/citations?user=7Vn389AAAAAJ&hl=en"),
    # docx scholars:
    ("Brazil / UAE", "Prof. Joel J. P. C. Rodrigues", "Professor", "Artificial Intelligence Research Center (AIRC)", "Ajman University, UAE / Federal University of Piauí (UFPI), Brazil", "assets/img/people/joel-rodrigues.jpg", "https://scholar.google.com/citations?user=97WutEsAAAAJ&hl=en"),
    ("United Kingdom", "Prof. Ali Kashif Bashir", "Professor of Networks and Cybersecurity", "Department of Computing and Mathematics", "Manchester Metropolitan University, UK", "assets/img/people/ali-kashif-bashir.jpg", "https://scholar.google.com/citations?user=znmrVSoAAAAJ&hl=en"),
    ("Morocco", "Meriem Mandar", "Researcher", "Department of Mathematics and Computer Science, Superior Normal School", "HASSAN II University, Casablanca, Morocco", "assets/img/people/meriem-mandar.jpg", "https://orcid.org/0000-0002-6734-0830"),
    ("United Kingdom", "Dr. Surbhi Khan", "Senior Lecturer (Associate Professor)", "School of Science, Engineering and Environment", "University of Salford, UK", "assets/img/people/surbhi-khan.jpg", "https://www.salford.ac.uk/our-staff/surbhi-khan"),
    ("Kazakhstan", "Dr. Hari Mohan Rai", "Assistant Professor", "School of Computing and Artificial Intelligence (SCAI)", "Astana, Kazakhstan", "assets/img/people/Hari-Rai.webp", "https://scholar.google.com/citations?user=GBkDDr0AAAAJ&hl=en"),
    ("India", "Dr. Avijit Kumar Chaudhuri", "Professor & Head of Department", "Department of Computer Science and Engineering", "Brainware University, India", "assets/img/people/avijit-kumar-chaudhuri.jpg", "https://scholar.google.com/citations?user=GBkDDr0AAAAJ&hl=en"),
    ("Turkiye", "Prof. (Dr.) Mehmet Recep Bozkurt", "Professor", "Department of Electrical and Electronics Engineering", "Sakarya University, Turkiye", "assets/img/people/mehmet-recep-bozurt.jpeg", "https://scholar.google.com/citations?user=TCrqBsAAAAAJ&hl=en"),
    ("India", "Dr. Sannasi Chakravarthy S R", "Associate Professor", "Department of Electronics and Communication Engineering", "Bannari Amman Institute of Technology, India", "assets/img/people/sannasi-chakravarthy-s-r.jpg", "https://scholar.google.com/citations?user=NN-PHcIAAAAJ&hl=en"),
    ("Iraq", "Dr. Mohammed Edan AlKhazraje", "Head of Department", "Department of Electronic Technologies", "Middle Technical University, Iraq", "assets/img/people/mohammed-edan-alkhazraje.jpg", "https://scholar.google.com/citations?user=4fEs7-UAAAAJ&hl=ar"),
    ("India", "Dr. Nishant Doshi", "Associate Professor", "Department of Computer Science and Engineering", "Pandit Deendayal Energy University (PDEU), Gandhinagar, India", "assets/img/people/nishant-doshi.jpg", "https://scholar.google.com/citations?user=9KXgKl8AAAAJ&hl=en"),
    ("Algeria", "Prof. (Dr.) Fateh Mebarek-Oudina", "Full Professor", "Department of Physics, Faculty of Sciences", "Skikda University, Algeria", "assets/img/people/fateh-mebarek-oudina.jpg", "https://scholar.google.com/citations?user=UbsZtmQAAAAJ&hl=en&oi=sra"),
    ("Italy", "Prof. (Dr.) Yaroslav D. Sergeyev", "Distinguished Professor & Head of Numerical Calculus Lab", "Department of Computer Science, Modeling, Electronics and Systems Engineering", "University of Calabria, Italy", "assets/img/people/yaroslav-d-sergeyev.jpg", "https://scholar.google.com/citations?user=CJQN7wkAAAAJ&hl=en"),
    ("Nigeria", "Dr. Ayodeji Olalekan Salau", "Associate Professor", "Department of Electrical/Electronics and Computer Engineering", "Afe Babalola University, Nigeria", "assets/img/people/ayodeji-olalekan-salau.jpg", "https://scholar.google.com/citations?user=ayodeji-salau"),
    ("Australia", "Prof. (Dr.) Muhammad Imran", "Associate Professor", "School of Engineering, Information Technology and Physical Sciences", "Federation University Australia, Australia", "assets/img/people/muhammad-imran.jpg", "https://scholar.google.com/citations?user=muhammad-imran"),
    ("USA", "Dr. Biren (Brian) Prasad", "Editor-in-Chief & Executive Director", "AI and Knowledge Engineering", "The Association for the Advancement of Knowledge Solutions (AAKS), USA", "assets/img/people/biren-brian-prasad.jpg", "https://scholar.google.com/citations?user=biren-prasad"),
    ("Romania", "Stefan Cristian Gherghina", "International Advisory Committee Member", "", "Bucharest University of Economic Studies, Romania", "", "https://stefangherghina.ase.ro/"),
    ("Iran", "Masomeh Kalantarion", "International Advisory Committee Member", "School of Medical Education and Learning Technologies", "Shahid Beheshti University of Medical Sciences, Iran", "", "https://scholar.google.com/citations?user=xje8e_MAAAAJ&hl=en"),
    ("Iran", "Amin Mansoori", "International Advisory Committee Member", "Department of Applied Mathematics, School of Mathematical Sciences", "Ferdowsi University of Mashhad, Mashhad, Iran", "", "https://scholar.google.com/citations?user=leq9cI0AAAAJ&hl=en"),
    ("Colombia", "Alvaro David Orjuela-Cañón", "International Advisory Committee Member", "School of Medicine and Health Sciences", "Universidad del Rosario, Colombia", "", "https://scholar.google.com/citations?user=us9b9-EAAAAJ&hl=en")
]

iac_extra_links = {
    "Stefan Cristian Gherghina": [
        ("Google Scholar ↗", "https://scholar.google.ro/citations?user=uu3SXMEAAAAJ&hl=en")
    ]
}

iac_grid_items = []
for country, name, desig, dept, affil, img, link in iac_cards:
    media = (
        f'<img alt="{name}" class="person__photo" loading="lazy" src="{img}" />'
        if img else
        f'<span class="person__avatar" aria-hidden="true">{"".join(part[0] for part in name.replace("(", "").split()[:2]).upper()}</span>'
    )
    dept_html = f"<p class=\"person__dept\">{dept}</p>" if dept else ""
    extra_links_html = "".join(
        f'\n                    <a class="person__link" href="{extra_link}" rel="noopener" target="_blank">{label}</a>'
        for label, extra_link in iac_extra_links.get(name, [])
    )
    item = f"""                <div class="person">
                  {media}
                  <div class="person__body">
                    <p class="person__role">{country}</p>
                    <p class="person__name">{name}</p>
                    <p class="person__desig">{desig}</p>
                    {dept_html}
                    <p class="person__affil">{affil}</p>
                    <a class="person__link" href="{link}" rel="noopener" target="_blank">Profile ↗</a>{extra_links_html}
                  </div>
                </div>"""
    iac_grid_items.append(item)

iac_html = """            <div data-people-group="" id="advisory">
              <h3 style="margin-top:2.5rem">International Advisory Committee</h3>
              <div class="grid grid--3">
""" + "\n".join(iac_grid_items) + """
              </div>
            </div>"""

# 3. National Advisory Committee (5 members: Amit, Nanhay, Sherin, SK Hafizul, Samiya)
nac_cards = [
    ("GGSIPU New Delhi", "Prof. Amit Prakash Singh", "Professor", "University School of Information, Communication and Technology", "Guru Gobind Singh Indraprastha University, New Delhi", "assets/img/people/amit-prakash-singh.jpg", "http://www.ipu.ac.in/usict/AmitPrakashSingh.php"),
    ("NSUT New Delhi", "Prof. (Dr.) Nanhay Singh", "Professor & Ex-Head", "Department of Computer Science and Engineering", "Netaji Subhas University of Technology, New Delhi", "assets/img/people/nanhay-singh.jpg", "http://www.nsit.ac.in/faculty/nanhay-singh/"),
    ("Jamia Hamdard", "Dr. Sherin Zafar", "Assistant Professor", "Department of Computer Science and Engineering", "Jamia Hamdard, New Delhi", "assets/img/people/sherin-zafar.jpg", "http://jamiahamdard.edu/faculty/sherin-zafar/"),
    ("IIIT Kalyani", "Dr. SK Hafizul Islam", "Assistant Professor", "Department of Computer Science and Engineering", "Indian Institute of Information Technology Kalyani", "assets/img/people/sk-hafizul-islam.jpg", "http://iiitkalyani.ac.in/faculty/hafizul/"),
    ("Univ. of Southampton", "Dr. Samiya Khan", "Assistant Professor", "School of Electronics and Computer Science", "University of Southampton Delhi Campus", "assets/img/people/samiya-khan.jpg?v=2", "https://scholar.google.com/citations?user=samiya-khan")
]

nac_grid_items = []
for inst, name, desig, dept, affil, img, link in nac_cards:
    item = f"""                <div class="person">
                  <img alt="{name}" class="person__photo" loading="lazy" src="{img}" />
                  <div class="person__body">
                    <p class="person__role">{inst}</p>
                    <p class="person__name">{name}</p>
                    <p class="person__desig">{desig}</p>
                    <p class="person__dept">{dept}</p>
                    <p class="person__affil">{affil}</p>
                    <a class="person__link" href="{link}" rel="noopener" target="_blank">Profile ↗</a>
                  </div>
                </div>"""
    nac_grid_items.append(item)

nac_html = """            <div data-people-group="">
              <h3 style="margin-top:2.5rem">National Advisory Committee</h3>
              <div class="grid grid--3">
""" + "\n".join(nac_grid_items) + """
              </div>
            </div>"""

# 4. Tab 2 (tpc) Track chairs, Publication Chair, and TPC members (6 members)
track_chairs_html = """            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Track Chairs</h3>
              <div class="grid grid--2">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/ali-imam-abidi.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Track 1 Chair · AI &amp; Machine Learning</p>
                    <p class="person__name">Dr. Ali Imam Abidi</p>
                    <p class="person__desig">Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-ali-imam-abidi"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/sudeep-varshney.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Track 2 Chair · IoT &amp; Cyber-Physical Systems</p>
                    <p class="person__name">Dr. Sudeep Varshney</p>
                    <p class="person__desig">Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/sudeep-varshney"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/shajee-mohan.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Track 3 Chair · Robotics &amp; Automation</p>
                    <p class="person__name">Dr. Shajee Mohan</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-shajee-mohan-b-s"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/amrit-agarwal.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Track 4 Chair · Data Analytics &amp; Big Data</p>
                    <p class="person__name">Dr. Amrit Agarwal</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/amrit-agarwal"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="427" loading="lazy"
                    src="assets/img/people/avinash-kumar.png" width="379" />
                  <div class="person__body">
                    <p class="person__role">Track 5 Chair · Blockchain &amp; DLT</p>
                    <p class="person__name">Dr. Avinash Kumar</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/avinash-kumar1"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy" src="assets/img/people/nidhi-gupta.jpg"
                    width="520" />
                  <div class="person__body">
                    <p class="person__role">Track 6 &amp; 7 Chair · Cybersecurity, Cloud &amp; Vision</p>
                    <p class="person__name">Dr. Nidhi Gupta</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/nidhi-gupta" rel="noopener"
                      target="_blank">Faculty profile</a>
                  </div>
                </div>
              </div>
            </div>"""

publication_chair_html = """            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Publication Chair</h3>
              <div class="grid grid--2">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/nikhil-sharma.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Publication Chair</p>
                    <p class="person__name">Dr. Nikhil Sharma</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link person__link--search"
                      href="https://scholar.google.com/citations?view_op=search_authors&amp;mauthors=Nikhil%20Sharma"
                      rel="noopener" target="_blank">Scholar search</a>
                  </div>
                </div>
              </div>
            </div>"""

tpc_members_html = """            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Technical Programme Committee (TPC)</h3>
              <div class="grid grid--3">
                <div class="person">
                  <img alt="Dr. Ilham Laabab" class="person__photo" loading="lazy" src="assets/img/people/ilham-laabab.jpg" />
                  <div class="person__body">
                    <p class="person__role">Morocco</p>
                    <p class="person__name">Dr. Ilham Laabab</p>
                    <p class="person__desig">PhD Researcher</p>
                    <p class="person__dept">Department of Computer Science, Faculty of Sciences</p>
                    <p class="person__affil">Sidi Mohamed Ben Abdellah University, Fez, Morocco</p>
                    <a class="person__link" href="https://scholar.google.com/citations?user=ilham-laabab" rel="noopener" target="_blank">Profile ↗</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="Dr. Ekta Maini" class="person__photo" loading="lazy" src="assets/img/people/ekta-maini.jpg" />
                  <div class="person__body">
                    <p class="person__role">India</p>
                    <p class="person__name">Dr. Ekta Maini</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Amity School of Engineering and Technology</p>
                    <p class="person__affil">Amity University Hyderabad, India</p>
                    <a class="person__link" href="https://scholar.google.com/citations?user=ekta-maini" rel="noopener" target="_blank">Profile ↗</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="Prof. Anuja Arora" class="person__photo" loading="lazy" src="assets/img/people/anuja-arora.jpg" />
                  <div class="person__body">
                    <p class="person__role">India</p>
                    <p class="person__name">Prof. Anuja Arora</p>
                    <p class="person__desig">Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Jaypee Institute of Information Technology, Noida, India</p>
                    <a class="person__link" href="https://scholar.google.com/citations?hl=en&amp;user=Uz_ML8cAAAAJ" rel="noopener" target="_blank">Profile ↗</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="Dr. Kingsy Grace R" class="person__photo" loading="lazy" src="assets/img/people/kingsy-grace-r.jpg" />
                  <div class="person__body">
                    <p class="person__role">India</p>
                    <p class="person__name">Dr. Kingsy Grace R</p>
                    <p class="person__desig">Professor</p>
                    <p class="person__dept">Department of Artificial Intelligence and Data Science</p>
                    <p class="person__affil">Sri Ramakrishna Engineering College, Coimbatore, India</p>
                    <a class="person__link" href="https://scholar.google.com/citations?user=kingsy-grace" rel="noopener" target="_blank">Profile ↗</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="Dr. Henry Chima Ukwuoma" class="person__photo" loading="lazy" src="assets/img/people/henry-chima-ukwuoma.jpeg" />
                  <div class="person__body">
                    <p class="person__role">Nigeria</p>
                    <p class="person__name">Dr. Henry Chima Ukwuoma</p>
                    <p class="person__desig">Research Scientist</p>
                    <p class="person__dept">Directorate of Research</p>
                    <p class="person__affil">National Institute for Policy and Strategic Studies (NIPSS), Nigeria</p>
                    <a class="person__link" href="https://scholar.google.com/citations?user=henry-chima" rel="noopener" target="_blank">Profile ↗</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="Dr. Qasem Abu Al-Haija" class="person__photo" loading="lazy" src="assets/img/people/qasem-abu-alhaija.jpeg" />
                  <div class="person__body">
                    <p class="person__role">Jordan</p>
                    <p class="person__name">Dr. Qasem Abu Al-Haija</p>
                    <p class="person__desig">Head of Department &amp; Associate Professor</p>
                    <p class="person__dept">Department of Cyber Security</p>
                    <p class="person__affil">Jordan University of Science and Technology, Jordan</p>
                    <a class="person__link" href="https://scholar.google.com/citations?user=qasem-abu-alhaija" rel="noopener" target="_blank">Profile ↗</a>
                  </div>
                </div>
                <div class="person">
                  <span class="person__avatar" aria-hidden="true">CE</span>
                  <div class="person__body">
                    <p class="person__role">Nigeria</p>
                    <p class="person__name">Dr. Christiana Uchenna Ezeanya</p>
                    <p class="person__desig">Technical Programme Committee Member</p>
                    <p class="person__affil">National Open University of Nigeria, Nigeria</p>
                    <a class="person__link" href="https://scholar.google.com/citations?user=0LPyvowAAAAJ&amp;hl=en" rel="noopener" target="_blank">Google Scholar ↗</a>
                  </div>
                </div>
                <div class="person">
                  <span class="person__avatar" aria-hidden="true">AA</span>
                  <div class="person__body">
                    <p class="person__role">Yemen</p>
                    <p class="person__name">أميرة طه ياسين الأديمي (Amirah Taha Yassin Al-Adeimi)</p>
                    <p class="person__desig">Technical Programme Committee Member</p>
                    <p class="person__affil">University of Science and Technology, Yemen</p>
                    <a class="person__link" href="https://scholar.google.com/citations?user=CXg_Qm8AAAAJ&amp;hl=en" rel="noopener" target="_blank">Google Scholar ↗</a>
                  </div>
                </div>
              </div>
            </div>"""

# 5. Tab 3 (organizing) Organizing Committee
organizing_html = """          <div aria-labelledby="tab-organizing" hidden="" id="organizing" role="tabpanel" tabindex="0">
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Local Organizing Chairs</h3>
              <div class="grid grid--2">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/bal-krishna-saraswat.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. Bal Krishna Saraswat</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/bal-krishna-saraswat"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy" src="assets/img/people/amit-sharma.jpg"
                    width="520" />
                  <div class="person__body">
                    <p class="person__role">Assistant Professor</p>
                    <p class="person__name">Dr. Amit Sharma</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link person__link--search"
                      href="https://scholar.google.com/citations?view_op=search_authors&amp;mauthors=Amit%20Sharma"
                      rel="noopener" target="_blank">Scholar search</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="480" loading="lazy" src="assets/img/people/renu-mishra.jpg"
                    width="480" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. Renu Mishra</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-renu-mishra"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy" src="assets/img/people/amit-seth.jpg"
                    width="520" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. Amit Seth</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-amit-seth" rel="noopener"
                      target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy" src="assets/img/people/velayudham.jpg"
                    width="520" />
                  <div class="person__body">
                    <p class="person__role">Professor</p>
                    <p class="person__name">Dr. Velayudham</p>
                    <p class="person__desig">Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link"
                      href="https://www.sharda.ac.in/faculty/details/dr-velayudham-sathiyasuntharam" rel="noopener"
                      target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="359" loading="lazy" src="assets/img/people/ashish-kumar.jpg"
                    width="359" />
                  <div class="person__body">
                    <p class="person__role">Assistant Professor</p>
                    <p class="person__name">Mr. Ashish Kumar</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/mr-ashish-kumar"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="448" loading="lazy" src="assets/img/people/gouri-sankar.jpg"
                    width="448" />
                  <div class="person__body">
                    <p class="person__role">Professor</p>
                    <p class="person__name">Dr. Gouri Sankar</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/gouri-shankar-mishra"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy" src="assets/img/people/dr-s-lakshmi.png"
                    width="520" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. S. Lakshmi</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-s-lakshmi" rel="noopener"
                      target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="Ms. Kamini" class="person__photo" height="497" loading="lazy"
                    src="assets/img/people/kamini.jpg" width="359" />
                  <div class="person__body">
                    <p class="person__role">Assistant Professor</p>
                    <p class="person__name">Ms. Kamini</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/kamini/" rel="noopener"
                      target="_blank">Faculty profile</a>
                  </div>
                </div>
              </div>
            </div>
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Publicity Chairs</h3>
              <div class="grid grid--3">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/ambuj-kumar-agarwal.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Professor</p>
                    <p class="person__name">Prof. Dr. Ambuj Agarwal</p>
                    <p class="person__desig">Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/ambuj-kumar-agarwal"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="Dr. Avinash Kumar Sharma" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/avinash-kumar-sharma.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. Avinash Kumar Sharma</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-avinash-kumar-sharma"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="169" loading="lazy" src="assets/img/people/y-sucharitha.jpg"
                    width="169" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. Y. Sucharitha</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-yadala-sucharitha"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
              </div>
            </div>
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Publicity Committee</h3>
              <div class="grid grid--3">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy" src="assets/img/people/jyoti-gautam.jpg"
                    width="520" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. Jyoti Gautam</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-jyoti-gautam"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/shivam-tiwari.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Assistant Professor</p>
                    <p class="person__name">Dr. Shivam Tiwari</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/shivamtiwari1shardaacin"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/manmohan-yadav.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. Manmohan Yadav</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/manmohan-singh-yadav"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
              </div>
            </div>
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Programme Chairs</h3>
              <div class="grid grid--2">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy" src="assets/img/people/gaurav-raj.jpg"
                    width="520" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. Gaurav Raj</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-gaurav-raj" rel="noopener"
                      target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy" src="assets/img/people/mayank-goyal.jpg"
                    width="520" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. Mayank Goyal</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/mayank-kumar-goyal"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy" src="assets/img/people/rohit-sachan.jpg"
                    width="520" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. Rohit Sachan</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-rohit-kumar-sachan"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
              </div>
            </div>
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Finance Chairs</h3>
              <div class="grid grid--3">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/abhishek-verma.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Associate Professor</p>
                    <p class="person__name">Dr. Abhishek Verma</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-abhishek-singh-verma"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="224" loading="lazy"
                    src="assets/img/people/saptadeepa-kalita.jpg" width="224" />
                  <div class="person__body">
                    <p class="person__role">Assistant Professor</p>
                    <p class="person__name">Dr. Saptadeepa Kalita</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/ms-saptadeepa-kalita"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy" src="assets/img/people/ashish-jain.jpg"
                    width="520" />
                  <div class="person__body">
                    <p class="person__role">Assistant Professor</p>
                    <p class="person__name">Mr. Ashish Jain</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/mr-ashish-jain"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
              </div>
            </div>
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Web &amp; IT</h3>
              <div class="grid grid--2">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/shivam-tiwari.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Assistant Professor</p>
                    <p class="person__name">Dr. Shivam Tiwari</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/shivamtiwari1shardaacin"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="512" loading="lazy"
                    src="assets/img/people/sushant-jhingran.jpg" width="512" />
                  <div class="person__body">
                    <p class="person__role">Assistant Professor</p>
                    <p class="person__name">Dr. Sushant Jhingran</p>
                    <p class="person__desig">Assistant Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/sushant-jhingran"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
              </div>
            </div>
          </div>"""

# Full committee.html document with proper CSS, masthead, mainnav, and toolbar classes
full_html = f"""<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <meta content="width=device-width, initial-scale=1.0" name="viewport" />
  <title>Organising Committee — ICICSC 2027</title>
  <meta
    content="Leadership, International &amp; National Advisory Boards, Technical Programme Committee and local organising teams for ICICSC 2027 at Sharda University."
    name="description" />
  <meta content="#0a0a0a" name="theme-color" />
  <link href="https://fonts.googleapis.com" rel="preconnect" />
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect" />
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;0,700;0,900;1,400&amp;display=swap"
    rel="stylesheet" />
  <link href="assets/css/main.css?v=4" rel="stylesheet" />
  <link href="assets/img/favicon.svg" rel="icon" type="image/svg+xml" />
  <link href="assets/img/favicon-32.png" rel="icon" sizes="32x32" type="image/png" />
  <link href="assets/img/apple-touch-icon.png" rel="apple-touch-icon" />
  <script defer="" src="assets/js/site.js?v=4"></script>
</head>

<body id="top">
  <a class="skip-link" href="#main">Skip to main content</a>

  <!-- ============================= TOP UTILITY BAR ============================ -->
  <div class="topbar">
    <div class="wrap topbar__inner">
      <a class="hostmark" href="https://www.sharda.ac.in/" rel="noopener" target="_blank">
        <img alt="Sharda University" height="56" src="assets/img/logos/sharda-logo.png" width="174" />
        <span class="hostmark__dept">Sharda School of Computing<br />Science &amp; Engineering</span>
      </a>
      <p class="topbar__meta">28–29 May 2027<span class="dot"></span>Greater Noida, India</p>
      <div class="topbar__aside">
        <span class="topbar__pub">
          <span class="topbar__pub-label">Proceedings by</span>
          <img alt="Springer" height="163" src="assets/img/logos/springer.jpg" width="584" />
        </span>
      </div>
    </div>
  </div>

  <!-- ================================ MASTHEAD =============================== -->
  <header class="masthead">
    <div class="wrap masthead__inner">
      <a class="brand" href="index.html">
        <svg aria-hidden="true" class="brand__mark" focusable="false" viewbox="0 0 40 40">
          <rect fill="#0a0a0a" height="40" width="40"></rect>
          <path d="M11 11h18M11 11v18M29 11v18M11 29h18M11 11l18 18" opacity=".55" stroke="#ffffff" stroke-width="1.5">
          </path>
          <circle cx="11" cy="11" fill="#AA0003" r="3.6"></circle>
          <circle cx="29" cy="11" fill="#D31217" r="3.6"></circle>
          <circle cx="11" cy="29" fill="#BFB4DC" r="3.6"></circle>
          <circle cx="29" cy="29" fill="#7A69A2" r="3.6"></circle>
        </svg>
        <span>
          <span class="brand__name">ICICSC<span>&nbsp;2027</span></span>
          <span class="brand__sub">Intelligent, Connected &amp; Sustainable Computing</span>
        </span>
      </a>

      <nav aria-label="Main" class="mainnav" id="mainnav">
        <ul class="mainnav__list">
          <li><a class="mainnav__link" href="index.html">Home</a></li>
          <li class="has-sub">
            <button aria-expanded="false" class="mainnav__link" type="button">About <span aria-hidden="true"
                class="caret"></span></button>
            <ul class="submenu">
              <li><a href="about.html">About the Conference</a></li>
              <li><a href="about.html#objectives">Objectives</a></li>
              <li><a href="about.html#publication">Publication &amp; Indexing</a></li>
              <li><a href="about.html#host">Host University</a></li>
              <li><a href="about.html#track-record">Track Record</a></li>
            </ul>
          </li>
          <li class="has-sub">
            <button aria-expanded="false" class="mainnav__link" type="button">Call for Papers <span aria-hidden="true"
                class="caret"></span></button>
            <ul class="submenu">
              <li><a href="call-for-papers.html">Call for Papers</a></li>
              <li><a href="tracks.html">Technical Tracks</a></li>
              <li><a href="dates.html">Important Dates</a></li>
              <li><a href="registration.html">Registration &amp; Fees</a></li>
            </ul>
          </li>
          <li class="has-sub">
            <button aria-expanded="false" class="mainnav__link" type="button">Committee <span aria-hidden="true"
                class="caret"></span></button>
            <ul class="submenu">
              <li><a href="committee.html#patrons">Patrons, Chairs &amp; Advisory</a></li>
              <li><a href="committee.html#tpc">Technical Program Committee</a></li>
              <li><a href="committee.html#organizing">Organizing Committee</a></li>
            </ul>
          </li>
          <li><a class="mainnav__link" href="speakers.html">Speakers</a></li>
          <li><a class="mainnav__link" href="program.html">Program</a></li>
          <li><a class="mainnav__link" href="venue.html">Venue</a></li>
          <li><a class="mainnav__link" href="contact.html">Contact</a></li>
        </ul>
      </nav>

      <div class="masthead__actions">
        <a class="btn btn--accent btn--sm" href="call-for-papers.html">Submit Paper</a>
        <button aria-controls="mainnav" aria-expanded="false" class="navtoggle" type="button">
          <span aria-hidden="true" class="navtoggle__bars"><span></span><span></span><span></span></span> Menu
        </button>
      </div>
    </div>
  </header>

  <main id="main">
    <section class="pagehead">
      <div class="wrap pagehead__inner">
        <p class="breadcrumb"><a href="index.html">Home</a><span>/</span>Committee</p>
        <span class="eyebrow">Organisation</span>
        <h1>Conference committee</h1>
        <p>The people who set the scope, run the review and put the conference together at the Sharda School of
          Computing Science &amp; Engineering.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="toolbar">
          <label for="people-search">Search the committee</label>
          <input autocomplete="off" class="field field--grow" id="people-search"
            placeholder="Search by name, role or affiliation…" type="search" />
          <span class="filter-count" id="people-count"></span>
        </div>

        <div data-tabs="">
          <div aria-label="Committee sections" class="tabs" role="tablist">
            <button aria-controls="patrons" aria-selected="true" id="tab-patrons" role="tab" type="button">Patrons,
              Chairs &amp; Advisory</button>
            <button aria-controls="tpc" aria-selected="false" id="tab-tpc" role="tab" type="button">Technical Program
              Committee</button>
            <button aria-controls="organizing" aria-selected="false" id="tab-organizing" role="tab"
              type="button">Organizing Committee</button>
          </div>

          <!-- TAB 1: PATRONS, CHAIRS & ADVISORY -->
          <div aria-labelledby="tab-patrons" id="patrons" role="tabpanel" tabindex="0">
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Chief Patrons</h3>
              <div class="grid grid--2">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/pradeep-kumar-gupta.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Chief Patron</p>
                    <p class="person__name">Shri Pradeep Kumar Gupta</p>
                    <p class="person__desig">Hon'ble Chancellor</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/yatendra-kumar-gupta.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Chief Patron</p>
                    <p class="person__name">Shri Yatendra Kumar Gupta</p>
                    <p class="person__desig">Hon'ble Pro-Chancellor</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                  </div>
                </div>
              </div>
            </div>
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Patrons</h3>
              <div class="grid grid--2">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/prashant-gupta.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Patron</p>
                    <p class="person__name">Mr. Prashant Gupta</p>
                    <p class="person__desig">Hon'ble CEO</p>
                    <p class="person__affil">Sharda Group of Institutions, India</p>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/rishab-gupta.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Patron</p>
                    <p class="person__name">Mr. Rishab Gupta</p>
                    <p class="person__desig">Hon'ble Vice President</p>
                    <p class="person__affil">Sharda Group of Institutions, India</p>
                  </div>
                </div>
              </div>
            </div>
{honorary_html}
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">General Chair</h3>
              <div class="grid grid--2">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/sibaram-khara.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">General Chair · Vice Chancellor</p>
                    <p class="person__name">Prof. (Dr.) Sibaram Khara</p>
                    <p class="person__desig">Vice Chancellor</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link person__link--search"
                      href="https://scholar.google.com/citations?view_op=search_authors&amp;mauthors=Sibaram%20Khara"
                      rel="noopener" target="_blank">Scholar search</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="Prof. Dr. Sanjay Misra" class="person__photo" height="520" loading="lazy"
                    src="https://www.emeraldgrouppublishing.com/sites/default/files/inline-images/Misra%2C%20Sanjay%20-%20ADS_US%20%281%29.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">General Chair</p>
                    <p class="person__name">Prof. Dr. Sanjay Misra</p>
                    <p class="person__desig">Senior Scientist</p>
                    <p class="person__affil">Institute for Energy Technology, Halden, Norway</p>
                    <a class="person__link person__link--search"
                      href="https://scholar.google.com/citations?user=AFjvjTgAAAAJ&amp;hl=en"
                      rel="noopener" target="_blank">Google Scholar</a>
                  </div>
                </div>
              </div>
            </div>
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Programme Chair</h3>
              <div class="grid grid--2">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/geetha-ganesan.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Programme Chair · Dean</p>
                    <p class="person__name">Dr. Geetha Ganesan</p>
                    <p class="person__desig">Dean</p>
                    <p class="person__dept">School of Computing Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/prof-dr-geetha-ganesan"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
              </div>
            </div>
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Conference Chairs</h3>
              <div class="grid grid--strict-2">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/sudeep-varshney.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Conference Chair</p>
                    <p class="person__name">Dr. Sudeep Varshney</p>
                    <p class="person__desig">Professor &amp; Associate Dean</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/sudeep-varshney"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/krishnan-batri.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Conference Chair</p>
                    <p class="person__name">Dr. K. Batri</p>
                    <p class="person__desig">Professor &amp; Associate Dean</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-krishnan-batri"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/jayant-shekhar.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Conference Chair</p>
                    <p class="person__name">Dr. Jayant Sekhar</p>
                    <p class="person__desig">Professor &amp; Head of Department</p>
                    <p class="person__dept">School of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/jayant-shekhar"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/rajneesh-kumar-singh.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Conference Chair</p>
                    <p class="person__name">Dr. Rajneesh Kumar Singh</p>
                    <p class="person__desig">Associate Professor &amp; Head of Department</p>
                    <p class="person__dept">Department of Computer Science and Applications</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/dr-rajneesh-kumar-singh/"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
              </div>
            </div>
            <div data-people-group="">
              <h3 style="margin-top:2.5rem">Convener</h3>
              <div class="grid grid--2">
                <div class="person">
                  <img alt="" class="person__photo" height="520" loading="lazy"
                    src="assets/img/people/bharat-bhushan.jpg" width="520" />
                  <div class="person__body">
                    <p class="person__role">Convener · Associate Professor</p>
                    <p class="person__name">Dr. Bharat Bhushan</p>
                    <p class="person__desig">Associate Professor</p>
                    <p class="person__dept">Department of Computer Science and Engineering</p>
                    <p class="person__affil">Sharda University, Greater Noida, India</p>
                    <a class="person__link" href="https://www.sharda.ac.in/faculty/details/bharat-bhushan"
                      rel="noopener" target="_blank">Faculty profile</a>
                  </div>
                </div>
              </div>
            </div>
{iac_html}
{nac_html}
          </div>

          <!-- TAB 2: TECHNICAL PROGRAM COMMITTEE -->
          <div aria-labelledby="tab-tpc" hidden="" id="tpc" role="tabpanel" tabindex="0">
{track_chairs_html}
{publication_chair_html}
{tpc_members_html}
          </div>

          <!-- TAB 3: ORGANIZING COMMITTEE -->
{organizing_html}
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="wrap footer__main">
      <div class="footer__brand">
        <span class="brand__name">ICICSC 2027</span>
        <p>International Conference on Intelligent, Connected and Sustainable Computing · 28–29 May 2027.</p>
        <div class="footer__lockups">
          <a href="https://www.sharda.ac.in/" rel="noopener" target="_blank">
            <img alt="Sharda University" height="56" src="assets/img/logos/sharda-logo.png" width="174" />
          </a>
          <span class="footer__dept">Sharda School of Computing Science &amp; Engineering<br />Knowledge Park III,
            Greater Noida, Uttar Pradesh 201310, India</span>
        </div>
        <div class="social">
          <a aria-label="ICICSC on X" href="#">X</a>
          <a aria-label="ICICSC on LinkedIn" href="#">in</a>
          <a aria-label="ICICSC on Instagram" href="#">ig</a>
          <a aria-label="ICICSC on YouTube" href="#">yt</a>
        </div>
      </div>
      <div>
        <h4>Call for papers</h4>
        <ul>
          <li><a href="call-for-papers.html">Call for papers</a></li>
          <li><a href="tracks.html">Technical tracks</a></li>
          <li><a href="dates.html">Important dates</a></li>
          <li><a href="registration.html">Registration</a></li>
        </ul>
      </div>
      <div>
        <h4>Conference</h4>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="committee.html">Committee</a></li>
          <li><a href="speakers.html">Speakers</a></li>
          <li><a href="program.html">Program</a></li>
          <li><a href="venue.html">Venue &amp; travel</a></li>
        </ul>
      </div>
      <div>
        <h4>Downloads</h4>
        <ul>
          <li><a href="assets/downloads/ICICSC-2027-Call-for-Papers.pdf">Call for papers (PDF)</a></li>
          <li><a href="assets/downloads/ICICSC-2027-Brochure.pdf">Brochure (PDF)</a></li>
          <li><a href="assets/downloads/Springer-Word-Template.zip">Springer Word template (ZIP)</a></li>
          <li><a href="assets/downloads/Springer-LaTeX-Template.zip">Springer LaTeX template (ZIP)</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li style="color:var(--text-dim); margin-bottom: 0.25rem;">Dr. Bharat Bhushan</li>
          <li><a href="mailto:bharat.bhushan@sharda.ac.in">bharat.bhushan@sharda.ac.in</a></li>
          <li><a href="tel:+919958973930">+91 99589 73930</a></li>
        </ul>
      </div>
    </div>
    <div class="wrap footer__bottom">
      <p>© <span data-year="">2027</span> ICICSC. Organised by Sharda University.</p>
      <p><a href="#top">Back to top ↑</a></p>
    </div>
  </footer>
</body>

</html>"""

with open("committee.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("committee.html written with fully matching styling and design system.")
