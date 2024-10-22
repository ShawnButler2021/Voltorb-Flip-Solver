import generate_map
import generate_map as gm
import algorithm as alg


if __name__ == '__main__':
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