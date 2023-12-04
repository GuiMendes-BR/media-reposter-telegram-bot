import os
import random

from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from instagrapi import Client
from instagrapi.exceptions import LoginRequired

import requests

from settings.logger import logger
from settings.config import config

SESSION_FILE = "instagrapi_session.json"

class InstagramBot():
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.client = self._get_client()
        os.system("export DISPLAY=$HOST_IP:99")
        self.driver: webdriver.Firefox = Driver(uc=True, browser='chrome', headed=True)
        self.wait = WebDriverWait(self.driver, 10)

    def _get_client(self):
        logger.info(f"Starting an instagram session for user '{self.username}'...")
        
        delay_range = [1, 3]
        
        cl = Client()
        if config.use_proxy:
            # before_ip = cl._send_public_request("https://api.ipify.org/")
            cl.set_proxy(config.proxy)
            # after_ip = cl._send_public_request("https://api.ipify.org/")
            
            # print(f"Before: {before_ip}")
            # print(f"After: {after_ip}")
        cl.delay_range = delay_range
        
        if os.path.exists(SESSION_FILE):
            cl.load_settings(SESSION_FILE)
            cl.login(self.username, self.password)

        else:
            cl.login(self.username, self.password)
            cl.dump_settings(SESSION_FILE)
        
        return cl

    def download(self, url, file_path):
        logger.info(f"Opening SSSInstagram...")
        self.driver.get(str(config.sssinstagram_url))
        
        logger.info("Getting response from SSSInstagram...")
        self.driver.find_element(
            By.XPATH, "//input[@id='main_page_text']").send_keys(url)
        self.driver.find_element(By.XPATH, "//button[@id='submit']").click()
        target_url = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='response']//a[contains(text(), 'Baixar')]"))).get_attribute("href")
        self.driver.close()

        logger.info(f"Making request to download file '{file_path}'")
        r = requests.get(target_url)
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=255):
                if chunk:
                    f.write(chunk)
            f.close()

    def upload(self, file_path, caption):
        logger.info(f"Uploading file {file_path} with caption {caption} to instagram...")
        if ".mp4" in file_path:
            self.client.video_upload(path=file_path, caption=caption)
        elif ".jpg" in file_path or ".jpeg" in file_path:
            self.client.photo_upload(path=file_path, caption=caption)

    def _get_comments(self, url):
        media_id = self.client.media_id(self.client.media_pk_from_url(url))
        comments = []
        next_min_id = None
        for i in range(1): # If you'd to extract more comments you can increase the range size but if it is too high instagram can block the account
            previous_next_min_id = next_min_id
            fetch_next = random.randint(100, 200)

            try:
                (comments_part, next_min_id) = self.client.media_comments_chunk(
                    media_id, fetch_next, next_min_id)
            except LoginRequired as e:
                logger.info(f"A login required error occurred at iteration {i}")
                self.client = self._get_client()

            for comment in comments_part:
                comments.append(comment)

            if next_min_id == previous_next_min_id:
                break
        return comments

    def choose_comment(self, url):
        logger.info("Choosing best comment...")
        comments = self._get_comments(url)
        # Remove comments from list that contains a mention to someone
        comments = [c for c in comments if '@' not in c.text]
        return max(comments, key=lambda x: x.like_count).text