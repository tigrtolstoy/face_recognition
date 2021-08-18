import cv2
import dlib


class FaceDetector:
    '''
    Класс для детектирования лиц на изображении
    '''

    def __init__(self):
        self.__detector = dlib.get_frontal_face_detector()
        self.__dst_img_size = (600, 600)

    def detect(self, image):
        img = self.__preprocess_image(image)
        faces = self.__detector(img)
        img_height, img_width, _ = image.shape
        faces = self.__reshape_faces_coords(faces, (img_width, img_height))
        return faces

    def __reshape_faces_coords(self, faces, original_image_size):
        coords = [self.__reshape_face(face, original_image_size)
                  for face in faces]
        return coords

    def __reshape_face(self, face, original_image_size):
        x1, y1 = face.tl_corner().x, face.tl_corner().y
        x2, y2 = face.br_corner().x, face.bl_corner().y

        orig_x1, orig_y1 = self.__reshape_point((x1, y1), original_image_size)
        orig_x2, orig_y2 = self.__reshape_point((x2, y2), original_image_size)
        coords = [orig_x1, orig_y1, orig_x2, orig_y2]
        coords = [round(value) for value in coords]
        return coords

    def __reshape_point(self, point, original_image_size):
        orig_w, orig_h = original_image_size
        dst_w, dst_h = self.__dst_img_size
        x, y = point

        orig_x = (x / dst_w) * orig_w
        orig_y = (y / dst_h) * orig_h
        return (orig_x, orig_y)

    def __preprocess_image(self, image):
        img = cv2.resize(image, self.__dst_img_size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
