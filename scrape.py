from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Specify the path to chromedriver.exe
chrome_driver_path = "C:/Tools/chromedriver.exe"

# Function to search for a job title on Behance and scrape job data
def search_job_title(job_title):
    # Initialize the Chrome WebDriver with the Service class
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        # Open the Behance job search page with the job title query
        search_url = f"https://www.behance.net/joblist?search={job_title}"
        driver.get(search_url)

        # Wait until the job listings are present on the page
        print(f"\nSearching for '{job_title}' jobs...\n")
        job_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".JobCard-jobCard-mzZ"))  # CSS selector for job listings
        )

        if len(job_listings) == 0:
            print(f"No job listings found for '{job_title}'. Please try a different search.\n")
            return

        print(f"\nFound {len(job_listings)} job(s) for '{job_title}':\n")
        
        # Loop through the job listings and extract details
        for job in job_listings:
            try:
                # Extract job details using appropriate CSS selectors
                title = job.find_element(By.CSS_SELECTOR, ".JobCard-jobTitle-LS4").text  # Job title selector
                company = job.find_element(By.CSS_SELECTOR, ".JobCard-company-GQS").text  # Company name selector
                location = job.find_element(By.CSS_SELECTOR, ".JobCard-jobLocation-sjd").text  # Location selector
                description = job.find_element(By.CSS_SELECTOR, ".JobCard-jobDescription-SYp").text  # Job description selector
                
                # Print the extracted details
                print(f"Title: {title}\nCompany: {company}\nLocation: {location}\nDescription: {description}\n")
            except Exception as e:
                print(f"Error extracting job details: {e}")

        print(f"\nThese are the jobs for the '{job_title}'.\n")

        # Wait for a while to ensure all results have been loaded
        time.sleep(3)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the browser after scraping is complete
        driver.quit()

# Prompt the user to input the job title
job_title = input("Enter the job title to search: ")

# Perform the search and scraping after receiving the input
search_job_title(job_title)
