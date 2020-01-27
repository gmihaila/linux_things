import pygame.surfarray as surfarray
import numpy as np
import pygame
import pygame.camera
import tensorflow as tf
from tensorflow.keras.models import model_from_json
import cv2

## multi thread webcam
## https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/


def load_model(json_model, weights):
    # load json and create model
    json_file = open(json_model, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights(weights)
    print("Loaded model from disk")
    return loaded_model

# classes
CLASS_NAMES = ['anger', 'joy', 'disgust', 'sadness', 'contempt', 'surprise', 'neutral', 'fear']

id_class = {0: 'anger', 1: 'joy', 2: 'disgust', 3: 'sadness', 4: 'contempt', 5: 'surprise', 6: 'neutral', 7: 'fear'}

# face detection
face_cascade = cv2.CascadeClassifier('../face_detection//haarcascade_frontalface_default.xml') 

width = 320
height = 240

# camera to be use

pygame.init()
pygame.camera.init()

cam = pygame.camera.Camera("/dev/video0", (width, height))

# prep show window
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)

# start camera to capure
cam.start()

path_model = "model_checkpoint/configuration_model.json"
path_weights = "model_checkpoint/final_epoch_model_weights.hdf5"

model = load_model(json_model=path_model,
                      weights=path_weights)

# compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print(model.summary())

"""

img = cv2.imread("download.jpeg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

print("faces detected",faces)

for (x,y,w,h) in faces:
    face_clip = img[y:y+h, x:x+w]
    new_img = cv2.resize(face_clip, (width, height))
    new_srf = pygame.surfarray.make_surface(new_img)
    window.blit(new_srf, (0, 0))
    pygame.display.update()
"""

#"""
for i in range(100):

   
    print("frame", i)

    image = cam.get_image()

    np_image = surfarray.array3d(image)
    new_image = cv2.resize(np_image, (150, 150))
    
    pred = model.predict(np.array([new_image]))
    
    label = id_class[np.argmax(pred)]

    # print("\t", pred)
    
    print("\t", label)
    
    new_srf = pygame.surfarray.make_surface(np_image)
    window.blit(new_srf, (0, 0))

    # refresh window
    pygame.display.update()


    '''
    gray = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    print(faces)

    if len(faces) > 0:
        print("\tface detected")

        (x,y,w,h)  = faces[0]
        face_clip = np_image[y:y+h, x:x+w]  #cropping the face in image
        face_clip = cv2.resize(face_clip, (width, height))
        
        new_srf = pygame.surfarray.make_surface(face_clip)
        window.blit(new_srf, (0, 0))

        # refresh window
        pygame.display.update()
    else:
        new_image = cv2.resize(np_image, (150, 150))
        pred = model.predict(np.array([new_image]))
        print("\t", pred)
        new_srf = pygame.surfarray.make_surface(np_image)
        window.blit(new_srf, (0, 0))

        # refresh window
        pygame.display.update()

    '''

#"""

# stop camera
cam.stop()
