import streamlit as st
from datetime import datetime
import re

# ============================================================
# JOBHUNT PRO — STREAMLIT MVP
# ============================================================

st.set_page_config(
    page_title="JobHunt Pro",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Demo data
# -----------------------------
if "jobs" not in st.session_state:
    st.session_state.jobs = [
        {
            "id": 1, "title": "Junior Python Developer", "company": "TechNova Solutions",
            "location": "Islamabad, Pakistan", "mode": "Hybrid", "type": "Full-time",
            "experience": "Entry Level", "salary": "PKR 80,000 – 120,000/month",
            "posted": "2 days ago", "category": "Software Development",
            "skills": ["Python", "Django", "REST API", "Git"],
            "description": "Join our engineering team and build reliable web applications for modern businesses.",
            "responsibilities": ["Develop and maintain Python applications.", "Build and consume REST APIs.", "Work with Git and code reviews."],
            "requirements": ["Basic Python knowledge.", "Understanding of APIs and Git.", "Good problem-solving skills."],
        },
        {
            "id": 2, "title": "Frontend Developer", "company": "PixelCraft Labs",
            "location": "Lahore, Pakistan", "mode": "Remote", "type": "Full-time",
            "experience": "Junior", "salary": "PKR 90,000 – 150,000/month",
            "posted": "1 day ago", "category": "Software Development",
            "skills": ["HTML", "CSS", "JavaScript", "React"],
            "description": "Create fast, accessible and beautiful interfaces for web products.",
            "responsibilities": ["Build responsive interfaces.", "Convert designs into reusable components.", "Optimize frontend performance."],
            "requirements": ["HTML, CSS and JavaScript.", "Basic React knowledge.", "Attention to UI details."],
        },
        {
            "id": 3, "title": "UI/UX Designer", "company": "CreativeHub",
            "location": "Karachi, Pakistan", "mode": "On-site", "type": "Full-time",
            "experience": "Junior", "salary": "PKR 70,000 – 110,000/month",
            "posted": "3 days ago", "category": "Design",
            "skills": ["Figma", "UI Design", "UX Research", "Prototyping"],
            "description": "Help us design intuitive digital products used by thousands of people.",
            "responsibilities": ["Create wireframes and prototypes.", "Design mobile and web experiences.", "Collaborate with developers."],
            "requirements": ["Strong Figma skills.", "Portfolio of UI/UX work.", "Understanding of user-centered design."],
        },
        {
            "id": 4, "title": "Data Analyst", "company": "DataCore Pakistan", 
            "location": "Rawalpindi, Pakistan", "mode": "Hybrid", "type": "Full-time",
            "experience": "Mid Level", "salary": "PKR 120,000 – 180,000/month",
            "posted": "5 days ago", "category": "Data",
            "skills": ["Excel", "SQL", "Power BI", "Python"],
            "description": "Turn business data into practical insights and decision-making dashboards.",
            "responsibilities": ["Analyze business datasets.", "Create dashboards and reports.", "Present insights to stakeholders."],
            "requirements": ["SQL knowledge.", "Experience with Excel or Power BI.", "Strong analytical thinking."],
        },
        {
            "id": 5, "title": "AI / Machine Learning Intern", "company": "FutureMind AI",
            "location": "Quetta, Pakistan", "mode": "Remote", "type": "Internship",
            "experience": "Internship", "salary": "PKR 30,000 – 50,000/month",
            "posted": "4 days ago", "category": "AI & ML",
            "skills": ["Python", "Machine Learning", "Pandas", "AI"],
            "description": "A practical internship for students interested in AI and machine learning.",
            "responsibilities": ["Prepare datasets.", "Experiment with ML models.", "Document experiments and results."],
            "requirements": ["Python basics.", "Interest in AI/ML.", "Currently studying CS, IT or a related field."],
        },
        {
            "id": 6, "title": "Digital Marketing Executive", "company": "GrowthWave",
            "location": "Multan, Pakistan", "mode": "On-site", "type": "Full-time",
            "experience": "Junior", "salary": "PKR 60,000 – 100,000/month",
            "posted": "6 days ago", "category": "Marketing",
            "skills": ["SEO", "Social Media", "Content", "Analytics"],
            "description": "Help brands grow through creative digital marketing campaigns.",
            "responsibilities": ["Plan social campaigns.", "Track marketing performance.", "Assist with SEO and content."],
            "requirements": ["Basic digital marketing knowledge.", "Good communication skills.", "Creative mindset."],
        },
        {
            "id": 7, "title": "Cybersecurity Analyst", "company": "SecureNet Technologies",
            "location": "Islamabad, Pakistan", "mode": "Hybrid", "type": "Full-time",
            "experience": "Mid Level", "salary": "PKR 150,000 – 250,000/month",
            "posted": "7 days ago", "category": "Cybersecurity",
            "skills": ["SIEM", "Networking", "Linux", "Security"],
            "description": "Monitor security events and help protect business systems from threats.",
            "responsibilities": ["Monitor security alerts.", "Investigate suspicious activity.", "Maintain security documentation."],
            "requirements": ["Networking fundamentals.", "Linux knowledge.", "Security monitoring experience."],
        },
        {
            "id": 8, "title": "Graphic Designer", "company": "BrandStudio",
            "location": "Peshawar, Pakistan", "mode": "Remote", "type": "Part-time",
            "experience": "Junior", "salary": "PKR 45,000 – 80,000/month",
            "posted": "8 days ago", "category": "Design",
            "skills": ["Photoshop", "Illustrator", "Canva", "Branding"],
            "description": "Design social media, marketing and brand assets for growing businesses.",
            "responsibilities": ["Create visual assets.", "Maintain brand consistency.", "Collaborate with marketing."],
            "requirements": ["Strong visual sense.", "Portfolio required.", "Knowledge of design tools."],
        },
    ]

if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = set()
if "applications" not in st.session_state:
    st.session_state.applications = []
if "posted_jobs" not in st.session_state:
    st.session_state.posted_jobs = []
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "selected_job" not in st.session_state:
    st.session_state.selected_job = None
if "role" not in st.session_state:
    st.session_state.role = "Job Seeker"
if "profile_complete" not in st.session_state:
    st.session_state.profile_complete = 65

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f7f8fc;
}

