from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login_to_instagram(username, password):
    # Set up Chrome options
    options = Options()
    
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--headless=new")  # Use the updated headless mode for Chrome


    # Specify the path to chromedriver using the Service class
    service = Service("Webdriver/chromedriver.exe")  # Update with your correct path

    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open Instagram login page
        driver.get("https://www.instagram.com")
        time.sleep(2)

        # Enter credentials
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        # Check if login is successful
        if "login" not in driver.current_url:
            print("Login successful!")
            return driver  # Return driver for further use
        else:
            print("Login failed!")
            driver.quit()
            return None
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()
        return None



def scrape_profiles(driver, query):
    try:
        # Navigate to the Instagram hashtag page
        driver.get(f"https://www.instagram.com/explore/tags/{query}/")
        
        # Wait for the main content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
        time.sleep(3)

        # Scroll to load more posts
        for _ in range(3):  # Adjust range to scroll more times if needed
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Extract post links
        posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
        post_links = [post.get_attribute("href") for post in posts]

        profile_links = set()
        for post_link in post_links[:5]:  # Limit to the first 5 posts
            driver.get(post_link)
            time.sleep(2)
            
            # Extract profile link
            try:
                profile_link = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/')]"))
                ).get_attribute("href")
                profile_links.add(profile_link)
            except Exception as e:
                print(f"Failed to extract profile link for post {post_link}: {e}")
        
        return list(profile_links)
    except Exception as e:
        print(f"Error while scraping profiles: {e}")
        return []

    
# Example usage
if __name__ == "__main__":
    username = "ruksha.roy.5891"
    password = "Mima#20"

    driver = login_to_instagram(username, password)
    if driver:
        profiles = scrape_profiles(driver, "travel")
        print("Profiles:", profiles)
        driver.quit()

def extract_email(driver, profile_url):
    try:
        driver.get(profile_url)
        time.sleep(3)

        # Extract the bio
        bio = driver.find_element(By.XPATH, "//div[@class='-vDIg']").text

        # Find email in the bio
        email = None
        if "@" in bio:
            email = [word for word in bio.split() if "@" in word][0]

        return email
    except Exception as e:
        print(f"Error while extracting email: {e}")
        return None


