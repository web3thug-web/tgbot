from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")