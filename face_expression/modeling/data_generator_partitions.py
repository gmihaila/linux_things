import os
from sklearn.model_selection import train_test_split
import shutil

faces_path = "/storage/scratch2/gm0234/face_dataset/face_dataset/all_faces/"
path_data = "/storage/scratch2/gm0234/face_dataset/faces_dataset/"

faces_images = os.listdir(faces_path)

categories = ['anger', 'joy', 'disgust', 'sadness', 'contempt', 'surprise', 'neutral', 'fear']

if not os.path.isdir(path_data):
    os.mkdir(path_data)


def mkdir_categories(path, categories, partition):
    tmp_path = path + partition
    if partition == "test":
        if not os.path.isdir(tmp_path):
            os.mkdir(tmp_path)
        return
    tmp_path = path + partition + "/"
    if not os.path.isdir(tmp_path):
        os.mkdir(tmp_path)
    for category in categories:
        tmp_path = path + partition + "/" + category
        if not os.path.isdir(tmp_path):
            os.mkdir(tmp_path)
    return


mkdir_categories(path_data, categories, 'train')
mkdir_categories(path_data, categories, 'valid')
mkdir_categories(path_data, categories, 'test')

lables = [face_image.split("_")[0] for face_image in faces_images]

x_train, x_test, y_train, y_test = train_test_split(faces_images, lables, test_size=0.15)

x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2)

print(len(x_train), len(x_valid), len(x_test))


def copy_in_partition(images_names, partition):
    print(partition)
    assert partition == "train" or partition == "valid" or partition == "test"
    for image_name in images_names:
        source_path = faces_path + image_name
        if partition == "test":
            destination_path = path_data + partition +  "/" + image_name
        else:
            category = image_name.split("_")[0]
            destination_path = path_data + partition + "/" + category + "/" + image_name

        shutil.copyfile(source_path, destination_path)

    return


copy_in_partition(x_train, "train")
copy_in_partition(x_valid, "valid")
copy_in_partition(x_test, "test")

print("Done!")
