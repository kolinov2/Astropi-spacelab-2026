from exif import Image
from datetime import datetime
import cv2
import math

def get_time(image_path: str) -> datetime:
    with open(image_path, 'rb') as f:
        img = Image(f)
        time_str = img.get("datetime_original")
        return datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')

def convert_to_cv(img1_path: str, img2_path: str):
    return cv2.imread(img1_path, 0), cv2.imread(img2_path, 0)

def calculate_features(img1_cv, img2_cv, nfeatures=1000):
    orb = cv2.ORB_create(nfeatures=nfeatures)
    kp1, des1 = orb.detectAndCompute(img1_cv, None)
    kp2, des2 = orb.detectAndCompute(img2_cv, None)
    return kp1, kp2, des1, des2

def calculate_matches(des1, des2):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    return sorted(matches, key=lambda x: x.distance)

def mean_feature_distance(kp1, kp2, matches):
    total = 0
    for m in matches:
        x1, y1 = kp1[m.queryIdx].pt
        x2, y2 = kp2[m.trainIdx].pt
        total += math.hypot(x1 - x2, y1 - y2)
    return total / len(matches)
