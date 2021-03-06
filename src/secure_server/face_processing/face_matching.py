import os
import cv2
import face_recognition
from src.secure_server.image_processing import crop_face



class FaceMatcher:
    def __init__(self, path_to_references):
        self.__path_to_references = path_to_references
        self.__img_size_to_encode = (150, 150)

    def compare_faces(self, face1, face2):
        encoded_face1 = self.__encode_face(face1)
        encoded_face2 = self.__encode_face(face2)
        distance = face_recognition.face_distance([encoded_face1], encoded_face2)
        return distance

    def load_reference(self, employee_id, face_detector):
        img_name = f'{employee_id}.png'
        img = cv2.imread(os.path.join(self.__path_to_references, img_name))
        if img is None:
            return
        face = face_detector.detect(img)
        face_img = crop_face(img, face[0])
        return face_img

    def __encode_face(self, face_img):
        img = cv2.resize(face_img, self.__img_size_to_encode)
        face_loc = [(0, *self.__img_size_to_encode, 0)]
        encoded = face_recognition.face_encodings(
            img, known_face_locations=face_loc)[0]
        return encoded

