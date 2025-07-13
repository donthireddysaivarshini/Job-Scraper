import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_driver_path = "C:/Tools/chromedriver.exe"

# Session state init
if "jobs" not in st.session_state: st.session_state["jobs"] = []
if "job_title" not in st.session_state: st.session_state["job_title"] = ""
if "organization" not in st.session_state: st.session_state["organization"] = ""
if "category" not in st.session_state: st.session_state["category"] = "ALL"

# Category formatter
def format_category_url(category):
    special_cases = {
        "Fonts & Typography": "fonts-typography",
        "UI/UX Design": "ui-ux-design",
    }
    return special_cases.get(category, category.lower().replace(' ', '-'))

# Scraper
def scrape_jobs_by_category(category):
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    scraped_jobs = []
    try:
        if category == "ALL":
            driver.get("https://www.behance.net/joblist")
        else:
            category_url = format_category_url(category)
            driver.get(f"https://www.behance.net/joblist?category={category_url}")
        time.sleep(2)

        scrollable_container = driver.find_element(By.TAG_NAME, "body")
        for _ in range(6):
            scrollable_container.send_keys(Keys.PAGE_DOWN)
            time.sleep(1.5)
            job_cards = driver.find_elements(By.CLASS_NAME, 'JobCard-jobCard-mzZ')
            for job in job_cards:
                try:
                    title = job.find_element(By.CLASS_NAME, 'JobCard-jobTitle-LS4').text
                    company = job.find_element(By.CLASS_NAME, 'JobCard-company-GQS').text
                    location = job.find_element(By.CLASS_NAME, 'JobCard-jobLocation-sjd').text
                    description = job.find_element(By.CLASS_NAME, 'JobCard-jobDescription-SYp').text
                    link = job.find_element(By.CLASS_NAME, 'JobCard-jobCardLink-Ywm').get_attribute("href")
                    try:
                        logo_img = job.find_element(By.CSS_SELECTOR, '.JobLogo-logo-pNN img')
                        logo_url = logo_img.get_attribute('src')
                    except:
                        logo_url = None

                    scraped_jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "description": description,
                        "link": link,
                        "logo": logo_url
                    })
                except Exception as e:
                    print("Error extracting job details:", e)
        return scraped_jobs
    finally:
        driver.quit()

# ----------------- Streamlit UI ---------------------
st.title("🎨 Creative Jobs Finder")

# Step 1: Select Category
job_categories = [ "Logo Design",
    "Stationery Design",
    "Fonts & Typography",
    "Branding Services",
    "Book Design",
    "Packaging Design",
    "Album Cover Design",
    "Signage Design",
    "Invitation Design",
    "T-Shirt & Merchandise",
    "Flyer & Brochure Design",
    "Poster Design",
    "Identity Design",
    "Website Design",
    "App Design",
    "UI/UX Design",
    "Landing Page Design",
    "Icon Design",
    "Illustrations",
    "Portraits",
    "Comics & Character Design",
    "Fashion Design",
    "Pattern Design",
    "Storyboards",
    "Tattoo Design",
    "NFT Art",
    "3D Illustration",
    "Children's Illustration",
    "Social Media Design",
    "Presentation Design",
    "Infographic Design",
    "Resume Design",
    "Copywriting",
    "Product Photography",
    "Landscape Photography",
    "Image Editing & Retouching",
    "Portrait Photography",
    "Architecture & Interior Design",
    "Landscape Design",
    "Industrial Design",
    "Graphics for Streamers",
    "Game Design",
    "Creative Tool Coaching",
    "Mentorship & Career Advice",
    "Modeling Projects",
    "Architecture Renderings",
    "Music Composition & Production",
    "Sound Design",
    "Animated Gifs",
    "Logo Animation",
    "Motion Graphics",
    "Video Production & Editing",
    "Explainer Videos",
    "Short Video Ads",]
st.session_state["category"] = st.selectbox("1️⃣ Select a Job Category", job_categories, index=job_categories.index(st.session_state["category"]))

# Step 2: Search Type
search_type = st.radio("2️⃣ Search By", ["Job Title", "Organization", "Both"])

if search_type == "Job Title":
    st.session_state["job_title"] = st.text_input("Enter Job Title", st.session_state["job_title"])
    st.session_state["organization"] = ""
elif search_type == "Organization":
    st.session_state["organization"] = st.text_input("Enter Organization Name", st.session_state["organization"])
    st.session_state["job_title"] = ""
else:
    col1, col2 = st.columns(2)
    with col1:
        st.session_state["job_title"] = st.text_input("Job Title", st.session_state["job_title"])
    with col2:
        st.session_state["organization"] = st.text_input("Organization", st.session_state["organization"])

# Step 3: Run
if st.button("🚀 Run"):
    with st.spinner("Scraping jobs..."):
        st.session_state["jobs"] = scrape_jobs_by_category(st.session_state["category"])
    st.success("Scraping completed!")

# Step 4: Reset
if st.button("🔄 Reset Search"):
    st.session_state["jobs"] = []
    st.session_state["job_title"] = ""
    st.session_state["organization"] = ""
    st.session_state["category"] = "ALL"
    st.experimental_rerun()

# Step 5: Show Jobs
if st.button("📄 Show Jobs"):
    jobs = st.session_state.get("jobs", [])

    job_title = st.session_state["job_title"].strip().lower()
    org = st.session_state["organization"].strip().lower()

    if job_title:
        jobs = [job for job in jobs if job_title in job["title"].lower()]
    if org:
        jobs = [job for job in jobs if org in job["company"].lower()]

    if jobs:
        cols_per_row = 3
        for i in range(0, len(jobs), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(jobs):
                    job = jobs[i + j]
                    logo_html = (
                        f'<img src="{job["logo"]}" alt="logo" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover;">'
                        if job["logo"] else
                        f'<div style="width: 44px; height: 44px; border-radius: 50%; background-color: #f2c94c; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 12px; color: black;">{job["company"][:6].upper()}</div>'
                    )

                    card_html = f"""
                        <div style="background: #fff; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.06);
                                    padding: 20px; margin-bottom: 20px; display: flex; flex-direction: column;
                                    font-family: 'Segoe UI', sans-serif; height: 320px; justify-content: space-between;">
                            <div style="display: flex; justify-content: space-between;">
                                <div style="display: flex; align-items: center;">
                                    {logo_html}
                                    <div style="margin-left: 12px;">
                                        <p style="margin: 0; font-weight: bold;">{job['company']}</p>
                                        <p style="margin: 0; font-size: 12px; color: #666;">{job['location']}</p>
                                    </div>
                                </div>
                                <div style="color: #999; font-size: 18px;">&#9734;</div>
                            </div>
                            <div style="margin-top: 14px;">
                                <h4 style="margin: 0; font-size: 18px; color: #111;">{job['title']}</h4>
                                <p style="margin-top: 6px; font-size: 14px; color: #444;
                                        display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
                                        overflow: hidden; text-overflow: ellipsis;">
                                    {job['description']}
                                </p>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <a href="{job['link']}" target="_blank" style="background-color: black; color: white;
                                padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 13px;">
                                    Apply Now
                                </a>
                                <span style="font-size: 12px; color: #999;">Posted recently</span>
                            </div>
                        </div>
                    """
                    with cols[j]:
                        st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.warning("No matching jobs found.")
