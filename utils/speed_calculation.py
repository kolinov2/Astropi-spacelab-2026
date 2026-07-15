def time_difference(t1, t2) -> int:
    return (t2 - t1).seconds

def calculate_speed_kmps(mean_distance_px, gsd, time_diff):
    return (mean_distance_px * gsd / 100000) / time_diff

def filter_speeds(speeds, perfect, frame, log):
    lo, hi = perfect - frame, perfect + frame
    filtered = []

    for s in speeds:
        if lo <= s <= hi:
            filtered.append(s)
        else:
            log(f"Speed rejected by frame filter: {s:.3f} km/s")

    return filtered

def safe_average(values):
    return sum(values) / len(values) if values else None
