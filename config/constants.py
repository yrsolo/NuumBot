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


cookie_path = 'browser\\cookies\\cookies.pkl'

STICKERS = [
    'https://static.nuum.ru/sticker-packs/seal/webp/medium/seal-08.webp',
    'https://static.nuum.ru/sticker-packs/seal/webp/medium/seal-05.webp'
    'https://static.nuum.ru/sticker-packs/nuum/webp/medium/nuum-09.webp',
    'https://static.nuum.ru/sticker-packs/seal/webp/medium/seal-03.webp',
    'https://static.nuum.ru/sticker-packs/seal/webp/medium/seal-07.webp',
    'https://static.nuum.ru/sticker-packs/goose/webp/medium/goose-05.webp',
    'https://static.nuum.ru/sticker-packs/goose/webp/medium/goose-14.webp',
    'https://static.nuum.ru/sticker-packs/boar/webp/large/boar-01.webp',
    'https://static.nuum.ru/sticker-packs/boar/webp/large/boar-05.webp',
    'https://static.nuum.ru/sticker-packs/boar/webp/medium/boar-06.webp',
    'https://static.nuum.ru/sticker-packs/boar/webp/medium/boar-14.webp',
    'https://static.nuum.ru/sticker-packs/dog-loaf/webp/medium/dog-loaf-12.webp',
    'https://static.nuum.ru/sticker-packs/dog-loaf/webp/large/dog-loaf-08.webp',
    'https://static.nuum.ru/sticker-packs/dog-loaf/webp/large/dog-loaf-15.webp',
    'https://static.nuum.ru/sticker-packs/doggy/webp/large/doggy-07.webp',
    'https://static.nuum.ru/sticker-packs/cat-meme/webp/large/cat-meme-08.webp',
    'https://static.nuum.ru/sticker-packs/cat-meme/webp/large/cat-meme-09.webp',
    'https://static.nuum.ru/sticker-packs/cat-meme/webp/large/cat-meme-18.webp',
    'https://static.nuum.ru/sticker-packs/rabbit/webp/large/rabbit-03.webp',
    'https://static.nuum.ru/sticker-packs/cat-yolk/webp/large/cat-yolk-05.webp',
]

STICKERS_PACKS = [s.split('/')[-4] for s in STICKERS]
STICKERS = [s.split('/')[-1] for s in STICKERS]


