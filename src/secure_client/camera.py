import cv2


class Camera:
    """
    Класс для работы с камерой
    """

    def __init__(self, camera_id, resolution=(640, 480)):
        """
            camera_id [int]: id камеры
            resolution [tuple]: разрешение (ширина, высота)
        """
        self.__capture = cv2.VideoCapture(camera_id)

        width, height = resolution
        self.__capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame(self):
        ret, frame = self.__capture.read()
        if not ret:
            return
        return frame

    def close(self):
        self.__capture.release()
