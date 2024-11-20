import random
import time

from selenium.webdriver.common.by import By
import pandas as pd

from service.browser import Browser
from service.gpt import AsyncOpenAIChatAgent
from config import OPENAI, PROXIES, NUUM, POLINA_CLIPS, CLIPS, cookie_path, STICKERS_PACKS, STICKERS



def img_sticker(s):
    s.get_attribute('src')
    # load sticker from url
    # example: 'https://static.nuum.ru/sticker-packs/seal/webp/medium/seal-14.webp'
    import requests
    import io
    from PIL import Image

    url = s.get_attribute('src')
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))

    return img


def rnd_sleep(m=1, d=1.5):
    # normal distribution
    sleep = random.normalvariate(m, d)
    # print(sleep)
    time.sleep(max(.5, sleep))


class Elm:
    def __init__(self, el):
        self.class_ = el.get_attribute('class')
        self.text = el.text
        self.tag = el.tag_name
        self.el = el
        self.src = el.get_attribute('src')
        self.location = el.location
        self.link = el.get_attribute('href')

    def click(self):
        self.el.click()

    def get_attribute(self, attr):
        return self.el.get_attribute(attr)


class NuumBaseAction:
    def __init__(self, driver):
        if isinstance(driver, Browser):
            driver = driver.driver
        self.driver = driver
        self.gpt = AsyncOpenAIChatAgent(OPENAI, proxies=PROXIES)
        self.tmp = None

    def find_description(self):
        description_element = self.driver.find_element(By.XPATH, "//app-text-cropper//span[contains(@class, 'text--full')]")
        description_text = self.driver.execute_script("return arguments[0].textContent;", description_element)
        return description_text

    def open(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    def like(self, click_liked=False):
        like_button = self.find_like_button()
        if like_button:
            active = 'active' in like_button.class_
            if not active or click_liked:
                like_button.click()
                return True
        return False

    def subscribe(self):
        sbscrs = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Подписаться')]")
        sbscrs = [Elm(s) for s in sbscrs]
        sbscrs = [s for s in sbscrs if self.in_screen(s)]
        if sbscrs:
            sbscrs[0].click()
            return True
        return False

    def send_sticker(self, only_safe=True):
        # press smile
        element = self.driver.find_elements(By.CLASS_NAME, 'comment-input__smile-button')
        if element:
            element[0].click()
        # select sticker tab
        element = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Стикеры')]")
        if element:
            element[0].click()
        # select sticker pack
        packs = self.driver.find_elements(By.XPATH, "//img[contains(@class, 'smiles__navigation-sticker')]")
        if packs:
            if only_safe:
                packs = [p for p in packs if p.get_attribute('src').split('/')[-2] in STICKERS_PACKS]
            pack = random.choice(packs)
            pack.click()
            rnd_sleep()
        # select sticker
        stickers = []
        smiles_content = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'smiles__content')]")
        if smiles_content:
            stickers = smiles_content[0].find_elements(By.XPATH, "//img[contains(@class, 'sticker-img-loaded')]")
            # stickers = [Elm(s) for s in stickers]
            # stickers = [s for s in stickers if s.is_displayed()]

            if only_safe:
                stickers = [s for s in stickers if s.get_attribute('src').split('/')[-1] in STICKERS]
        # send sticker
        # tmp.append(stickers)
        if stickers:
            sticker = random.choice(stickers)
            # sticker.click()
            self.driver.execute_script("arguments[0].click();", sticker)
            return True
        return False

    def send_comment(self, text):
        textarea = self.driver.find_elements(By.NAME, 'commentInput')
        if textarea:
            textarea = textarea[0]
            # textarea[0].send_keys(text)
            self.driver.execute_script("""
    var textarea = arguments[0];
    console.log('Тип textarea:', textarea.constructor.name);
    console.log('Имеет dispatchEvent:', typeof textarea.dispatchEvent);

    textarea.value = arguments[1];

    var event = document.createEvent('Event');
    event.initEvent('input', true, true);
    textarea.dispatchEvent(event);
""", textarea, text)
        button = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'input-form__send-button')]")
        if button:
            button[0].click()

    def get_clips_from_page(self):
        elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/channel/') and contains(@href, '/clips/')]")
        user_clips = []
        for element in elements:
            link = element.get_attribute('href')
            user_clips.append(link)
        return user_clips

    def generate_comment(self, description):
        prompt = f'Надо написать очень короткий комментарий к тик-ток видео у которого такое описание: !!!" {description}"!!! позитиыный, но не банальный и со смайликами'
        return self.gpt.chat(prompt)

    def find_like_button(self):
        like_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'reactions__button')]")
        like_buttons = [Elm(b) for b in like_buttons]
        like_buttons = [b for b in like_buttons if self.in_screen(b)]
        if like_buttons:
            return like_buttons[0]
        return None

    def is_liked(self, default=True):
        like_button = self.find_like_button()
        if like_button:
            return 'active' in like_button.class_
        return default

    def next(self):
        next_button = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'large secondary-btn only-icon')]")
        if next_button:
            next_button[-1].click()

    def in_screen(self, el):
        x = el.location['x']
        y = el.location['y']
        return y > 0 and x < 1500

    def find_by_text(self, text, el='span'):
        elements = self.driver.find_elements(By.XPATH, f"//{el}[contains(text(), '{text}')]")
        if elements:
            return elements[0]
        return None

    def user_name(self):
        f = 'shorts-bottom-panel-wrapper'
        user_names = self.driver.find_elements(By.XPATH, f"//div[contains(@class, '{f}')]")
        user_names = [Elm(s) for s in user_names]
        user_names = [s for s in user_names if self.in_screen(s)]
        if user_names:
            return user_names[0].text.split('\n')[0]
        return None

    def turn_off_notifications(self):
        btns = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'secondary-btn small only-icon')]")
        click = 0
        for i, b in enumerate(btns):
            svg = b.find_elements(By.CLASS_NAME, 'ng-star-inserted')
            fill = False
            if svg:
                fill = 'icons-bell-filled' in svg[0].get_attribute('data-inlinesvg')
            if fill:
                b.click()
                click += 1
            print(i, '/', len(btns), 'clicked:', click, '                ', end='\r')


class NuumActions(NuumBaseAction):
    def __init__(self, driver):
        super().__init__(driver)

    def open_rec(self):
        self.open(CLIPS)
        rnd_sleep()
        self.driver.refresh()
        rnd_sleep(1)
        clips = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/clips/')]")
        if clips:
            clip = random.choice(clips)
            clip.click()

    def open_subs(self):
        self.open(CLIPS)
        rnd_sleep()
        self.driver.refresh()
        rnd_sleep(1)
        self.find_by_text('Подписки').click()
        rnd_sleep()
        clips = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/clips/')]")
        if clips:
            clip = random.choice(clips)
            clip.click()

    def like_sticker_subscribe(self, like_ratio=1, sticker_ratio=1, subscribe_ratio=1):
        if not self.is_liked():
            rnd_sleep(1)
            like = sticker = subscribe = False
            if sticker_ratio >= random.random():
                sticker = self.send_sticker()
                #rnd_sleep()
            if like_ratio >= random.random():
                like = self.like()
                rnd_sleep()
            if subscribe_ratio >= random.random():
                subscribe = self.subscribe()

            if sticker or like or subscribe:
                name = self.user_name()
                datetime = pd.Timestamp.now()
                return {'name': name, 'sticker': sticker, 'like': like, 'subscribe': subscribe, 'time': datetime}
        return None

