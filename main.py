import generate_map
import generate_map as gm
import algorithm as alg
import website_script as ws
from selenium import webdriver
from tensorflow.keras.models import load_model
import pyautogui as pyg
import random



def web_loop():
    firefox = webdriver.Firefox()
    ws.open_site(firefox)
    dm = load_model('digits.keras')
    

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

        try:
            map_choice = random.choice(possible_tiles)
            x = boxes[y][x][0] + boxes[y][x][2] // 2
            y = boxes[y][x][1] + boxes[y][x][3] // 2
            pyg.click(x=x,y=y)
        except IndexError:
            print('No solution found')
            break

    firefox.close()


def commandline_run():
    solution = gm.generate_map()
    generate_map.set_voltorbs(solution,0)
    work_space = gm.make_work_copy(solution)

    result, work_space = alg.solve(work_space,0,0)
    valid_path = False

    if result: valid_path = True
    gm.printMap(solution, 'Solution')
    gm.printMap(work_space, 'Valid Path Found')

    print(f'Is path valid?', valid_path)
    print(f'Is path solution? {solution == work_space}')



if __name__ == '__main__':
    web_loop()