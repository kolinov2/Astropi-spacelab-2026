from picamzero import Camera

_camera = Camera()

def take_photo(path: str):
    _camera.take_photo(path)
