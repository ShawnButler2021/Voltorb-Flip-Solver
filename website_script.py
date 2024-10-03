from selenium import webdriver
from PIL import Image
import time
import pyautogui as pyg
import cv2
import numpy as np
import sys


def open_site(driver):
    driver.get('https://voltorbflip.brandon-stein.com/')
    time.sleep(2)

def image_transformation(img, pixels=50):
    # making image easier to work with
    #data = cv2.resize(np.array(img), (16 * pixels, 9 * pixels))
    return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)



if __name__ == '__main__':
    with webdriver.Firefox() as firefox:
        open_site(firefox)
        time.sleep(5)
        image = image_transformation(pyg.screenshot())


        map = list(pyg.locateAll('comparison-pictures\\map.png', image, confidence=0.7))

        left_margin = 15    # got through trial-and-error
        top_margin = 15     # got through trial-and-error

        split = int((map[0][0] + map[0][2])/10) # got through trial-and-error

        # visual purposes
        '''for loc in map:

            #cv2.rectangle(image, (loc[0]+left_margin,loc[1]+top_margin), (x,y), (0,0,255), 2)

            # total map
            #cv2.rectangle(image, (loc[0],loc[1]), (loc[0]+loc[2],loc[1]+loc[3]), (0,0,255), 2)
            # map without margins
            #cv2.rectangle(image, (loc[0]+left_margin,loc[1]+top_margin), (loc[0]+loc[2]-left_margin,loc[1]+loc[3]-top_margin), (0,0,255), 2)

            print(f'Width: {loc[2]}')
            print(f'Height: {loc[3]}')'''

        loc = map[0]
        img_map = []
        for y in range(1,4):
            y_top = loc[1]+split*(y-1)
            y_bottom = loc[1]+split*(y)

            row = []

            for x in range(1,3):
                x_left = loc[0]+split*(x-1)
                x_right = loc[0]+split*(x)

                # if you want to draw rectangles
                # on the image
                cv2.rectangle(image, (x_left+left_margin, y_top+top_margin), (x_right,y_bottom), (0,0,255), 2)

                temp = pyg.screenshot(region=(int(x_left+left_margin), int(y_top+top_margin), int(split), int(split)))
                temp.resize((200,200))

                row.append(temp)
            img_map.append(row)




        matrix_map = []
        for row in img_map:
            new_row = []
            for img in row:
                for item in ['tile-empty.png','tile-1.png','tile-2.png','tile-3.png', 'tile-0.png']:
                    try:
                        print(list(pyg.locate(f'comparison-pictures\\{item}', img, confidence=0.15)))
                        new_row.append(item.strip('.png')[-1])
                    except pyg.ImageNotFoundException:
                        print(f'Not {item}')
            matrix_map.append(new_row)

        print(matrix_map)
        cv2.imshow('',image)
        cv2.waitKey(0)
