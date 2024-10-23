from selenium import webdriver
from generate_map import generate_map
from PIL import Image
import time
import pyautogui as pyg
import cv2
import numpy as np




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
            boxes.append((x, y))
            img_row.append(pyg.screenshot(region=(x, y, column_width, row_height)))
        tiles.append(img_row)

    return boxes, tiles

def get_site(wait_time):
    with webdriver.Firefox() as firefox:
        open_site(firefox)
        time.sleep(wait_time)
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

def preprocess_image(image, margin, rgb):
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

# label series



if __name__ == '__main__':
    boxes, img_map, env = get_site(6)

    work_map = generate_map()
    #work_map = syncing_tiles_to_matrix(img_map,work_map)

    #for item in img_map:
    #    item.show()

    # marking map
    env.show()
    for row in work_map:
        print(row)
