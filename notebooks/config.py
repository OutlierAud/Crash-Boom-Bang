from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

#config

USE_SAMPLE = True

if USE_SAMPLE:
    DATA_SRC = DATA_DIR / "eng_2024_main.csv"
else:
    DATA_SRC = (
        "https://raw.githubusercontent.com/"
        "OutlierAud/Crash-Boom-Bang/main/data/eng_2024_main.csv"
    )

FILTERED_DATA_PATH = DATA_DIR / "okinawa_2024_accidents.csv"
MUNICIPAL_DATA_PATH = DATA_DIR / "eng_oka_municipalities.csv"


