import os
from enum import Enum
from cv2 import imwrite

from src.secure_server import image_processing
from src.secure_server.face_processing import FaceMatcher, FaceDetector
from src.logger import server_logger


class IdentificationStatus(Enum):
    successful = 'Пользователь [{}] успешно идентифицирован'
    wrong_person_in_frame = 'Другой человек в кадре'
    too_much_persons = 'Больше одного лица в кадре'
    no_person_in_frame = 'Нет лица в кадре'
    no_id_in_database = 'Идентификационный номер [{}] отсутствует в БД'


class IdentificationHandler:
    def __init__(self, identification_thrashold, path_to_staff_faces, dir_to_save_photos):
        self.__ident_thrashold = identification_thrashold
        self.__face_matcher = FaceMatcher(path_to_staff_faces)
        self.__face_detector = FaceDetector()
        self.__image_saver = ImageSaver()
        self.__dir_to_save_photos = dir_to_save_photos

    def identificate(self, image, employee_id):
        server_logger.info('Start identification')
        confidence = '-'
        detected_faces = self.__face_detector.detect(image)
        if len(detected_faces) == 1:
            status, msg, subdir_to_save, confidence = self.__process_single_face_photo(
                image, detected_faces, employee_id
            )
        else:
            status, subdir_to_save = 'unsuccessful', 'unsuccessful'
            msg = self.__process_wrong_photo(len(detected_faces))

        server_logger.info(
            f'Identification completed - STATUS: {status} - COINCIDENCE_CONFIDENCE: {confidence}% - MSG: {msg}')

        full_path_to_save = os.path.join(
            self.__dir_to_save_photos, subdir_to_save)

        fname_to_save = self.__image_saver.get_fname_to_save(full_path_to_save)
        self.__image_saver.save_image(image, full_path_to_save, fname_to_save)
        server_logger.info(f'Saved photo as {full_path_to_save}')

        response = dict(
            response=dict(status=status,
                          msg=msg, 
                          filename=fname_to_save,
                          coincidence_confidence=confidence)
        )
        return response

    def __process_single_face_photo(self, image, detected_faces, employee_id):
        status = 'unsuccessful'
        subdir_to_save = 'unsuccessful'

        reference = self.__face_matcher.load_reference(employee_id,
                                                       self.__face_detector)
        if reference is None:
            status = 'unsuccessful'
            msg = IdentificationStatus.no_id_in_database.value.format(employee_id)
        else:
            match_result = self.__match_faces(
                image, detected_faces[0], reference)
            if match_result >= self.__ident_thrashold:
                status = 'successful'
                subdir_to_save = 'successful'
                msg = IdentificationStatus.successful.value.format(employee_id)
            else:
                msg = IdentificationStatus.wrong_person_in_frame.value
        return status, msg, subdir_to_save, round(match_result[0]*100)

    def __process_wrong_photo(self, num_of_faces):
        if not num_of_faces:
            msg = IdentificationStatus.no_person_in_frame.value
        else:
            msg = IdentificationStatus.too_much_persons.value
        return msg

    def __match_faces(self, image, face, reference):
        face_to_match = image_processing.crop_face(image, face)
        match_result = self.__face_matcher.compare_faces(
            reference, face_to_match
        )
        return match_result


class ImageSaver:
    def save_image(self, image, dir_to_save, fname_to_save):
        path_to_save = os.path.join(dir_to_save, fname_to_save)
        imwrite(path_to_save, image)

    def get_fname_to_save(self, dir_to_save):
        files_in_dir = os.listdir(dir_to_save)
        max_id = 0
        for fname in files_in_dir:
            ident_id = int(fname.split('.')[0])
            if ident_id > max_id:
                max_id = ident_id
        fname_to_save = f'{max_id + 1}.png'
        return fname_to_save
