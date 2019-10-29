import cv2
from matplotlib import pyplot as plt
import numpy as np


def get_relevant_image(image_path):
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img_face = extract_face(img_gray)
    img_face = cv2.resize(img_face, (96, 96))
    img_face = img_face.reshape((96, 96, 1))
    return img_face


def extract_face(img_grey):
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Detect faces
    faces = face_cascade.detectMultiScale(img_grey, 1.1, 4)
    for (x, y, w, h) in faces:
        return img_grey[y:y + h, x:x + w]


def show_relevant_image(img):
    img = img.reshape((96, 96))
    plt.imshow(img, cmap='gray')
    plt.show()

def save_image(img, path):
    cv2.imwrite(path, img)

def load_image(path):
    img_gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img_gray
