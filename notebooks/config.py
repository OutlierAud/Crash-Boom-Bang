#config

USE_SAMPLE = True

if USE_SAMPLE:
    DATA_SRC = "../data/eng_2024_main.csv"
else:
    DATA_SRC = (
        "https://raw.githubusercontent.com/"
        "OutlierAud/Crash-Boom-Bang/main/data/eng_2024_main.csv"
    )