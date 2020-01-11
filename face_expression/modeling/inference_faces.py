import keras
from keras.models import model_from_json

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


path_model = "/storage/scratch2/gm0234/face_expression/modeling/architecture_model_face_expression.json"
path_weights = "/storage/scratch2/gm0234/face_expression/modeling/weights_model_face_expression.h5"

model = load_model(json_model=path_model,
                      weights=path_weights)

# compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print(model.summary())


# initialize the camera