.block-container {
    max-width: 1180px;
    padding: 1.2rem 1rem 4rem;
}

header[data-testid="stHeader"] {
    background: rgba(247,248,252,.92);
}

.hero {
    background: linear-gradient(135deg, #173b8f 0%, #315bd6 55%, #5b76e8 100%);
    border-radius: 24px;
    padding: 42px 34px;
    color: white;
    margin: 8px 0 24px;
    box-shadow: 0 14px 35px rgba(31,66,150,.16);
}

.hero h1 {
    font-size: clamp(2rem, 5vw, 3.25rem);
    line-height: 1.05;
    margin: 0 0 12px;
    font-weight: 800;
}

.hero p {
    font-size: 1rem;
    max-width: 650px;
    opacity: .92;
}

.section-title {
    font-size: 1.45rem;
    font-weight: 800;
    margin: 28px 0 14px;
    color: #172033;
}

.job-card {
    background: white;
    border: 1px solid #e7eaf1;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 13px;
    box-shadow: 0 4px 16px rgba(20,30,55,.04);
}

.job-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: #172033;
}

.company {
    color: #536174;
    font-weight: 600;
    margin-top: 3px;
}

.meta {
    color: #657286;
    font-size: .9rem;
    margin-top: 8px;
}

.tag {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 999px;
    background: #eef3ff;
    color: #2852b8;
    font-size: .75rem;
    font-weight: 700;
    margin: 5px 4px 0 0;
}

.salary {
    color: #176b46;
    font-weight: 800;
    margin-top: 8px;
}

.stat-card {
    background: white;
    border: 1px solid #e7eaf1;
    border-radius: 17px;
    padding: 20px;
    min-height: 105px;
}

.stat-number {
    font-size: 1.7rem;
    font-weight: 800;
    color: #172033;
}

