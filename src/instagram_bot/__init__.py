import time
from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

class InstagramBot():
    def __init__(self) -> None:
        self.driver: webdriver.Chrome = Driver(uc=True)
        self.wait = WebDriverWait(self.driver, 10)

    def download(self, url, file_path):
        if "https://www.instagram.com/reel/" in url:
            file = self._download_reel(url, file_path)
        elif "https://www.instagram.com/p/" in url:
            file = self._download_photo(url, file_path)
        else:
            print("url type specified not supported")


    def _download_reel(self, url: str, file_path):
        self.driver.get("https://sssinstagram.com/pt/reels-downloader")
        self.driver.find_element(By.XPATH, "//input[@id='main_page_text']").send_keys(url)
        self.driver.find_element(By.XPATH, "//button[@id='submit']").click()
        target_url = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='response']//a[contains(text(), 'Baixar')]"))).get_attribute("href")
        self.driver.close()

        r=requests.get(target_url)
        with open(file_path,'wb') as f:
            for chunk in r.iter_content(chunk_size=255): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
            f.close()

    def _download_photo(self, url):
        pass

if __name__ == "__main__":
    bot = InstagramBot()
    bot.download("https://www.instagram.com/reel/CusGdYluw1s/?igshid=MTc4MmM1YmI2Ng==", "teste.mp4")