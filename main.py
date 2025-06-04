import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 


class LogInLinkedin:
    def __init__(self,driver):
        self.driver = driver
        self.password= password
        self.email= email

    def run(self):
        self.driver.get("https://www.linkedin.com/login")
        WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located((By.ID,"username"))
        )
        self.driver.find_element(By.ID,"username").send_keys(email)
        self.driver.find_element(By.ID,"password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(30)
        print("djjd")

class Search:
    def __init__(self,driver,tilte,location):
        self.title = tilte
        self.driver= driver
        self.location = location

    def run(self):
        # self.driver.get(f"https://www.linkedin.com/jobs/search/?keywords={(self.title).replace(" ","%20")}&location={self.location}")
        self.driver.get("https://www.linkedin.com/jobs")

        search_title = self.driver.find_element(By.CSS_SELECTOR,"input[aria-label='Search by title, skill, or company']")
        search_title.clear()
        search_title.send_keys(self.title)
        time.sleep(2)

        search_location = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")
        search_location.clear()
        search_location.send_keys(self.location)
        time.sleep(1)

        search_location.send_keys(Keys.DOWN)
        search_location.send_keys(Keys.RETURN)
        time.sleep(1)

        # what_input = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")
        # search_title.send_keys(Keys.RETURN)
        time.sleep(5)

class Main:
    def __init__(self, title, email, password, num_results=10 ):
        self.num = num_results
        self.title = title
        self.password = password
        self.email = email
        self.results =[]

        service = Service(executable_path ="chromedriver.exe")
        self.driver = webdriver.Chrome(service=service) 
        self.new_run()

    def new_run(self):
        self.login = LogInLinkedin(self.driver)
        self.search =  Search(self.driver,self.title,"Worldwide")


    def run(self):
        self.login.run()
        self.search.run()
        posts = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'occludable-update') and contains(@class, 'scaffold-layout__list-item')]")

        for post in posts:
            print(post.text)
            self.driver.execute_script("arguments[0].scrollIntoView();", post)
            time.sleep(1)
            my_list=[]
            title= WebDriverWait(post, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.job-card-list__title--link"))).get_attribute("aria-label")
            my_list.append(title)
            company = WebDriverWait(post, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"div.artdeco-entity-lockup__subtitle"))).text
            my_list.append(company)
            location = WebDriverWait(post, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"div.artdeco-entity-lockup__caption"))).text
            link= WebDriverWait(post, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.job-card-list__title--link"))).get_attribute("href")  
            
            loc,type=location.split("(")
            type=type[:-1]
            my_list.append(loc)
            my_list.append(type)
            my_list.append(link)
            self.results.append(my_list)


    def save_to_csv(self):
        pd.DataFrame(self.results).to_csv("job_results.csv", index=False)

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    email = "atasadig56@gmail.com"
    password = "ata5831Sm"
    scraper = Main("data analyst", email, password, num_results=10)
    scraper.run()
    scraper.save_to_csv()
    scraper.close()
