import generate_map as gm
import pickle
import random

verbose = False

# doomlings reference
def stabilize(list,value,num_to_reach):
    for key,item in enumerate(list):
        num_of_values = num_to_reach-len(item)
        list[key] += value*num_of_values
    return list

def get_label_data(label):
    value=label[1]
    voltorb_count=label[0]
    number_of_point_tiles = 5 - voltorb_count
    combinations = gm.combinationSum([1, 2, 3], value)
    combinations = [combination for combination in combinations if len(combination)==number_of_point_tiles]
    combinations = stabilize(combinations,[0],5)
    data = {
        'value':value,
        'voltorb_count':voltorb_count,
        'number_of_point_tiles':number_of_point_tiles,
    }


    return data,combinations

def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]

def get_used_values(env, coordinate):
    x = coordinate[0]
    y = coordinate[1]
    used_row_values = []
    used_column_values = []
    for row in env[:-1]:
        if row[x] != -1:
            used_column_values.append(row[x])
    for tile in env[y][:-1]:
        if tile != -1:
            used_row_values.append(tile)

    return used_row_values,used_column_values

def remove_used_values(combinations,used_values):
    for item in used_values:
        for combination in combinations:
            try:
                combination.remove(item)
            except ValueError:
                #print('Used not in list')
                combinations.remove(combination)
    return combinations



def valid_moves(env,coordinate):
    x = coordinate[0]
    y = coordinate[1]

    # getting possible combinations
    row_data, row_combinations = get_label_data(env[y][-1])
    column_data, column_combinations = get_label_data(env[-1][x])

    # removing used values from combinations
    used_row_values, used_column_values = get_used_values(env, (x,y))
    row_combinations = remove_used_values(row_combinations,used_row_values)
    column_combinations = remove_used_values(column_combinations,used_column_values)

    # getting possible choices
    # by intersection column and row combinations
    # and seeing if move is in left-overs
    intersection_list=[]
    for rc in row_combinations:
        for cc in column_combinations:
            if intersection(rc,cc):
                intersection_list.append((rc,cc, list(set(intersection(rc,cc)))))
    choice_list = [set[2] for set in intersection_list]
    for item in choice_list[1:]:
        choice_list[0] += item
    if choice_list:
        choice_list = list(set(choice_list[0]))



    return choice_list



def solve(env, row, column):
    if row == len(env)-1:                         # solution found
        if verbose: print('solution found')
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
        choices = valid_moves(env, (column,row))
        for item in choices:
            print(f'item choices',item)
            env[row][column] = random.choice(choices)
            boolean = bool(solve(env,row,column+1))
            if boolean:
                return solve(env, row,column+1)
            #env[row][column] = -1
        env[row][column] = -1

    else:
        return False, env


