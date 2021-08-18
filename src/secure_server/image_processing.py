import cv2


def draw_face(image, face_coords):
    x1, y1, x2, y2 = face_coords
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)


def crop_face(image, face_coords):
    x1, y1, x2, y2 = face_coords
    face_img = image[y1:y2, x1:x2]
    return face_img
