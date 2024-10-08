from selenium import webdriver
from generate_map import generate_map
from PIL import Image, ImageOps
import time
import pyautogui as pyg
import cv2
import numpy as np
import sys
from sklearn import svm
import pickle

def open_site(driver):
    driver.get('https://voltorbflip.brandon-stein.com/')
    time.sleep(2)

def image_transformation(img, pixels=50):
    # making image easier to work with
    #data = cv2.resize(np.array(img), (16 * pixels, 9 * pixels))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGRA)

def array_diff(img1, img2):
    img1 = img1.resize((100,100))
    img1 = list(np.array(img1).flatten())
    img2 = img2.resize((100,100))
    img2 = np.array(img2).flatten()

    img1.extend([0] * (len(img2)-len(img1)))
    img1 = np.array(img1)

    diff = img1 - img2

    return abs(np.sum(diff))

def img_diff(img1,img2):
    img1 = img1.resize((100, 100))
    img1 = list(np.array(img1).flatten())
    img2 = img2.resize((100, 100))
    img2 = list(np.array(img2).flatten())

    img1.extend([0] * (len(img2) - len(img1)))
    img1 = np.array(img1,dtype=np.uint8)
    img2 = np.array(img2,dtype=np.uint8)
    diff = cv2.subtract(img1, img2)

    return abs(np.sum(diff))

def mapping_site():
    # mapping values
    left_margin = 15
    top_margin = 15
    spacing = 2

    new_map_left = map[0] + left_margin
    new_map_top = map[1] + top_margin

    new_map_width = map[2] - left_margin * 2
    new_map_height = map[3] - top_margin * 2
    column_width = int(new_map_width / 6)
    row_height = int(new_map_height / 6)

    # getting centers of
    # all tiles and labels
    boxes = []
    tiles = []
    for column in range(0, 6):
        img_row = []
        for row in range(0, 6):
            if column == 5 and row == 5: break
            x = int(new_map_left + row * column_width + row * spacing)
            y = int(new_map_top + column * row_height + column * spacing)
            boxes.append((x, y))
            img_row.append(pyg.screenshot(region=(x, y, column_width, row_height)))
        tiles.append(img_row)

    return boxes, tiles

def is_value(x,y,needle,haystack,conf=0.4):
    try:
        pyg.locate(needle, haystack, confidence=conf)
        return True
    except pyg.ImageNotFoundException:
        return False

def preprocess_image(image):
    # Load the image from the file
    #img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    img = np.array(ImageOps.grayscale(image))

    # Resize it to 8x8 pixels (same as the MNIST digits dataset)
    img_resized = cv2.resize(img, (8, 8))

    # Invert the image (so the background is black and digits are white)
    img_resized = cv2.bitwise_not(img_resized)

    # Scale pixel values to match the range of the MNIST dataset (0-16 instead of 0-255)
    img_resized = img_resized // 16

    # Flatten the image to a 1D vector
    img_flattened = img_resized.flatten().reshape(1, -1)

    return img_flattened


if __name__ == '__main__':
    with webdriver.Firefox() as firefox:
        open_site(firefox)
        time.sleep(6)
        image = pyg.screenshot()
        work_map = generate_map()

        map = list(pyg.locate('comparison-pictures\\map.png', image, confidence=0.7))
        #print('(left,top,width,height)', map)

        boxes, img_map = mapping_site()


        # TODO train svm to get numbers
        tile_clf = None
        with open('tiles.model','rb') as f:
            tile_clf = pickle.load(f)

        print(type(tile_clf))
        for y, row in enumerate(img_map):
            for x, tile in enumerate(row):
                print(f'{x},{y} =>',tile_clf.predict(preprocess_image(tile)))


        # marking map
        for row in work_map:
            print(row)

        image = image_transformation(image)
        cv2.rectangle(image, (map[0],map[1]), (map[0]+map[2],map[1]+map[3]), (0,0,255), 4)
        '''for c in boxes:
            cv2.rectangle(image, (c[0],c[1]), (c[0]+column_width,c[1]+row_height), (0,255,255), 2)'''
        #print(matrix_map)
        cv2.imshow('',image)
        cv2.waitKey(0)
