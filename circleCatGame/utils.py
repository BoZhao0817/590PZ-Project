from random import randint

CONST_FOOD = "F"  # cat food
CONST_CAT = "C"  # cat
CONST_MOUSE = "M"  # mouse
CONST_EMPTY = "-"  # empty
CONST_OBSTACLE = "X"  # obstacle
CONST_DOG = "D"  # dog

# 6 possible direction for a singe move
DIRECTIONS = {(-1, -1), (-1, 0), (0, -1),
              (0, 1), (1, -1), (1, 0)}

def generate_random_locations(n, loc_dict):
    # within a board n*n
    # generate a random valid location
    while True:
        i = randint(0, n - 1)
        j = randint(0, n - 1)
        if (i, j) not in loc_dict:
            return i, j


def check_valid_move(loc_dict, board_size, input_move, who=CONST_CAT):
    i, j = input_move
    if who.strip().upper() == CONST_CAT:
        if (i, j) not in loc_dict:
            return True
        return False

    if (0 <= i < board_size) and (0 <= j < board_size):
        if (i, j) not in loc_dict:
            return True
        else:
            print("This position has been occupied")
            return False
    else:
        print("Your move is out of boundary")
        return False


def is_adjacent(loc1, loc2):
    x1, y1 = loc1
    x2, y2 = loc2
    for direction in DIRECTIONS:
        delta_x, delta_y = direction[0], direction[1]
        if x1+delta_x == x2 and y1+delta_y == y2:
            return True
    return False
