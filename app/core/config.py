import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")

print(f"FIREBASE_CREDENTIALS_PATH: {FIREBASE_CREDENTIALS_PATH}")

if not FIREBASE_CREDENTIALS_PATH:
    raise RuntimeError("Firebase credentials path not set")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment variables")
