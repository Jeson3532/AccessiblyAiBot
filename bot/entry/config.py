from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
DEBUG_MODE = bool(os.getenv("DEBUG_MODE"))
