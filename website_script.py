from selenium import webdriver
from generate_map import generate_map
import PIL
from PIL import Image, ImageOps
import time
import pyautogui as pyg
import cv2
import numpy as np

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
    img2 = list(np.array(img2).flatten())

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

#https://www.tutorialspoint.com/python_pillow/python_pillow_change_color_by_changing_pixel_values.htm
def color_filter(img):
    pixels = list(img.getdata())
    modified_pixels = [(10,10,10) if pixel == (188,140,133) else pixel for pixel in pixels ]

    temp = Image.new('RGB', img.size)
    temp.putdata(modified_pixels)

    return temp

def color_removal(img):
    pixels = list(img.getdata())
    modified_pixels = [pixel for pixel in pixels if pixel != (188,140,133)]

    temp = Image.new('RGB', img.size)
    temp.putdata(modified_pixels)

    return temp


def preprocess_image(image, margin=5):
    #if type(image) != type(PIL.Image.Image):
    #    print(f'Image isn\'t PIL image')
    #    return
    width, height = image.size
    left = width / 8 + margin
    top = height / 8 + margin
    right = width * 7 / 8 - margin
    bottom = height * 7 / 8 - margin
    image = image.crop((left, top, right, bottom))

    return color_removal(image)



if __name__ == '__main__':
    with webdriver.Firefox() as firefox:
        open_site(firefox)
        time.sleep(6)
        image = pyg.screenshot()
        work_map = generate_map()

        map = list(pyg.locate('map.png', image, confidence=0.7))
        boxes, img_map = mapping_site()



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
        for y, row in enumerate(img_map[:-1]):
            for x, tile in enumerate(row[:-1]):
                tile = preprocess_image(tile)

                temp_dict[0] = img_diff(tile,point_map[0])
                temp_dict[1] = img_diff(tile,point_map[1])
                temp_dict[2] = img_diff(tile,point_map[2])
                temp_dict[3] = img_diff(tile,point_map[3])
                if temp_dict[0] < 1000: work_map[y][x] = 0
                elif temp_dict[1] < 1000: work_map[y][x] = 1
                elif temp_dict[2] < 1000: work_map[y][x] = 2
                elif temp_dict[3] < 1000: work_map[y][x] = 3
                else: work_map[y][x] = -1






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