.stat-label {
    color: #6a7485;
    font-size: .86rem;
}

.company-logo {
    width: 48px;
    height: 48px;
    border-radius: 13px;
    background: #eef3ff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 800;
    color: #315bd6;
}

.detail-box {
    background: white;
    border: 1px solid #e7eaf1;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 16px;
}

.notice {
    background: #eef5ff;
    border: 1px solid #d9e6ff;
    color: #294b8e;
    border-radius: 14px;
    padding: 14px 16px;
}

.footer {
    text-align: center;
    color: #8992a1;
    padding: 35px 0 10px;
    font-size: .85rem;
}

div.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
}

@media (max-width: 700px) {
    .block-container {
        padding: .7rem .7rem 3rem;
    }
    .hero {
        padding: 28px 20px;
        border-radius: 18px;
    }
    .hero h1 {
        font-size: 2rem;
    }
    .job-card, .detail-box {
        padding: 16px;
        border-radius: 15px;
    }
    .section-title {
        font-size: 1.25rem;
    }
    .stat-card {
        min-height: 90px;
        padding: 15px;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Helpers
# -----------------------------
def go(page):
    st.session_state.page = page
    st.session_state.selected_job = None
    st.rerun()

def get_job(job_id):
    for job in st.session_state.jobs + st.session_state.posted_jobs:
        if job["id"] == job_id:
            return job
    return None

def logo_letter(company):
    return company.strip()[0].upper() if company else "J"

def job_card(job):
    saved = job["id"] in st.session_state.saved_jobs
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown(
            f'<div class="job-card">'
            f'<div class="job-title">{job["title"]}</div>'
            f'<div class="company">{job["company"]}</div>'
            f'<div class="meta">📍 {job["location"]} &nbsp; • &nbsp; {job["mode"]} &nbsp; • &nbsp; {job["type"]}</div>'
            f'<div class="salary">{job["salary"]}</div>'
            f'<div class="meta">Experience: {job["experience"]} &nbsp; • &nbsp; {job["posted"]}</div>'
            + "".join([f'<span class="tag">{x}</span>' for x in job["skills"]])
            + '</div>',
            unsafe_allow_html=True
        )
    with c2:
        if st.button("★" if saved else "☆", key=f"save_{job['id']}", help="Save job"):
            if saved:
                st.session_state.saved_jobs.remove(job["id"])
            else:
                st.session_state.saved_jobs.add(job["id"])
            st.rerun()
        if st.button("View", key=f"view_{job['id']}"):
            st.session_state.selected_job = job["id"]
            st.session_state.page = "Job Details"
            st.rerun()

def render_nav():
    st.markdown(
        '<div style="display:flex;align-items:center;justify-content:space-between;'
        'padding:8px 0 18px;">'
        '<div style="font-size:1.35rem;font-weight:800;color:#173b8f;">💼 JobHunt <span style="color:#315bd6;">Pro</span></div>'
        '<div style="color:#687385;font-size:.85rem;">Find your next opportunity.</div>'
        '</div>',
        unsafe_allow_html=True
    )
    nav = st.columns(6)
    pages = ["Home", "Find Jobs", "Saved Jobs", "Dashboard", "Post a Job", "Profile"]
    for col, page in zip(nav, pages):
        with col:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                go(page)

# -----------------------------
# Header
# -----------------------------
render_nav()

# -----------------------------
# Home
# -----------------------------
if st.session_state.page == "Home":
    st.markdown("""
    <div class="hero">
        <h1>Find work that moves you forward.</h1>
        <p>Search jobs, discover great companies, and take the next step in your career — all in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔎 Search jobs")
    a, b, c = st.columns([2.2, 1.5, 1.2])
    with a:
        keyword = st.text_input("Job title or keyword", placeholder="e.g. Python Developer")
    with b:
        location = st.text_input("Location", placeholder="e.g. Islamabad")
    with c:
        mode = st.selectbox("Work type", ["Any", "Remote", "Hybrid", "On-site"])

    if st.button("Search Jobs", type="primary", use_container_width=True):
        st.session_state.search_keyword = keyword
        st.session_state.search_location = location
        st.session_state.search_mode = mode
        st.session_state.page = "Find Jobs"
        st.rerun()

    st.markdown('<div class="section-title">Popular searches</div>', unsafe_allow_html=True)
    popular = ["Python Developer", "Frontend Developer", "UI/UX Designer", "Data Analyst", "AI Engineer", "Cybersecurity"]
    cols = st.columns(3)
    for i, item in enumerate(popular):
        with cols[i % 3]:
            if st.button(item, key=f"popular_{i}", use_container_width=True):
                st.session_state.search_keyword = item
                st.session_state.search_location = ""
                st.session_state.search_mode = "Any"
                st.session_state.page = "Find Jobs"
                st.rerun()

    st.markdown('<div class="section-title">Why JobHunt Pro?</div>', unsafe_allow_html=True)
    s = st.columns(4)
    stats = [("50K+", "Jobs"), ("10K+", "Companies"), ("100K+", "Job Seekers"), ("5K+", "New jobs this month")]
    for col, (num, label) in zip(s, stats):
        with col:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Featured jobs</div>', unsafe_allow_html=True)
    for job in st.session_state.jobs[:4]:
        job_card(job)

# -----------------------------
# Find Jobs
# -----------------------------
elif st.session_state.page == "Find Jobs":
    st.markdown("## Find jobs")
    defaults = {
        "search_keyword": "", "search_location": "", "search_mode": "Any",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    q1, q2, q3 = st.columns([2, 1.4, 1])
    with q1:
        keyword = st.text_input("Keyword", value=st.session_state.search_keyword, placeholder="Job title, skill or company")
    with q2:
        location = st.text_input("Location", value=st.session_state.search_location, placeholder="City or remote")
    with q3:
        mode = st.selectbox("Work type", ["Any", "Remote", "Hybrid", "On-site"],
                            index=["Any", "Remote", "Hybrid", "On-site"].index(st.session_state.search_mode)
                            if st.session_state.search_mode in ["Any", "Remote", "Hybrid", "On-site"] else 0)

    f1, f2, f3 = st.columns(3)
    with f1:
        category = st.selectbox("Category", ["All", "Software Development", "Design", "Data", "AI & ML", "Marketing", "Cybersecurity"])
    with f2:
        experience = st.selectbox("Experience", ["All", "Internship", "Entry Level", "Junior", "Mid Level"])
    with f3:
        sort = st.selectbox("Sort by", ["Relevance", "Newest", "Salary: High to Low"])

    results = st.session_state.jobs + st.session_state.posted_jobs
    k = keyword.lower().strip()
    loc = location.lower().strip()

    if k:
        results = [
            j for j in results
            if k in j["title"].lower()
            or k in j["company"].lower()
            or k in j["category"].lower()
            or any(k in skill.lower() for skill in j["skills"])
        ]
    if loc:
        results = [j for j in results if loc in j["location"].lower() or (loc == "remote" and j["mode"] == "Remote")]
    if mode != "Any":
        results = [j for j in results if j["mode"] == mode]
    if category != "All":
        results = [j for j in results if j["category"] == category]
    if experience != "All":
        results = [j for j in results if j["experience"] == experience]

    if sort == "Newest":
        results = list(reversed(results))
    elif sort == "Salary: High to Low":
        def salary_num(j):
            nums = re.findall(r'[\d,]+', j["salary"])
            return int(nums[0].replace(",", "")) if nums else 0
        results = sorted(results, key=salary_num, reverse=True)

    st.markdown(f"### {len(results):,} jobs found")
    if results:
        for job in results:
            job_card(job)
    else:
        st.info("No jobs match your current filters. Try changing your keyword, location or filters.")

# -----------------------------
# Job Details
# -----------------------------
elif st.session_state.page == "Job Details":
    job = get_job(st.session_state.selected_job)
    if not job:
        st.warning("Job not found.")
        if st.button("Back to jobs"):
            go("Find Jobs")
    else:
        if st.button("← Back to jobs"):
            go("Find Jobs")
        st.markdown(f"""
        <div class="detail-box">
            <div style="font-size:1.8rem;font-weight:800;color:#172033;">{job["title"]}</div>
            <div class="company" style="font-size:1.05rem;">{job["company"]}</div>
            <div class="meta">📍 {job["location"]} &nbsp; • &nbsp; {job["mode"]} &nbsp; • &nbsp; {job["type"]}</div>
            <div class="salary">{job["salary"]}</div>
            <div class="meta">Experience: {job["experience"]} &nbsp; • &nbsp; Posted {job["posted"]}</div>
        </div>
        """, unsafe_allow_html=True)

        left, right = st.columns([2.2, 1])
        with left:
            st.markdown("### Job description")
            st.write(job["description"])
            st.markdown("### Responsibilities")
            for x in job["responsibilities"]:
                st.markdown(f"- {x}")
            st.markdown("### Requirements")
            for x in job["requirements"]:
                st.markdown(f"- {x}")
            st.markdown("### Required skills")
            st.markdown(" ".join([f"`{x}`" for x in job["skills"]]))
            st.markdown("### Benefits")
            st.markdown("- Flexible working environment\n- Learning and development opportunities\n- Professional growth")

        with right:
            st.markdown('<div class="detail-box">', unsafe_allow_html=True)
            st.markdown("### Apply for this job")
            if st.button("Apply Now", type="primary", use_container_width=True):
                st.session_state.apply_job = job["id"]
                st.session_state.page = "Apply"
                st.rerun()
            saved = job["id"] in st.session_state.saved_jobs
            if st.button("Remove from Saved" if saved else "Save Job", use_container_width=True):
                if saved:
                    st.session_state.saved_jobs.remove(job["id"])
                else:
                    st.session_state.saved_jobs.add(job["id"])
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Apply
# -----------------------------
elif st.session_state.page == "Apply":
    job = get_job(st.session_state.get("apply_job"))
    if not job:
        st.error("Job not found.")
    else:
        st.markdown("## Apply for this job")
        st.markdown(f"**{job['title']}** · {job['company']}")
        st.markdown('<div class="notice">Your application will be stored in this demo session. Connect a database before production use.</div>', unsafe_allow_html=True)
        with st.form("application_form"):
            name = st.text_input("Full name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            portfolio = st.text_input("Portfolio / LinkedIn URL")
            resume = st.file_uploader("Upload resume", type=["pdf", "doc", "docx"])
            cover = st.text_area("Cover letter", height=150, placeholder="Tell the employer why you are a good fit...")
            confirm = st.checkbox("I confirm that the information provided is accurate.")
            submitted = st.form_submit_button("Submit Application", type="primary", use_container_width=True)

            if submitted:
                if not name or not email or not confirm:
                    st.error("Please provide your name, email and confirmation.")
                else:
                    st.session_state.applications.append({
                        "job": job["title"], "company": job["company"],
                        "date": datetime.now().strftime("%d %b %Y"),
                        "status": "Under Review"
                    })
                    st.success("Application submitted successfully!")
                    st.balloons()

# -----------------------------
# Saved Jobs
# -----------------------------
elif st.session_state.page == "Saved Jobs":
    st.markdown("## Saved jobs")
    saved = [j for j in st.session_state.jobs + st.session_state.posted_jobs if j["id"] in st.session_state.saved_jobs]
    if not saved:
        st.info("You have not saved any jobs yet. Browse jobs and tap ☆ to save one.")
        if st.button("Find Jobs", type="primary"):
            go("Find Jobs")
    else:
        st.markdown(f"**{len(saved)} saved jobs**")
        for job in saved:
            job_card(job)

# -----------------------------
# Dashboard
# -----------------------------
elif st.session_state.page == "Dashboard":
    st.markdown("## Job seeker dashboard")
    st.markdown("### Welcome back 👋")
    cols = st.columns(4)
    metrics = [
        ("Applications", len(st.session_state.applications)),
        ("Interviews", sum(1 for x in st.session_state.applications if x["status"] == "Interview")),
        ("Saved Jobs", len(st.session_state.saved_jobs)),
        ("Profile", f'{st.session_state.profile_complete}%'),
    ]
    for col, (num, label) in zip(cols, metrics):
        with col:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Recent applications</div>', unsafe_allow_html=True)
    if st.session_state.applications:
        for app in st.session_state.applications:
            st.markdown(
                f'<div class="job-card"><div class="job-title">{app["job"]}</div>'
                f'<div class="company">{app["company"]}</div>'
                f'<div class="meta">Applied {app["date"]} • Status: <b>{app["status"]}</b></div></div>',
                unsafe_allow_html=True
            )
    else:
        st.info("You have not submitted any applications yet.")

    st.markdown('<div class="section-title">Recommended jobs</div>', unsafe_allow_html=True)
    for job in st.session_state.jobs[:3]:
        job_card(job)

# -----------------------------
# Profile
# -----------------------------
elif st.session_state.page == "Profile":
    st.markdown("## My profile")
    st.markdown(f"### Your profile is {st.session_state.profile_complete}% complete")
    st.progress(st.session_state.profile_complete / 100)

    with st.form("profile"):
        name = st.text_input("Full name", value="Ahmed Khan")
        headline = st.text_input("Professional headline", value="Computer Science Student")
        location = st.text_input("Location", value="Pakistan")
        about = st.text_area("About", value="CS student interested in software development, AI and modern web technologies.")
        skills = st.text_input("Skills", value="Python, Git, Streamlit, HTML, CSS")
        education = st.text_input("Education", value="BS Computer Science")
        save = st.form_submit_button("Save Profile", type="primary")
        if save:
            st.session_state.profile_complete = 85
            st.success("Profile updated successfully.")

# -----------------------------
# Post Job
# -----------------------------
elif st.session_state.page == "Post a Job":
    st.markdown("## Post a job")
    st.markdown("Create a professional listing for candidates.")
    with st.form("post_job"):
        title = st.text_input("Job title")
        company = st.text_input("Company name")
        location = st.text_input("Location", placeholder="e.g. Islamabad, Pakistan")
        mode = st.selectbox("Work arrangement", ["Remote", "Hybrid", "On-site"])
        job_type = st.selectbox("Employment type", ["Full-time", "Part-time", "Internship", "Contract"])
        experience = st.selectbox("Experience level", ["Internship", "Entry Level", "Junior", "Mid Level", "Senior"])
        category = st.selectbox("Category", ["Software Development", "Design", "Data", "AI & ML", "Marketing", "Cybersecurity"])
        salary = st.text_input("Salary", placeholder="e.g. PKR 80,000 – 120,000/month")
        skills = st.text_input("Skills", placeholder="Python, Git, SQL")
        description = st.text_area("Job description", height=130)
        responsibilities = st.text_area("Responsibilities", height=120, placeholder="One responsibility per line")
        requirements = st.text_area("Requirements", height=120, placeholder="One requirement per line")
        publish = st.form_submit_button("Publish Job", type="primary", use_container_width=True)

        if publish:
            if not title or not company or not location or not description:
                st.error("Please fill in the required fields.")
            else:
                new_id = 100 + len(st.session_state.posted_jobs)
                st.session_state.posted_jobs.append({
                    "id": new_id,
                    "title": title,
                    "company": company,
                    "location": location,
                    "mode": mode,
                    "type": job_type,
                    "experience": experience,
                    "salary": salary or "Salary not disclosed",
                    "posted": "Just now",
                    "category": category,
                    "skills": [x.strip() for x in skills.split(",") if x.strip()],
                    "description": description,
                    "responsibilities": [x.strip() for x in responsibilities.splitlines() if x.strip()],
                    "requirements": [x.strip() for x in requirements.splitlines() if x.strip()],
                })
                st.success("Job published successfully.")
                st.session_state.page = "Find Jobs"

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    '<div class="footer">© 2026 JobHunt Pro · Professional opportunities, simplified.</div>',
    unsafe_allow_html=True
)
