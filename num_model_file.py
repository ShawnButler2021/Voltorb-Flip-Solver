from sklearn import svm, neighbors, linear_model
from sklearn.model_selection import train_test_split
import pickle
from PIL import Image
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
import random
import time
import os
import cv2
import shutil
import sys

s = 1


def color_removal(img):
    pixels = list(img.getdata())
    modified_pixels = [pixel for pixel in pixels if pixel != (188,140,133)]

    temp = Image.new('RGB', img.size)
    temp.putdata(modified_pixels)

    return temp


def x_preprocess_image(image):
    #if type(image) != type(PIL.Image.Image):
    #    print(f'Image isn\'t PIL image')
    #    return
    width, height = image.size
    left = width / 8
    top = height / 8
    right = width * 7 / 8 - 5
    bottom = height * 7 / 8
    image = image.crop((left, top, right, bottom))

    return color_removal(image)

def migrate_dataset(dataset_path, new_path):
    if os.path.exists(new_path):
        print('Destination already exists. Deleting path.')
        shutil.rmtree('.\\work_dataset')
    shutil.copytree(dataset_path, new_path)

def preprocess_image(image_path):
    # Load the image from the file
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize it to 8x8 pixels (same as the MNIST digits dataset)
    #img_resized = cv2.resize(img, (8, 8))

    # Invert the image (so the background is black and digits are white)
    #img_resized = cv2.bitwise_not(img_resized)

    # Flatten the image to a 1D vector
    #img_flattened = img.flatten().reshape(-1, 1)
    print(image_path[:16])
    print(img.shape)

    return img

def rotate_images(datafield_path,num_of_additions=20,angle_range=(10,30)):
    for file in os.listdir(f'{datafield_path}'):
        temp = Image.open(f'{datafield_path}\\{file}')
        for i in range(0, num_of_additions):
            t = temp.rotate(random.randint(angle_range[0], angle_range[1]) * random.choice([-1, 1]), expand=1)
            t.save(f'{datafield_path}\\{i}-{file}')

def fix_folder_names(datafield_path):
    # giving temp name
    for key, file in enumerate(os.listdir(f'{datafield_path}')):
        os.rename(f'{datafield_path}\\{file}', f'{datafield_path}\\Y-{file}')

    # renaming in easier order
    for key, file in enumerate(os.listdir(f'{datafield_path}')):
        os.rename(f'{datafield_path}\\{file}', f'{datafield_path}\\{key + 1}.array')

def remove_pngs(datafield_path):
    for file in os.listdir(f'{datafield_path}'):
        if (file.split('.')[-1]) == 'png':
            os.remove(f'{datafield_path}\\{file}')

def preprocess_datafield(datafield_path):
    # turning into arrays
    for key, file in enumerate(os.listdir(f'{datafield_path}')):
        temp = preprocess_image(f'{datafield_path}\\{file}')
        with open(f'{datafield_path}\\{file.split('.')[0]}.array', 'wb') as f:
            pickle.dump(temp, f)


def ds_labels_sample_split(dataset_path,dir_list=[]):
    if not dir_list:
        dir_list = os.listdir(dataset_path)
    samples = []
    labels = []
    for dir in dir_list:
        for key,file in enumerate(os.listdir(f'{dataset_path}\\{dir}')):
            labels.append(dir)
            with open(f'{dataset_path}\\{dir}\\{file}', 'rb') as f:
                samples.append(pickle.load(f)[0].flatten().flatten())


    return samples, labels

def train_model(model_data={},dataset_data={}):
    if not model_data:
        print('Add model data')
        print('model_data = {')
        print('\tmodel_name=str,')
        print('\tcurrent_name=str,')
        print('\tdesired_accuracy=int,')
        print('\tmodel=model_class')
        print('}')
        return
    if not dataset_data:
        print('Add dataset data')
        print('dataset_data = {')
        print('\tdataset_path=str,')
        print('\tdir_list=list,')
        print('\ttest_size=float<1')
        print('}')
        return

    clf = model_data['model']
    start = time.time()
    current_accuracy = 0.0
    best_accuracy = 0.0
    X, Y = ds_labels_sample_split(dataset_data['dataset_path'], dir_list=dataset_data['dir_list'])

    while current_accuracy < model_data['desired_accuracy']:
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=dataset_data['test_size'])

        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        current_accuracy = f1_score(y_test, y_pred, average='micro')

        if current_accuracy > best_accuracy:
            best_accuracy = current_accuracy
            with open('current_best.txt', 'w') as f:
                f.write(str(best_accuracy))
            with open(model_data['current_name'], 'wb') as f:
                pickle.dump(clf, f)

        current_time = time.time()
        print(f"{(current_time - start) // 60} minutes:\n  Current accuracy => {current_accuracy}")

        if current_accuracy > model_data['desired_accuracy']:
            print(f'New accuracy: {current_accuracy}')
            with open(model_data['folder_path']+'\\'+model_data['model_name'], 'wb') as f:
                pickle.dump(clf, f)

def append_datafields(src,dest):
    for key, file in enumerate(os.listdir(f'{src}')):
        os.rename(f'{src}\\{file}', f'{dest}\\xyz-{file}')

# try decision trees next
data_for_model = {
    'folder_path': '.\\models',
    'model_name': 'tiles.model',
    'current_name': 'current_best.model',
    'desired_accuracy': 0.98,
    'model': svm.SVC(gamma=0.001)
}
data_for_dataset = {
    'dataset_path': '.\\work_dataset',
    'dir_list': [],
    'test_size': 0.45
}

if __name__ == '__main__':
    file_list = []
    temp = None
    for file in os.listdir(f'.\\comparison_pictures\\2'):
        temp = np.array(Image.open(f'.\\comparison_pictures\\2\\{file}'))
        file_list.append(temp.flatten())

    bool_list = []
    for key,sublist in enumerate(file_list[:-1]):
        if list(file_list[key]) == list(file_list[key+1]): bool_list.append(True)
        else: bool_list.append(False)
    print(f'2:')
    print(bool_list)
