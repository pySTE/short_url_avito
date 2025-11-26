import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
MAIN_URL = os.getenv("MAIN_URL")