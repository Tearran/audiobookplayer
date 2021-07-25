# constants.py

# GPIO Pins in BCM
GPIO_PINS = {
        "butA": 5,
        "butB": 6,
        "butX": 16,
        "butY": 24  # old version 20, new version 24
}

# path to icons
ICONS = "/home/pi/player/icons/"

# how long should the player wait before turning off
SLEEP_TIME = 1800

# where are the audiobooks
DEFAULT_AUDIO_PATH = "/home/pi/audiobooks/"
LASTBOOK_PATH = "/home/pi/audiobooks/lastbook.txt"
