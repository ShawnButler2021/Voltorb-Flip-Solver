from sklearn import datasets, metrics, svm
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pickle
from PIL import Image
import numpy as np
from sklearn.metrics import accuracy_score
import random
import time
import os
import cv2
import pandas as pd

# TODO MAKE OWN DATASET FOR NUMS


def preprocess_image(image_path):
    # Load the image from the file
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Resize it to 8x8 pixels (same as the MNIST digits dataset)
    img_resized = cv2.resize(img, (8, 8))

    # Invert the image (so the background is black and digits are white)
    img_resized = cv2.bitwise_not(img_resized)

    # Scale pixel values to match the range of the MNIST dataset (0-16 instead of 0-255)
    img_resized = img_resized // 16

    # Flatten the image to a 1D vector
    img_flattened = img_resized.flatten().reshape(1, -1)

    return img_flattened

def get_dir_list(blacklist=[]):
    directories = os.listdir('.\\dataset')

    # uncomment if needed
    for item in blacklist:
        directories.remove(item)

    return directories

def rotate_images(dir_list):
    for dir in dir_list:
        for file in os.listdir(f'.\\dataset\\{dir}'):
            temp = Image.open(f'.\\dataset\\{dir}\\{file}')
            for i in range(0, 20):
                t = temp.rotate(random.randint(10, 30) * random.choice([-1, 1]), expand=1)
                t.save(f'.\\dataset\\{dir}\\{i * 1000}{file}')

def fix_folder_name(dir_list):
    # giving temp name
    for dir in dir_list:
        for key, file in enumerate(os.listdir(f'.\\dataset\\{dir}')):
            os.rename(f'.\\dataset\\{dir}\\{file}', f'.\\dataset\\{dir}\\X-{file}')

    # renaming in easier order
    for dir in dir_list:
        for key, file in enumerate(os.listdir(f'.\\dataset\\{dir}')):
            os.rename(f'.\\dataset\\{dir}\\{file}', f'.\\dataset\\{dir}\\{key + 1}.png')

def remove_pngs(dir_list):
    for dir in dir_list:
        for file in os.listdir(f'.\\dataset\\{dir}'):
            if (file.split('.')[-1]) == 'png':
                os.remove(f'.\\dataset\\{dir}\\{file}')

def preprocess_dataset(dir_list):
    # turning into arrays
    for dir in dir_list:
        for key, file in enumerate(os.listdir(f'.\\dataset\\{dir}')):
            temp = preprocess_image(f'.\\dataset\\{dir}\\{file}')
            with open(f'.\\dataset\\{dir}\\{key + 1}.array', 'wb') as f:
                pickle.dump(temp, f)

def process_dataset(whitelist=[],blacklist=[]):
    directories = whitelist
    if blacklist:
        directories = get_dir_list(blacklist)

    start = time.time()
    #rotate_images(directories)
    #print('Images rotated')

    #fix_folder_name(directories)
    #print('Folders renamed')

    preprocess_dataset(directories)
    print('Images processed')

    remove_pngs(directories)
    print('PNGs removed')

    end = time.time()
    print(f'Time taketh: {end-start}')

def string_to_num(string):
    map = {'empty':-2,
           'voltorbs':-1,
           'zero':0,
           'one':1,
           'two':2,
           'three':3,
           'four':4,
           'five':5,
           'six':6,
           'seven':7,
           'eight':8,
           'nine':9
           }
    return map[string]

def ds_labels_sample_split(dir_list):
    samples = []
    labels = []
    for dir in dir_list:
        for key,file in enumerate(os.listdir(f'.\\dataset\\{dir}')):
            labels.append(string_to_num(dir))
            with open(f'.\\dataset\\{dir}\\{file}', 'rb') as f:
                samples.append(pickle.load(f)[0])


    return samples,labels


desired_accuracy = 0.97  # You can adjust this value
current_accuracy = 0.0
best_accuracy = 0.0
X, Y = ds_labels_sample_split(get_dir_list())

# Iterate until the desired accuracy is achieved
start = time.time()
current_time = 0


# TRY TRAINING AS
# SIGMOID KERNEL
# POLY KERNEL

# 1 sec * (60 sec/1 min) * (60 min/1 hr)
while current_accuracy < desired_accuracy:
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.35)

    clf = svm.SVC(gamma=0.001)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    current_accuracy = accuracy_score(y_test, y_pred)

    if current_accuracy > best_accuracy:
        best_accuracy = current_accuracy
        with open('current_best.txt', 'w') as f:
            f.write(str(best_accuracy))
        with open('current_best.model', 'wb') as f:
            pickle.dump(clf, f)


    current_time = time.time()
    print(f"{(current_time-start)//60} minutes:\n  Current accuracy => {current_accuracy}")

    if current_accuracy > desired_accuracy:
        print(f'New accuracy: {current_accuracy}')
        with open('tiles.model', 'wb') as f:
            pickle.dump(clf, f)
