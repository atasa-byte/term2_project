import time
import pickle
import os
import random
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# try to act like human

def human_delay(a=0.5, b=1.5):
    time.sleep(random.uniform(a, b))

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

def scroll_slowly(driver, step=400, delay_range=(0.2, 0.5), times=3):
    for _ in range(times):
        driver.execute_script(f"window.scrollBy(0, {step});")
        time.sleep(random.uniform(*delay_range))

def random_mouse_move(driver):
    try:
        actions = ActionChains(driver)
        width = driver.execute_script("return window.innerWidth")
        height = driver.execute_script("return window.innerHeight")
        x = random.randint(0, width)
        y = random.randint(0, height)
        actions.move_by_offset(x, y).perform()
        human_delay(0.5, 1)
        actions.reset_actions()
    except:
        pass

class LogInLinkedin:
    def __init__(self, driver, password1, email1):
        self.driver = driver
        self.password = password1
        self.email = email1

    def run(self):
        self.driver.get("https://www.linkedin.com/")
        logged_in = False

        if os.path.exists("linkedin_cookies.pkl"):
            human_delay()
            with open("linkedin_cookies.pkl", "rb") as cookies_file:
                cookies = pickle.load(cookies_file)
                for cookie in cookies:
                    if 'expiry' in cookie:
                        del cookie['expiry']
                    self.driver.add_cookie(cookie)

            self.driver.get("https://www.linkedin.com/feed/")
            human_delay()

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "global-nav-search"))
                )
                print("✅ log in successfully with cookies.")
                logged_in = True
            except:
                print("⚠️ cookies invalid or expired. Manual login required.")

        if not logged_in:
            self.driver.get("https://www.linkedin.com/login/")
            print("🔑 Please log in manually and solve the captcha.")

            try:
                WebDriverWait(self.driver, 180).until(
                    EC.presence_of_element_located((By.ID, "global-nav-search"))
                )
                print("✅ Manual login successful.")

                cookies = self.driver.get_cookies()
                with open("linkedin_cookies.pkl", "wb") as cookies_file:
                    pickle.dump(cookies, cookies_file)
                print("💾 Cookies saved.")
            except:
                print("⛔️ Login failed or timeout.")
                self.driver.quit()
                exit()



class Search:
    def __init__(self, driver, title, location):
        self.title = title
        self.driver = driver
        self.location = location

    def run(self):
        try:
            print("jgjghjghffffffff")
            human_delay()
            self.driver.get("https://www.linkedin.com/jobs")
            search_title = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")
            search_title.clear()
            human_delay()
            human_typing(search_title, self.title)

            search_location = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")
            search_location.clear()
            human_delay()
            human_typing(search_location, self.location)
            human_delay()
            search_location.send_keys(Keys.DOWN)
            human_delay()
            search_location.send_keys(Keys.RETURN)
            human_delay(2, 4)
            scroll_slowly(self.driver)
        except Exception as e:
            print("Search error:", e)

class Main:
    def __init__(self, title, email, password, num_results=10):
        self.num = num_results
        self.title = title
        self.password = password
        self.email = email
        self.results = []
        service = Service(executable_path="chromedriver.exe")
        self.driver = webdriver.Chrome(service=service)
        self.new_run()

    def new_run(self):
        self.login = LogInLinkedin(self.driver, self.password, self.email)
        self.search = Search(self.driver, self.title, "Worldwide")

    def run(self):
        self.login.run()
        self.search.run()
        posts = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'occludable-update') and contains(@class, 'scaffold-layout__list-item')]")
        for post in posts[:self.num]:
            self.driver.execute_script("arguments[0].scrollIntoView();", post)
            human_delay(0.7, 1.3)
            scroll_slowly(self.driver, step=300, times=1)
            random_mouse_move(self.driver)

            my_list = []
            try:
                title = WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.job-card-list__title--link"))).get_attribute("aria-label")
                my_list.append(title)
                company = WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.artdeco-entity-lockup__subtitle"))).text
                my_list.append(company)
                location = WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.artdeco-entity-lockup__caption"))).text
                link = WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.job-card-list__title--link"))).get_attribute("href")
                loc, type_ = location.split("(")
                type_ = type_[:-1]
                my_list.extend([loc.strip(), type_.strip(), link])
                self.results.append(my_list)
            except Exception as e:
                print("Error scraping post:", e)

    def save_to_csv(self):
        columns = ["title", "company", "location", "type", "link"]
        pd.DataFrame(self.results, columns=columns).to_csv("job_results.csv", index=False)

    def close(self):
        self.driver.quit()
#  for init test

if __name__ == "__main__":
    load_dotenv()
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    scraper = Main("data analyst", email, password, num_results=10)
    scraper.run()
    scraper.save_to_csv()
    scraper.close()
