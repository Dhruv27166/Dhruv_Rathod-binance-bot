# src/config.py
import os
from dotenv import load_dotenv

# Load .env from project root
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

if not API_KEY or not API_SECRET:
    raise RuntimeError("Missing BINANCE_API_KEY or BINANCE_API_SECRET in .env")
