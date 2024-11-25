import generate_map
import generate_map as gm
import algorithm as alg
import website_script as ws
from selenium import webdriver
from tensorflow.keras.models import load_model
import pyautogui as pyg
import random
import sys


def web_loop():
    firefox = webdriver.Firefox()
    ws.open_site(firefox)
    dm = load_model('digits.keras')
    

    visited = []
    while True:
        boxes, img_map, env = ws.get_map()

        w_map = ws.copy_map(img_map, dm)

        result, solution_map = alg.solve(w_map,0,0)


        for row in w_map:
            print(row)
        
        possible_tiles = []
        for y, row in enumerate(w_map[:-1]):
            for x, tile in enumerate(row[:-1]):
                if tile == 2 or tile == 3: possible_tiles.append((x,y))
        print('Possible tiles to click:', possible_tiles)
        

        #gm.printMap(w_map,'work')
        if possible_tiles:
            map_choice = random.choice(possible_tiles)
        
            if map_choice in visited:
                map_choice = (random.randint(0,4), random.randint(0,4))

        else: map_choice = (random.randint(0,4), random.randint(0,4))

        x, y = map_choice
        try:
            box = boxes[y][x]
        except IndexError:
            box = boxes[random.randint(0,4)][random.randint(0,4)]

        for row in boxes:
            print(row)


        x = box[0] + box[2] // 2
        y = box[1] + box[3] // 2
            


        pyg.click(x=x,y=y)
        visited.append(map_choice)

    firefox.close()


def commandline_run():
    solution = gm.generate_map()
    generate_map.set_voltorbs(solution,0)
    work_space = gm.make_work_copy(solution)

    result, work_space = alg.solve(work_space,0,0)
    valid_path = False

    while not result:
        result, work_space = alg.solve(work_space,0,0)
    valid_path = True


    gm.printMap(solution, 'Solution')
    gm.printMap(work_space, 'Valid Path Found')

    print(f'Is path valid?', valid_path)
    print(f'Is path solution? {solution == work_space}')



if __name__ == '__main__':
    try:
        if sys.argv[1] == 'web': web_loop()
        elif sys.argv[1] == 'cli': commandline_run()
    except IndexError:
        print('Add web or cli as the second argument of your call.')
        print('Example: python main.py web')