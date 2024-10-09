import generate_map as gm

verbose = 0

def printMap(env):
    for row in env:
        for item in row:
            if env[-1] == row:
                print(item,end='\t')
            elif row[-1] == item: print(item,end='')
            else: print(item,end='\t   | ')
        print()
    print('\n')

# isSafe/isValidMove
def isValidMove(env,coordinate,num):
    # setting up variables
    x = coordinate[0]
    y = coordinate[1]
    row_points = env[y][-1][1]
    column_points = env[-1][x][1]
    row_voltorb_count = env[y][-1][0]
    column_voltorb_count = env[-1][x][0]
    row_point_sum = 0
    column_point_sum = 0
    row_voltorb_sum = 0
    column_voltorb_sum = 0

    # check if points match up
    # check if voltorbs match up

    # row information gathering
    for item in env[y][:-1]:
        row_point_sum += item
        if item == 0: row_voltorb_sum += 1
    # column information gathering
    for row in env[:-1]:
        column_point_sum += row[x]
        if row[x] == 0: column_voltorb_sum += 1

    # extracting out conditions for readability
    over_row_points = row_point_sum >= row_points
    over_column_points = column_point_sum >= column_points
    over_row_voltorbs = row_voltorb_count >=  row_voltorb_sum
    over_column_voltorbs = column_voltorb_count >=  column_voltorb_sum
    booleans = [over_row_points,over_column_points,over_row_voltorbs,over_column_voltorbs]
    if verbose == 1:
        if over_row_points: print(f'{coordinate}: over_row_points')
        if over_row_points: print(f'{coordinate}: over_column_points')
        if over_row_points: print(f'{coordinate}: over_row_voltorbs')
        if over_row_points: print(f'{coordinate}: over_column_voltorbs')

    if False in booleans:
        return True
    return False

#
#def findSolution():
#   if (valid_solution):
#       return True
#       store solution
#       return
#   for (all choices):
#       if (valid_choice):
#           apply choice
#           find_Solution(parameters)
#           reverse_decision(choice)
#   return

def solve(env, row, column):
    # all solutions
    #   * solution found        x
    #   * empty tile            
    #   * filled tile
    #   * end of row            x


    # solution found
    if env[row] == env[-1]:
        return True, env
    elif column == 5:
        print(f'End of row {row}')
        return solve(env, row+1,0)
    elif env[row][column] == -1 and column != 5:
        print(f'Empty tile ({column},{row})')
        return solve(env, row,column+1)


    else:
        return False, env




solution_map = gm.generate_map()
solution_map = gm.set_voltorbs(solution_map, 0)
work_map = gm.make_work_copy(solution_map)

print('solution map')
printMap(solution_map)


#work_map[1][0]=solution_map[1][0]
#print('work',work_map[1][0])
#print('solution',solution_map[1][0])
#printMap(work_map)

result, path = solve(work_map,0,0)
print('Solved?',result)
#printMap(path)
x,y = 0,0

#for n in range(0,4):
#    print(f'({x},{y})->{n} is valid move?',isValidMove(work_map,(x,y),n))

