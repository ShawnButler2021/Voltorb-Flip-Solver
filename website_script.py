from selenium import webdriver
from generate_map import generate_map
from PIL import Image
import time
import pyautogui as pyg
import cv2
import numpy as np

color_approval_list = (
    (44, 22, 17),  # dark red
    (38, 20, 44),  # dark purple
    (14, 33, 14),  # dark green
    (11, 29, 49),  # dark blue
    (46, 32, 13)  # brown
)
color_removal_list = (
    (191, 101, 221),  # purple
    (69, 167, 70),  # green
    (222, 112, 85),  # red
    (55, 146, 245),  # blue
    (230, 159, 67),  # yellow
    (224, 112, 80),  # voltorb red
    (224, 111, 79),
    (64, 63, 65),  # voltorb grey
    (66, 64, 63),
    (64, 64, 64),
    (255, 255, 255),  # voltorb white
    (254, 253, 252)
)

def open_site(driver):
    driver.get('https://voltorbflip.brandon-stein.com/')
    time.sleep(2)

def image_transformation(img, pixels=50):
    # making image easier to work with
    #data = cv2.resize(np.array(img), (16 * pixels, 9 * pixels))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGRA)

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

def mapping_site(map):
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

#https://www.tutorialspoint.com/python_pillow/python_pillow_change_color_by_changing_pixel_values.html
def color_removal(img, rgb):
    pixels = list(img.getdata())
    modified_pixels = [pixel for pixel in pixels if pixel != rgb]

    temp = Image.new('RGB', img.size)
    temp.putdata(modified_pixels)

    return temp

def list_of_colors_removal(img, list_of_rgbs):
    pixels = list(img.getdata())
    modified_pixels = [pixel for pixel in pixels if pixel not in list_of_rgbs ]

    temp = Image.new('RGB', img.size)
    temp.putdata(modified_pixels)

    return temp


def color_approval(img, rgb_list):
    pixels = list(img.getdata())
    modified_pixels = [(0,0,0) if tuple(pixel) in rgb_list else (255,255,255) for pixel in pixels]

    temp = Image.new('RGB', img.size)
    temp.putdata(modified_pixels)

    return temp



def preprocess_image(image, margin, rgb):
    #if type(image) != type(PIL.Image.Image):
    #    print(f'Image isn\'t PIL image')
    #    return
    width, height = image.size
    left = width / 8 + margin
    top = height / 8 + margin
    right = width * 7 / 8 - margin
    bottom = height * 7 / 8 - margin
    image = image.crop((left, top, right, bottom))

    return color_removal(image, rgb)

def preprocess_label(image):
    pixels = list(image.getdata())
    modified_pixels = [(0,0,0) if pixel == (44,22,17) else pixel for pixel in pixels]
    modified_pixels = [pixel for pixel in modified_pixels if pixel != (255,255,255)]

    temp = Image.new('RGB', image.size)
    temp.putdata(modified_pixels)
    return image

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

def split_label(label):
    # syncing labels to matrix
    width, height = label.size
    left = int(width / 2)
    right = width
    top = int(height / 2)
    bottom = height

    voltorb_count = label.crop((left, top, right, bottom))
    voltorb_count = list_of_colors_removal(voltorb_count,color_removal_list)
    

    return voltorb_count



if __name__ == '__main__':
    with webdriver.Firefox() as firefox:
        open_site(firefox)
        time.sleep(1)
        image = pyg.screenshot()
        work_map = generate_map()

        starting_map = list(pyg.locate('map.png', image, confidence=0.7))
        boxes, img_map = mapping_site(starting_map)

        work_map = syncing_tiles_to_matrix(img_map,work_map)

        # syncing labels to matrix
        label = preprocess_label(img_map[-1][0])
        label = color_approval(label, ((44, 22, 17),(38,20,44)))
        width, height = label.size

        #voltorb_count = split_label(label)




        left = int(width * 1/5)
        right = int(width * 3/5)
        top = 0
        bottom = int(height / 2)

        point_count_left = color_approval(label.crop((left,top,right,bottom)), (44,22,17))

        left = int(width * 3 / 5)
        right = width
        top = 0
        bottom = int(height / 2)

        #point_count_right = preprocess_label(color_approval(label.crop((left, top, right, bottom)), (44, 22, 17)))
        '''
        #label.show()
        #preprocess_label(point_count_left).show()
        #point_count_right.show()
        #voltorb_count.show()
        for y, row in enumerate(img_map[:-1]):
            label = preprocess_label(row[-1])
            #label = list_of_colors_removal(label, color_removal_list)
            label.show()
            voltorb_count = split_label(label)
            voltorb_count.show()
            # crop label (row[-1]) into 3 segments
            # cast img_diff => string
            # appropriately combine and apply labels
        for x, label in enumerate(img_map[-1]):
            pass
            # crop labels into 3 segments
            # cast img_diff => string
            # appropriately combine and apply labels








        # marking map
        for row in work_map:
            print(row)

        image = image_transformation(image)
        cv2.rectangle(image, (starting_map[0],starting_map[1]), (starting_map[0]+starting_map[2],starting_map[1]+starting_map[3]), (0,0,255), 4)
        '''
        '''
        for c in boxes:
            cv2.rectangle(image, (c[0],c[1]), (c[0]+column_width,c[1]+row_height), (0,255,255), 2)
        #print(matrix_map)
        #cv2.imshow('',image)
        #cv2.waitKey(0)
        '''
