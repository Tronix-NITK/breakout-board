import cv2


def get_command():
    key = cv2.waitKey(10)
    if key == -1:
        return None
    return chr(key)
