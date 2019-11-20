"""
this script is used to develop better GUI
which might be involved with tkinter
for now just run game.py should be enough
"""
import game

CONST_FOOD = "F"  # cat food
CONST_CAT = "C"  # cat
CONST_MOUSE = "M"  # mouse
CONST_EMPTY = "-"  # empty
CONST_OBSTACLE = "X"  # obstacle
CONST_DOG = "D"  # dog
MAX_INT = 2 ** 31 - 1
# 6 possible direction for a singe move
DIRECTIONS = {
    1: [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)],  # if row_num % 2 == 1
    0: [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]  # if row_num % 2 == 0
}


if __name__ == "__main__":
    size = 11
    n_food = 0
    n_mouse = 3
    n_dog = 0
    # if dog_move_interval == MAX_INT, means dog should be keep stationary
    dog_move_interval = MAX_INT
    my_game = game.Game(size, n_food, n_mouse, n_dog, dog_move_interval)  # 8x8 grid, 2 food, 3 mice, 1 dog, 2 interval
    my_game.play_game()
