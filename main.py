import generate_map as gm

verbose = False
s = 0


# use combinationSum to get possibilities
# exclude 0 from list
# manually add 0 to combinations
# check columns AND rows
def isValidMove(env,coordinate, num):
    x = coordinate[0]
    y = coordinate[1]
    row_value = env[y][-1][1]
    column_value = env[-1][x][1]
    row_combinations = gm.combinationSum([1, 2, 3],row_value)
    column_combinations = gm.combinationSum([1, 2, 3],column_value)

    print('Row combinations\n',row_combinations)
    print('Column combinations\n',column_combinations)

    return True


def solve(env, row, column):
    if row == len(env)-1:                         # solution found
        return True, env
    elif column == 5:                               # end of row
        if verbose: print(f'End of row {row}')
        return solve(env, row+1,0)
    elif env[row][column] != -1 and column != 5:    # filled tile
        if verbose: print(f'Filled tile ({column},{row})')
        return solve(env, row, column+1)
    elif env[row][column] == -1 and column != 5:    # empty tile
        if verbose: print(f'Empty tile ({column},{row})')

        # bread and butter
        # check if all possible states are
        # valid moves
        # revert changes if not
        for i in range(0,4):
            if isValidMove(env,(column,row), i):
                env[row][column] = i
                if solve(env, row,column+1): return True, env
                env[row][column] = -1
        return False, env

    else:
        return False, env




solution_map = gm.generate_map()
solution_map = gm.set_voltorbs(solution_map, 0)
work_map = gm.make_work_copy(solution_map)

gm.printMap(solution_map,'solution')


#work_map[1][0]=solution_map[1][0]
#print('work',work_map[1][0])
#print('solution',solution_map[1][0])
#gm.printMap(work_map)

if s == 1:
    result, path = solve(work_map,0,0)
    print('Solved?',result)
    gm.printMap(path, 'path')


# need to check columns
if s == 0:
    x,y = 0,0
    for k1,v1 in enumerate(solution_map[:-1]):
        work_map[k1][0] = solution_map[k1][0]
        for k2, v2 in enumerate(v1[:-1]):
            work_map[0][k2] = solution_map[0][k2]
    gm.printMap(work_map, 'work map')
    print(isValidMove(work_map,(0,0),1))

#for n in range(0,4):
#    print(f'({x},{y})->{n} is valid move?',isValidMove(work_map,(x,y),n))

