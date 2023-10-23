import time
import random

from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from instagrapi import Client
from instagrapi.exceptions import LoginRequired

import requests


class InstagramBot():
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.client = self._get_client()
        self.driver: webdriver.Chrome = Driver(uc=True)
        self.wait = WebDriverWait(self.driver, 10)

    def _get_client(self):
        cl = Client()
        cl.login(self.username, self.password)
        return cl

    def download(self, url, file_path):
        self.driver.get("https://sssinstagram.com/pt/reels-downloader")
        self.driver.find_element(
            By.XPATH, "//input[@id='main_page_text']").send_keys(url)
        self.driver.find_element(By.XPATH, "//button[@id='submit']").click()
        target_url = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='response']//a[contains(text(), 'Baixar')]"))).get_attribute("href")
        self.driver.close()

        r = requests.get(target_url)
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=255):
                if chunk:
                    f.write(chunk)
            f.close()

    def upload(self, file_path, caption):
        if ".mp4" in file_path:
            self.client.video_upload(path=file_path, caption=caption)
        elif ".jpg" in file_path or ".jpeg" in file_path:
            self.client.photo_upload(path=file_path, caption=caption)

    def _get_comments(self, url, amount=500):
        media_id = self.client.media_id(self.client.media_pk_from_url(url))
        comments = []
        next_min_id = None
        for i in range(3):
            previous_next_min_id = next_min_id
            fetch_next = random.randint(100, 200)

            try:
                (comments_part, next_min_id) = self.client.media_comments_chunk(
                    media_id, fetch_next, next_min_id)
            except LoginRequired as e:
                print(f"A login required error occurred at iteration {i}")
                self.client = self._get_client()

            for comment in comments_part:
                comments.append(comment)

            if next_min_id == previous_next_min_id:
                break
        return comments

    def choose_comment(self, url):
        return max(self._get_comments(url), key=lambda x: x.like_count).text
