from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

class JopFinder:
    def __init__(self, job_title , num_results):
        self.job_title = job_title
        self.num_result = num_results
        self.driver = webdriver.Chrome()
        self.result = []

    def search(self):
        search = self.job_title.replace(' ', '%20')
        url = f"https://www.linkedin.com/jobs/search/?keywords={search}"
        self.driver.get(url)
        time.sleep(5)

    def scrape_results(self):
        jops = self.driver.find_elements(By.CLASS_NAME, "job-card-container__link")
        for jop in jops[:self.num_result]:
            title = jop.find_element(By.CLASS_NAME, "job-card-list__title").text
            link = jop.find_element(By.CLASS_NAME ,"jop-card-list__title").get_attribute('href')
            company = jop.find_element(By.CLASS_NAME ,"jop-card-container__company-name").text
            location = jop.find_element(By.CLASS_NAME ,"jop-card-container__metadata-item").text

            self.result.append({
                'title' : title,
                "Company" : company,
                "Location" : location,
                "Link" : link,
            })

    def save_to_file(self):
        df = pd.DataFrame(self.result)
        df.to_csv('result.csv', index=False)

    def close(self):
        self.driver.close()

if __name__ == "__main__":
    scraper = JopFinder("data analyst", 5)
    scraper.search()
    scraper.scrape_results()
    scraper.save_to_file()
    scraper.close()