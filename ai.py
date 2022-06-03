import cv2
import numpy as np
from cv2 import imread
import io
from PIL import Image

from faceRecModule import faceRec
import base64

def encode_base64(fName):
    with open(fName, 'rb') as file:
        binary_file_data = file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        return base64_encoded_data.decode('utf-8')

def decode_Base64(data):
    image = stringToImage(data)
    image = toRGB(image)
    return image

# Take in base64 string and return PIL image
def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

# convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

def faceRecognition(base64Img, dbEntries):

    currentImage = decode_Base64(base64Img)

    #decode all images from DB
    imagesFromDB = []
    for entry in dbEntries:
        img = decode_Base64(entry['image'])
        imagesFromDB.append(img)

    faceR = faceRec(imagesFromDB)
    encodeListKnown = faceR.findEncodings()

    (facesCurFrame, encodesCurFrame) = faceR.encodeFacesInImage(currentImage)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches, faceDis = faceR.compareFaces(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)  # Gesicht suchen, zu dem es am besten passt

        if matches[matchIndex]:
            # Gesicht, mit dem es am besten zusammenpasst
            return dbEntries[matchIndex]['id']

    return -1