import cv2


class Camera:
    """
    Класс для работы с камерой
    """
    def __init__(self, camera_id):
        """
            camera_id (int): id камеры
        """
        self.__capture = cv2.VideoCapture(camera_id)
    
    def get_frame(self):
        ret, frame = self.__capture.read()
        if not ret:
            return
        return frame
    
    def close(self):
        self.__capture.release()