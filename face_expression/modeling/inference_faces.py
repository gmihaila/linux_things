import pygame.surfarray as surfarray
import numpy as np
import pygame
import pygame.camera
import tensorflow as tf
from tensorflow.keras.models import model_from_json

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

path_model = "architecture_model_face_expression.json"
path_weights = "weights_model_face_expression.h5"

model = load_model(json_model=path_model,
                      weights=path_weights)

# compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print(model.summary())

image = cam.get_image()

print(type(image))

print(image)

image = surfarray.array3d(image)
print(image.shape)

print(type(image))
# stop camera
cam.stop()
