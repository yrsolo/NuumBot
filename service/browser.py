from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import NUUM
import pickle

from config import cookie_path

class Browser:
    def __init__(self, cookies_path=cookie_path):
        self.cookies_path = cookies_path
        self.driver = self.start_browser()

    def start_browser(self):
        driver = webdriver.Chrome()

        #chrome_options = Options()
        #chrome_options.add_argument("--user-data-dir=browser/profile")
        #driver = webdriver.Chrome(options=chrome_options)
        driver.get(NUUM)

        return driver

    def save_cookies(self):
        # Сохраняем куки с помощью pickle
        with open(self.cookies_path, 'wb') as file:
            pickle.dump(self.driver.get_cookies(), file)

    def load_cookies(self):
        # Загружаем куки с использованием pickle
        with open(self.cookies_path, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        self.driver.refresh()