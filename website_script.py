from selenium import webdriver
from generate_map import generate_map
from PIL import Image
import time
import pyautogui as pyg
import cv2
import numpy as np
import pickle
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import random




def open_site(driver):
    driver.get('https://voltorbflip.brandon-stein.com/')
    time.sleep(2)

def mapping_site(map, left_margin=15, top_margin=15, spacing=2):
    # mapping values
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
            boxes.append((x, y, column_width, row_height))
            img_row.append(pyg.screenshot(region=(x, y, column_width, row_height)))
        tiles.append(img_row)

    temp_box = []
    temp_row = []
    index = 0
    for item in boxes:
        if index < 5: temp_row.append(item)
        index += 1

        if index > 5: 
            index = 0
            temp_box.append(temp_row)


    return boxes, tiles

def get_map():
    environment = pyg.screenshot()
    starting_map = list(pyg.locate('map.png', environment, confidence=0.7))
    bounding_boxes, map_of_images = mapping_site(starting_map)

    return bounding_boxes, map_of_images, environment

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

#https://www.tutorialspoint.com/python_pillow/python_pillow_change_color_by_changing_pixel_values.html
def color_removal(img, rgb):
    pixels = list(img.getdata())
    modified_pixels = [pixel for pixel in pixels if pixel != rgb]

    temp = Image.new('RGB', img.size)
    temp.putdata(modified_pixels)

    return temp

def list_of_colors_approval(img, rgb_list):
    pixels = list(img.getdata())
    modified_pixels = [(255,255,255) if pixel not in rgb_list else (0,0,0) for pixel in pixels ]

    temp = Image.new('RGB', img.size)
    temp.putdata(modified_pixels)

    return temp

def preprocess_image(image, margin, rgb):
    width, height = image.size
    left = width / 8 + margin
    top = height / 8 + margin
    right = width * 7 / 8 - margin
    bottom = height * 7 / 8 - margin
    image = image.crop((left, top, right, bottom))

    return color_removal(image, rgb)

def syncing_tiles_to_matrix(img_env,work_env):
    point_map = {
        1: Image.open(f'.\\comparison_pictures\\1.png'),
        2: Image.open(f'.\\comparison_pictures\\2.png'),
        3: Image.open(f'.\\comparison_pictures\\3.png'),
        0: Image.open(f'.\\comparison_pictures\\0.png')
    }
    temp_dict = {
        0: None,
        1: None,
        2: None,
        3: None,

    }
    for y, row in enumerate(img_env[:-1]):
        for x, tile in enumerate(row[:-1]):
            tile = preprocess_image(tile, 5, (188,140,133))

            temp_dict[0] = img_diff(tile, point_map[0])
            temp_dict[1] = img_diff(tile, point_map[1])
            temp_dict[2] = img_diff(tile, point_map[2])
            temp_dict[3] = img_diff(tile, point_map[3])
            if temp_dict[0] < 1000:
                work_env[y][x] = 0
            elif temp_dict[1] < 1000:
                work_env[y][x] = 1
            elif temp_dict[2] < 1000:
                work_env[y][x] = 2
            elif temp_dict[3] < 1000:
                work_env[y][x] = 3
            else:
                work_env[y][x] = -1
    return work_env

# label series
def get_labels(environment):
    vertical_labels = [row[-1] for row in environment[:-1]]
    horizontal_labels = [image for image in environment[-1]]

    approval_list = (
        (38,20,44), # purple
        (46,32,13), # yellow
        (14,33,14), # green
        (44,22,17), # red
        (11,29,49)  # blue
    )

    for index, image in enumerate(vertical_labels):
        vertical_labels[index] = list_of_colors_approval(image,approval_list)

    for index, image in enumerate(horizontal_labels):
        horizontal_labels[index] = list_of_colors_approval(image, approval_list)

    return vertical_labels, horizontal_labels

def predict_label(model, image):
    image_array = img_to_array(image.resize((30,30))) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    prediction = model.predict(image_array)
    return np.argmax(prediction, axis=1)

def split_vertical_label(label):
    width, height = label.size

    left = width // 2 - 10
    right = width * 7 // 10
    top = 0
    bottom = height // 2 - 10
    left_point = label.crop((left, top, right, bottom))


    left = width * 7 // 10
    right = width
    top = 0
    bottom = height // 2 - 10
    right_point = label.crop((left, top, right, bottom))


    left = width * 7 // 10
    right = width
    top = height // 2 - 10
    bottom = height - 10
    voltorb = label.crop((left, top, right, bottom))


    return left_point, right_point, voltorb

def split_horizontal_label(label):
    width, height = label.size

    left = width * 3 // 10
    right = width * 6 // 10
    top = 0
    bottom = height // 2
    left_point = label.crop((left, top, right, bottom))


    left = width * 6 // 10
    right = width
    top = 0
    bottom = height // 2
    right_point = label.crop((left, top, right, bottom))


    left = width // 2
    right = width
    top = height // 2
    bottom = height
    voltorb = label.crop((left, top, right, bottom))


    return left_point, right_point, voltorb

def copy_map(map, model):
    work_map = generate_map()
    work_map = syncing_tiles_to_matrix(map,work_map)

    v_labels, h_labels = get_labels(map)

    # adding labels to the workmap
    for x, label in enumerate(h_labels):
        left, right, voltorb = split_horizontal_label(label)

        
        left = str(predict_label(model, left)[0])
        if left != '1' or left != '0':      # heuristic for handling false positives
            left = random.choices(['0','1'], weights=[7,3])[0]

        right = str(predict_label(model, right)[0])
        points = int(left+right)
        if points > 12:         # heuristic for handling false positives
            points -= 10

        voltorb = int(predict_label(model, voltorb)[0])
        if voltorb not in [0,1,2,3,4,5]:    # heuristic for handling false positives
            print(x,voltorb)
            voltorb = random.choices([0,1,2,3,4,5], weights=[1,1,2,3,2,1])[0]

        work_map[-1][x] = (voltorb, points)

    
    for y, label in enumerate(v_labels):
        left, right, voltorb = split_vertical_label(label)
        left = str(predict_label(model, left)[0])
        right = str(predict_label(model, right)[0])
        points = int(left+right)
        voltorb = int(predict_label(model, voltorb)[0])

        work_map[y][-1] = (voltorb, points)

    return work_map

if __name__ == '__main__':
    boxes, img_map, env = None, None, None
    with webdriver.Firefox() as firefox:
        open_site(firefox)
        time.sleep(1)
        boxes, img_map, env = get_map()


    env.show('Map')
    digits_model = load_model('digits.keras')

    w_map = copy_map(img_map, digits_model)

    # marking map
    #env.show()
    for row in w_map:
        print(row)
    
