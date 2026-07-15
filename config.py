import os

# ================== CONFIG ==================

GSD = 12648 # GSD value for pi camera
INTERVAL = 3   # Time between photos
DURATION = 540  # 9 minutes
MAX_IMAGES = 42 # MAX images at the end of running code
ENABLE_SENSOR_LOGGING = True
SENSOR_LOG_FILE = "sensors.csv"

REFERENCE_SPEED = 7.6  # [km/s] reference speed
# Reference orbital speed of the ISS used ONLY to discard
# extreme outliers caused by image-matching errors.
# The final result is calculated exclusively from measured data.
FRAME = 2.0 # how much room for error in final average speed (e.g. Frame = 1 is values from 6.6 to 8.6 for each pair of photos )

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")
RESULT_FILE = os.path.join(BASE_DIR, "result.txt")
