from random import randint, sample, choice, shuffle



# GeeksForGeeks
# https://www.geeksforgeeks.org/combinational-sum/
def findNumbers(ans, arr, temp, sum, index):
    if sum == 0:
        ans.append(list(temp))
        return

    for i in range(index, len(arr)):
        if (sum - arr[i]) >= 0:
            temp.append(arr[i])
            findNumbers(ans, arr, temp, sum-arr[i], i)

            temp.remove(arr[i])

# GeeksForGeeks
# https://www.geeksforgeeks.org/combinational-sum/
def combinationSum(arr, sum):
    ans = []
    temp = []


    arr = sorted(list(set(arr)))
    findNumbers(ans,arr,temp,sum,0)
    return ans

def generate_map():
    x = [-1 for i in range(0,5)]
    x.append(-1)
    temp = [x.copy() for i in range(0,5)]
    temp.append( [[-1,-1] for i in range(0,5)] )
    return temp

def generate_labels(range):
    # deciding how many voltorbs and the row value
    # handling extreme cases
    count = randint(range[0], range[1])
    value = randint((5 - count), (5 - count) * 3)
    if count == 5: value = 0
    if count == 0: value = randint(5, 15)

    return count, value

def set_row(env, count, value):
    # picking where each voltorb goes and
    # marking values at the end of the row
    locations = sample([i for i in range(0, 5)], k=count)
    env[-1] = [count, value]  # setting up end tile
    for loc in locations:
        env[loc] = 0

def set_column(env):
    # reading columns and filling in last
    # row with corrosponding information
    for x in range(0, 5):
        column_score = 0
        voltorb_score = 0
        for y in range(0, 5):
            if env[y][x] == 0:
                voltorb_score += 1
            else:
                column_score += env[x][y]

        env[5][x] = [voltorb_score, column_score]

def set_points(env):
    for index, row in enumerate(env[:-1]):
        # getting combination sum list
        voltorb_count, row_value = row[-1][0], row[-1][1]
        ch = [1, 2, 3]
        ans = combinationSum(ch, row_value)
        ans = [item for item in ans if len(item) == (5 - voltorb_count)]
        point_set = choice(ans)
        shuffle(point_set)

        # applying the set of points
        i = 0
        for key, location in enumerate(row[:-1]):
            if location == -1:
                row[key] = point_set[i]
                i += 1

def set_voltorbs(env, difficulty):
    if difficulty == 0: pass # have range change
    voltorb_range = [1,5]

    for key, row in enumerate(env[:-1]):
        voltorb_count, row_value = generate_labels(voltorb_range)
        set_row(row, voltorb_count, row_value)
    set_points(env)     # getting & applying point combination
    set_column(env)     # setting last row

def get_labels(env):
    # getting labels to
    # know how "easy" the
    # map is
    labels = [row[-1] for row in env[:-1]] + env[-1]
    ease_value = []
    point_value = []
    for key, label in enumerate(labels):
        if label == [5, 0] or label[0] == 0: ease_value.append(key)
        if label[1] > 9: point_value.append(key)

    return ease_value, point_value






map = generate_map()
set_voltorbs(map, 0)
for row in map:
    print(row)