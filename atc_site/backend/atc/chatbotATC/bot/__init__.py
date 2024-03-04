from decouple import config
import openai
from openai import OpenAI
import json

client = OpenAI(api_key=config("OPENAI_API_KEY"))

GPT_MODEL = "gpt-3.5-turbo-1106" #* "gpt-4-1106-preview" or "gpt-3.5-turbo-1106"

TOOLS = json.load(open('atc_site/backend/atc/chatbotATC/bot/training_data.json', 'r'))
