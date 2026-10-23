import os

# GitHub Actions automatically CI=true set karta hai
IS_CI = os.getenv("CI", "").lower() == "true"

BASE_URL = "https://www.saucedemo.com"
HEADLESS = IS_CI            # local pe browser dikhega, CI pe headless
SLOW_MO = 0 if IS_CI else 0          # local pe dekhna ho toh doosra 0 badal do (jaise 1000)
DEFAULT_TIMEOUT = 10000
DEMO_PAUSE = 0 if IS_CI else 0       # local pe dekhna ho toh doosra 0 badal do (jaise 2000)

STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"