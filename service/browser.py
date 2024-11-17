from selenium import webdriver
from config import NUUM

class Browser:
    def __init__(self):
        self.driver = self.start_browser()

    def start_browser(self):
        driver = webdriver.Chrome()
        driver.get(NUUM)

        return driver