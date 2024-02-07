from decouple import config
import openai
from openai import OpenAI
import json
import string
import random
import requests
import uuid
import os

from atc_site.settings import MEDIA_ROOT

client = OpenAI(api_key=config("OPENAI_API_KEY"))

MODEL = 'dall-e-3'


FILE_PATH = f'{MEDIA_ROOT}/images/ai_images/'