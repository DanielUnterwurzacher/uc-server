import cv2
import numpy as np
import face_recognition
import os

class faceRec():

    def __init__(self, imgList):
        self.images = []

        for img in imgList:
            self.images.append(img)

    def findEncodings(self):
        encodeListKnown = []
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeListKnown.append(encode)
        return encodeListKnown

    def encodeFacesInImage(self, imgS):
        facesCurFrame = face_recognition.face_locations(imgS)  # alle Gesichter im Bild erkennen
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)  # alle Gesichter im Bild encoden
        return (facesCurFrame, encodesCurFrame)

    def compareFaces(self, encodeListKnown, encodeFace):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)  # Gesichter mit den Bekannten vergleichen
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        return (matches, faceDis)



