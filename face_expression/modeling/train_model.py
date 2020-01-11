import os
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.layers import Conv2D, MaxPooling2D, Flatten, Input, Dense
from keras.models import model_from_json


def count_images(partition, path):
    print(partition)
    assert partition == "train" or partition == "valid" or partition == "test"
    if partition == "test":
        return len(os.listdir(path + partition))
    else:
        n_images = 0
        for category in os.listdir(path + partition):
            images_names = os.listdir(path + partition + "/" + category)
            n_images += len(images_names)
        return n_images


def save_model(model_to_save, json_model, weights):
    # serialize model to JSON
    model_json = model_to_save.to_json()
    with open(json_model, "w") as json_file:
        json_file.write(model_json)

    # serialize weights to HDF5
    model_to_save.save_weights(weights)
    print("Saved model to disk")
    return


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


path_data = "/storage/scratch2/gm0234/face_expression/faces_dataset"
categories = ['anger', 'joy', 'disgust', 'sadness', 'contempt', 'surprise', 'neutral', 'fear']

n_train_images = count_images(partition="train", path=path_data)
n_valid_images = count_images(partition="valid", path=path_data)
n_test_images = count_images(partition="test", path=path_data)

BATCH_SIZE = 32
EPOCHS = 1

train_steps = n_train_images // BATCH_SIZE
valid_steps = n_valid_images // BATCH_SIZE
test_steps = n_test_images // BATCH_SIZE


train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

valid_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        path_data + "train",
        target_size=(150, 150),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        classes=categories)

validation_generator = valid_datagen.flow_from_directory(
        path_data + "valid",
        target_size=(150, 150),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        classes=categories)

class_index = train_generator.class_indices
index_class = {ind : cls for ind, cls in class_index.items()}

input = Input(shape=(150, 150, 3), name='input')

layer = Conv2D(32, (3, 3), activation='relu')(input)
layer = MaxPooling2D(pool_size=(2, 2))(layer)

# layer = Conv2D(32, (3, 3), activation='relu')(layer)
# layer = MaxPooling2D(pool_size=(2, 2))(layer)
#
# layer = Conv2D(64, (3, 3), activation='relu')(layer)
# layer = MaxPooling2D(pool_size=(2, 2))(layer)

layer = Flatten()(layer)  # this converts our 3D feature maps to 1D feature vectors
output = Dense(8, activation="softmax")(layer)

model = Model(inputs=input, outputs=output)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print(model.summary())


history = model.fit_generator(
                            train_generator,
                            steps_per_epoch=2,
                            epochs=EPOCHS,
                            validation_data=validation_generator,
                            validation_steps=2)

# save model
save_model(model_to_save=model,
           json_model="architecture_model_face_expression.json",
           weights="weights_model_face_expression.h5")

## save model, write inference, write training as a process


print("Done")