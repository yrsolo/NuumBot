"""Constants for the project."""
import os
from types import MappingProxyType as MapProxy

from dotenv import load_dotenv

load_dotenv()


TG = os.environ.get('TG_TOKEN')
OPENAI = os.environ.get('OPENAI_TOKEN')
ORG = os.environ.get('ORG_TOKEN')
EMAIL = os.environ.get('EMAIL')
PASS = os.environ.get('PASS')

PROXIES = MapProxy({
    'https://': 'http://FHmgTs:RFBgtW@195.158.194.74:8000',
})

MODEL = 'gpt-3.5-turbo'

TEXT_MODEL = 'gpt-3.5-turbo'
IMG_MODEL = 'dall-e-3'

COMMENT_PROMPT = 'Write a comment for this image:'

NUUM = 'https://nuum.ru/'
POLINA_CLIPS = 'https://nuum.ru/channel/polinakrusenstern/clips'
CLIPS = 'https://nuum.ru/clips'


cookie_path = 'cookies\\cookies.pkl'