import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from config import *
from utils.logger import log
from utils.sensor_logger import SensorLogger
from utils.camera_capture import take_photo
from utils.image_processing import (
    get_time,
    convert_to_cv,
    calculate_features,
    calculate_matches,
    mean_feature_distance
)

from utils.speed_calculation import (
    time_difference,
    calculate_speed_kmps,
    filter_speeds,
    safe_average
)

from utils.cleanup import cleanup_photos

log("Program started")

sensor_logger = None

if ENABLE_SENSOR_LOGGING:
    sensor_log_path = os.path.join(BASE_DIR, SENSOR_LOG_FILE)
    sensor_logger = SensorLogger(sensor_log_path)
    log("Sensor logging enabled")

start_time = time.time()
photos = []
speeds = []

photo_id = 0
previous_photo = None

while time.time() - start_time < DURATION:
    photo_name = f"photo_{photo_id}.jpg"
    photo_path = os.path.join(BASE_DIR, photo_name)

    try:
        take_photo(photo_path)
    except Exception as e:
        log(f"Camera error – stopping capture: {e}")
        break

    photos.append(photo_path)
    log(f"Photo taken: {photo_name}")

    #rolling cleanup
    if len(photos) > MAX_IMAGES:
        old = photos.pop(0)
        if os.path.exists(old):
            os.remove(old)
            log(f"Deleted old photo: {os.path.basename(old)}")

    if previous_photo:
        try:
            img1_cv, img2_cv = convert_to_cv(previous_photo, photo_path)

            kp1, kp2, des1, des2 = calculate_features(img1_cv, img2_cv)

            if des1 is None or des2 is None:
                raise ValueError("Descriptors missing")

            matches = calculate_matches(des1, des2)
            if len(matches) < 10:
                raise ValueError("Not enough matches")

            mean_dist = mean_feature_distance(kp1, kp2, matches)

            t1 = get_time(previous_photo)
            t2 = get_time(photo_path)
            dt = time_difference(t1, t2)

            if dt <= 0:
                raise ValueError("Invalid time difference")

            speed = calculate_speed_kmps(mean_dist, GSD, dt)
            speeds.append(speed)
            log(f"Speed calculated: {speed:.3f} km/s")

        except Exception as e:
            log(f"Pair skipped: {e}")

    previous_photo = photo_path
    photo_id += 1
    # --- Optional Sense HAT sensor logging ---
    if sensor_logger:
        try:
            sensor_logger.log_once()
        except Exception as e:
            log(f"Sensor logging error: {e}")
    time.sleep(INTERVAL)

log("Capture finished")

# ================== Result ==================

filtered = filter_speeds(speeds, REFERENCE_SPEED, FRAME, log)
final_speed = safe_average(filtered)

if final_speed is not None:
    result_str = "{:.5g}".format(final_speed)
    with open(RESULT_FILE, "w") as f:
        f.write(result_str)
    log(f"Final speed delivered: {final_speed:.3f}")
else:
    log("No valid speed could be calculated")

# ================== Cleaning ==================

cleanup_photos(photos, MAX_IMAGES, log)
log("Program finished")
