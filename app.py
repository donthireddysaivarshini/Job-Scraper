import streamlit as st
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Specify the path to chromedriver.exe
chrome_driver_path = "C:/Tools/chromedriver.exe"

# Define a function to map category names to URL-compatible formats
def format_category_url(category):
    special_cases = {
        "Fonts & Typography": "fonts-typography",
        "UI/UX Design": "ui-ux-design",
        "Architecture & Interior Design": "architecture-interior-design",
        "T-Shirt & Merchandise": "t-shirt-merchandise",
        "Flyer & Brochure Design": "flyer-brochure-design",
        "Image Editing & Retouching": "image-editing-retouching",
        "Mentorship & Career Advice": "mentorship-and-career-advice",
        "Music Composition & Production": "music-composition-and-production",
        "Video Production & Editing": "video-production-and-editing",
    }
    return special_cases.get(category, category.lower().replace(' ', '-'))

# Define a function to scrape job data
def scrape_jobs(category):
    # Set up the WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        # Open the Behance job listing page for the selected category
        if category == "ALL":
            driver.get("https://www.behance.net/joblist")
        else:
            category_url = format_category_url(category)
            driver.get(f"https://www.behance.net/joblist?category={category_url}")
        time.sleep(2)

        # Find the scrollable container (use 'body' as fallback)
        scrollable_container = driver.find_element(By.TAG_NAME, "body")

        # Initialize the list to store jobs and a set to track already scraped job links
        scraped_jobs = []
        scraped_job_links = set()  # To store unique job links

        # Perform scrolling and scrape jobs
        for _ in range(6):  # Scroll 6 times
            scrollable_container.send_keys(Keys.PAGE_DOWN)
            time.sleep(1.5)  # Adjust delay to ensure content loads

            # Wait for job cards to load dynamically
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "JobCard-jobCard-mzZ"))
            )

            # Extract job cards
            job_cards = driver.find_elements(By.CLASS_NAME, 'JobCard-jobCard-mzZ')
            for job in job_cards:
                try:
                    job_link = job.find_element(By.CLASS_NAME, 'JobCard-jobCardLink-Ywm').get_attribute("href")
                    
                    # Skip job if it's already been scraped
                    if job_link in scraped_job_links:
                        continue

                    # Add the job link to the set to avoid duplicates
                    scraped_job_links.add(job_link)

                    # Extract job details
                    title = job.find_element(By.CLASS_NAME, 'JobCard-jobTitle-LS4').text
                    company = job.find_element(By.CLASS_NAME, 'JobCard-company-GQS').text
                    location = job.find_element(By.CLASS_NAME, 'JobCard-jobLocation-sjd').text
                    description = job.find_element(By.CLASS_NAME, 'JobCard-jobDescription-SYp').text
                    image_url = job.find_element(By.CSS_SELECTOR, '.JobLogo-logoButton-aes img').get_attribute('src')

                  

                    # Append the job to the list
                    scraped_jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "description": description,
                        "logo": image_url,
                        "link": job_link,
                    })
                except Exception as e:
                    print("Error extracting job details:", e)

        return scraped_jobs

    finally:
        driver.quit()

# Streamlit Frontend
st.title("Behance Job Scraper")

# Input/select box for job categories
job_categories = [
    "ALL",
    "Logo Design",
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
    "Short Video Ads",
]

selected_category = st.selectbox("Select a Job Category", job_categories)

# Run button
if st.button("Run"):
    with st.spinner("Scraping jobs, please wait..."):
        if selected_category:
            jobs = scrape_jobs(selected_category)
            st.session_state["jobs"] = jobs
            st.success(f"Data for category '{selected_category}' scraped successfully.")
        else:
            st.warning("Please select a job category.")

# CSS styling to ensure layout starts from left and fills the available space
st.markdown(
    """
    <style>
    /* Background gradient */
    body {
        background: linear-gradient(135deg, #00aaff, #ff7f7f);
        margin: 0;
        padding: 0;
    }

    /* Main container style */
    .stApp {
        max-width: 100%;
        width: 100%;
        margin: 0;
        font-family: 'Arial', sans-serif;
    }

    /* Adjust grid-container for full-width layout */
    .grid-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: flex-start; /* Align items to the left */
        margin-top: 20px;
        width: 100%;
    }

    /* Cards should take up 100% of the available space */
    .card {
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        width: 100%;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: 0.3s ease;
        margin-bottom: 20px;
        height: auto; /* Remove fixed height to prevent cutting off */
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
    }


    .job-title {
        font-size: 18px;
        font-weight: bold;
        color: #007acc;
        margin: 10px 0 5px;
    }
    
    .job-company, .job-location {
        font-size: 14px;
        color: #555;
        margin: 5px 0;
    }

    .job-description {
        font-size: 14px;
        color: #666;
        margin: 10px 0;
    }

    .apply-button {
        background-color: white;
        color: #007acc;
        padding: 10px 15px;
        text-align: center;
        border: 2px solid #007acc;
        border-radius: 5px;
        text-decoration: none;
        font-size: 14px;
        display: inline-block;
    }

    .apply-button:hover {
        background-color: #007acc;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Show Jobs button
if st.button("Show Jobs"):
    jobs = st.session_state.get("jobs", [])
    if jobs:
        # Split jobs into rows of 3
        rows = [jobs[i:i+3] for i in range(0, len(jobs), 3)]
        
        for row in rows:
            cols = st.columns(3)  # Create 3 columns for each row
            for col, job in zip(cols, row):
                with col:
                    # Render job card using markdown and inline styles
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #f9f9f9; 
                            border: 1px solid #ddd; 
                            border-radius: 10px; 
                            padding: 15px; 
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
                            transition: 0.3s ease;
                            display: flex; 
                            flex-direction: column;
                            justify-content: flex-start;
                            margin-bottom: 20px;  /* Add space between rows */
                            height: auto;
                            width: 100%;
                            position: relative;
                        ">
                            <img src="{job['logo']}" alt="Company Logo" style="
                                width: 100px; 
                                height: 100px; 
                                object-fit: cover; 
                                border-radius: 50%; 
                                border: 3px solid #FFFFFF; 
                                margin-bottom: 15px;
                            ">
                            <h4 style="color: #007acc; margin-bottom: 10px;">{job['title']}</h4>
                            <p style="margin: 0; font-weight: bold;">📌 {job['company']}</p>
                            <p style="margin: 0;">📍 {job['location']}</p>
                            <p style="margin-top: 10px; overflow: hidden; text-overflow: ellipsis; 
                                       display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
                                📝 {job['description']}
                            </p>
                            <a href="{job['link']}" target="_blank" 
                               style="display: inline-block; background-color: white; color: #007acc; 
                                      padding: 10px 15px; text-align: center; border: 2px solid #007acc; 
                                      border-radius: 5px; text-decoration: none; font-size: 14px; margin-top: 10px;">
                               Apply Now
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True  # Ensures HTML is rendered properly
                    )
    else:
        st.warning("No data available. Please scrape jobs first.")
