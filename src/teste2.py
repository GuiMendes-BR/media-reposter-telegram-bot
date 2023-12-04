from seleniumbase import Driver
from time import sleep
import os

os.system("export DISPLAY=$HOST_IP:99")
d = Driver(browser='chrome', headed=True)
d.open('youtube.com')
print("Aguardando")

sleep(600)