"""Configuration: load secrets from the environment, never hard-code them."""

import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
GEMINI_API_KEY = os.getenv("ANTHROPIC_API_KEY")
