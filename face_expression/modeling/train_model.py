#!/usr/bin/env
from __future__ import absolute_import, division, print_function, unicode_literals
import os
os.environ["CUDA_VISIBLE_DEVICES"]="0"
import tensorflow as tf
import pathlib
import mlflow
import numpy as np

# model train
EPOCHS = 10
BATCH = 50

# model compile
OPTIMIZER = 'adam'
LOSS = 'categorical_crossentropy'
METRICS = ['accuracy']

# parameters
CLASS_NAMES = ['anger', 'joy', 'disgust', 'sadness', 'contempt', 'surprise', 'neutral', 'fear']
IMG_WIDTH = 150
IMG_HEIGHT = 150


# load the files as a tf.data.Dataset
def get_label(file_path):
    # convert the path to a list of path components
    parts = tf.strings.split(file_path, os.path.sep)
    # The second to last is the class-directory
    return parts[-2] == CLASS_NAMES


def decode_img(img):
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=3)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    return tf.image.resize(img, [IMG_WIDTH, IMG_HEIGHT])


def process_path(file_path):
    label = get_label(file_path)
    # load the raw data from the file as a string
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img, label


def prepare_for_training(ds, cache=True, shuffle_buffer_size=1000):
    # This is a small dataset, only load it once, and keep it in memory.
    # use `.cache(filename)` to cache preprocessing work for datasets that don't
    # fit in memory.
    if cache:
        if isinstance(cache, str):
            ds = ds.cache(cache)
        else:
            ds = ds.cache()

    ds = ds.shuffle(buffer_size=shuffle_buffer_size)

    # Repeat forever
    ds = ds.repeat()

    ds = ds.batch(BATCH)

    # `prefetch` lets the dataset fetch batches in the background while the model
    # is training.
    ds = ds.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

    return ds


def tf_data_generator(path, cache=True):
    data_dir = pathlib.Path(path)
    list_ds = tf.data.Dataset.list_files(str(data_dir / '*/*'))

    # Set `num_parallel_calls` so multiple images are loaded/processed in parallel.
    labeled_ds = list_ds.map(process_path, num_parallel_calls=tf.data.experimental.AUTOTUNE)

    train_ds = prepare_for_training(labeled_ds, cache)

    return train_ds


def mlflow_model_summary(my_model, path='model_summary.txt'):
    # show model setup in artifacts
    with open(path, 'w') as fh:
        # Pass the file handle in as a lambda function to make it callable
        my_model.summary(print_fn=lambda x: fh.write(x + '\n'))
    mlflow.log_artifact(path)
    return


class MlflowCallBacks(tf.keras.callbacks.Callback):

    # initialize additional variables
    def __init__(self):
        self.checkpoint_path = "model_checkpoint/"
        # set path
        if not os.path.isdir(self.checkpoint_path):
            os.mkdir(self.checkpoint_path)
        self.config_path = self.checkpoint_path + "configuration_model.json"

    def on_train_begin(self, logs=None):
        # save model configuration
        model_json = self.model.to_json()
        with open(self.config_path, "w") as json_file:
            json_file.write(model_json)
        # log file to mlflow
        mlflow.log_artifact(local_path=self.checkpoint_path)
        mlflow.set_tag("Current epoch", 0)
        return

    def on_train_end(self, logs=None):
        # serialize weights to HDF5
        self.model.save_weights(self.checkpoint_path + "final_epoch_model_weights.hdf5")
        # log file to mlflow
        mlflow.log_artifact(local_path=self.checkpoint_path)
        mlflow.set_tag("Current epoch", "Done!")
        return

    def on_epoch_end(self, epoch, logs={}):
        offset_epoch = epoch + 1
        # log each metric to mlflow
        [mlflow.log_metric(key=name, value=value, step=offset_epoch) for name, value in logs.items()]
        # save weights at each epoch
        tmp_path = self.checkpoint_path + str(offset_epoch) + "_epoch_model_weights.hdf5"
        self.model.save_weights(tmp_path)
        # log file to mlflow
        mlflow.log_artifact(local_path=self.checkpoint_path)
        mlflow.set_tag("Current epoch", offset_epoch)
        return


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


def load_model(json_model, weights):
    # load json and create model
    json_file = open(json_model, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = tf.keras.model.model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights(weights)
    print("Loaded model from disk")
    return loaded_model


# PATHS SETUP
path_data = "../faces_dataset/"
path_train = "../faces_dataset/train/"
path_valid = "../faces_dataset/valid/"

# COUNTS DEFINITION
n_train_images = count_images(partition="train", path=path_data)
n_valid_images = count_images(partition="valid", path=path_data)
n_test_images = count_images(partition="test", path=path_data)

# DATA GENERATORS
train_generator = tf_data_generator(path_train)
train_steps = np.ceil(n_train_images/BATCH)
print("Found train: ", n_train_images)

validation_generator = tf_data_generator(path_valid)
valid_steps = np.ceil(n_valid_images/BATCH)
print("Found dev:   ", n_valid_images)


# BUILD MODEL
input_layer = tf.keras.layers.Input(shape=(150, 150, 3), name='input')
layer = tf.keras.layers.Conv2D(32, (3, 3), activation='relu')(input_layer)
layer = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(layer)

# layer = Conv2D(32, (3, 3), activation='relu')(layer)
# layer = MaxPooling2D(pool_size=(2, 2))(layer)
#
# layer = Conv2D(64, (3, 3), activation='relu')(layer)
# layer = MaxPooling2D(pool_size=(2, 2))(layer)

layer = tf.keras.layers.Flatten()(layer)  # this converts our 3D feature maps to 1D feature vectors
output = tf.keras.layers.Dense(8, activation="softmax")(layer)

model = tf.keras.Model(inputs=input_layer, outputs=output)
model.compile(loss=LOSS, optimizer=OPTIMIZER, metrics=METRICS)

print(model.summary())

# MLFLOW LOGS AND TRAIN MODEL
with mlflow.start_run(run_name="small_model"):
    mlflow_model_summary(my_model=model,
                         path='model_summary.txt')
    # log tag
    mlflow.set_tag("module", "tensorflow/2.1.0-gpu")
    mlflow.set_tag("type", "development")

    # log parameters
    mlflow.log_param("epochs", EPOCHS)
    mlflow.log_param("batch", BATCH)
    mlflow.log_param("optimizer", OPTIMIZER)
    mlflow.log_param("loss", LOSS)
    mlflow.log_param("n_train_images", n_train_images)
    mlflow.log_param("n_valid_images", n_valid_images)
    # mlflow.log_param("n_test_images", n_test_images) # only when testing

    # log artifacts
    mlflow.log_artifact("train_model.py")
    mlflow_model_summary(my_model=model)

    # train model with callbacks
    model.fit(
        train_generator,
        steps_per_epoch=train_steps,
        epochs=EPOCHS,
        validation_data=validation_generator,
        validation_steps=valid_steps,
        callbacks=[MlflowCallBacks()])




print("\nFinished!")
