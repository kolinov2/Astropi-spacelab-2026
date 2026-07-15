import os

def cleanup_photos(photos, max_images, log):
    """
    Ensures that no more than max_images photos remain.
    Keeps the first and last photos.
    """

    total = len(photos)

    # Nic nie robimy, jeśli limit nie został przekroczony
    if total <= max_images:
        return

    # Podział na początek i koniec
    first_keep = max_images // 2
    last_keep = max_images - first_keep

    keep = photos[:first_keep] + photos[-last_keep:]

    for p in photos:
        if p not in keep and os.path.exists(p):
            os.remove(p)
            log(f"Deleted photo: {os.path.basename(p)}")