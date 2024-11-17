import random
import time

from selenium.webdriver.common.by import By
from service.gpt import AsyncOpenAIChatAgent

from config import OPENAI, PROXIES, NUUM, POLINA_CLIPS, CLIPS, cookie_path, EMAIL, PASS

def img_stiker(s):
    s.get_attribute('src')
    # load stiker from url
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
        self.url = el.get_attribute('src')
        self.pos = el.location
        self.link = el.get_attribute('href')

    def click(self):
        self.el.click()

    def get_attribute(self, attr):
        return self.el.get_attribute(attr)


class NuumBaseAction:
    def __init__(self, driver):
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

    def send_stiker(self):
        # comment-input__smile-button ng-star-inserted
        element = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'comment-input__smile-button')]")

        if element:
            rnd_sleep()
            element[0].click()

        element = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Стикеры')]")

        if element:
            rnd_sleep()
            element[0].click()

        rnd_sleep()
        d = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'smiles__navigation-sticker-wrapper')]")
        if d:
            d = random.choice(d)
            d.click()
            time.sleep(1)

        stikers_div = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'sticker ng-star-inserted')]")
        stikers = []
        for s in stikers_div:
            stiker = s.find_elements(By.CSS_SELECTOR, '*')
            if stiker:
                if stiker[0].get_attribute('src'):
                    stikers.append(stiker[0])

        if stikers:
            stiker = random.choice(stikers)
            stiker.click()
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
        return el.pos['y'] > 0 and el.pos['y'] < 1500

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


class NuumActions(NuumBaseAction):
    def __init__(self, driver):
        super().__init__(driver)

    def open_rec(self):
        self.open(CLIPS)
        clips = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/clips/')]")
        if clips:
            clips[0].click()

    def open_subs(self):
        self.open(CLIPS)
        self.find_by_text('Подписки').click()
        clips = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/clips/')]")
        if clips:
            clips[0].click()

    def like_stiker_subscribe(self, like_ratio=1, stiker_ratio=1, subscribe_ratio=1):
        if not self.is_liked():
            like = stiker = subscribe = False
            if stiker_ratio >= random.random():
                stiker = self.send_stiker()
                rnd_sleep()
            if like_ratio >= random.random():
                like = self.like()
                rnd_sleep()
            if subscribe_ratio >= random.random():
                subscribe = self.subscribe()

            name = self.user_name()

            log = [name + ': ', ]
            if stiker:
                log.append('stiker ,')
            if like:
                log.append('like')
            if subscribe:
                log.append('and subscribe')
            if stiker or like or subscribe:
                print(' '.join(log))
                return True
        return False

