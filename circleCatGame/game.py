import math
import random
import utils

CONST_FOOD = "F"  # cat food
CONST_CAT = "C"  # cat
CONST_MOUSE = "M"  # mouse
CONST_EMPTY = "-"  # empty
CONST_OBSTACLE = "X"  # obstacle
CONST_DOG = "D"  # dog
MAX_INT = 2**31 - 1
# 6 possible direction for a singe move
DIRECTIONS = {
    1: [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)],  # if row_num % 2 == 1
    0: [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]   # if row_num % 2 == 0
}


class Board:
    def __init__(self, n, n_food, n_mouse, n_dog):
        self.n = n
        self.n_food = n_food
        self.n_mouse = n_mouse
        self.n_dog = n_dog
        self.loc_dict = {}

    def get_nodeType(self, loc):
        if loc in self.loc_dict:
            return self.loc_dict[loc]
        return CONST_EMPTY

    def random_place_mouse_food_dog(self, n_times, nodeType):
        for i in range(n_times):
            loc = utils.generate_random_locations(self.n, self.loc_dict)
            self.loc_dict[loc] = nodeType

    def init_board(self):
        # place cat in the center of the board
        cat_loc = int(self.n / 2)
        self.loc_dict[(cat_loc, cat_loc)] = CONST_CAT

        # place mouses and  food
        self.random_place_mouse_food_dog(self.n_mouse, CONST_MOUSE)
        self.random_place_mouse_food_dog(self.n_food, CONST_FOOD)
        self.random_place_mouse_food_dog(self.n_dog, CONST_DOG)

    def update_board_human(self, loc):
        """
        update loc_dict
        don't check if loc is valid here
        should be checked before passing parameters in
        """
        self.loc_dict[loc] = CONST_OBSTACLE

    def update_board_animal(self, prev_loc, new_loc, who):
        """
        update loc_dict
        don't check if new_loc and prev_loc are valid here
        should be checked before passing parameters in
        """
        self.loc_dict.pop(prev_loc)
        self.loc_dict[new_loc] = who

    def show_board(self):
        for i in range(self.n):
            to_print = []
            # draw the board to hexagon
            if i % 2 == 0:
                to_print.insert(0, "")
            for j in range(self.n):
                if (i, j) in self.loc_dict:
                    to_print.append(self.loc_dict[(i, j)])
                else:
                    to_print.append("-")
            print(' '.join(to_print))

    def add_obstacle(self, loc):
        self.loc_dict[loc] = CONST_OBSTACLE

    def get_loc(self, who):
        """
        :param who: can be chosen from ["F","C","M","X","D"]
        :return: list of list
        """
        assert who in [CONST_FOOD, CONST_CAT, CONST_MOUSE, CONST_OBSTACLE, CONST_DOG], \
            "input must be in ['F','C','M','X','D']"

        loc = [key for key, val in self.loc_dict.items() if val == who]
        return loc

    def get_valid_moves(self, loc, who="Cat"):
        """
        :param loc: a tuple of two element
        :param who: either be ['Cat', 'Dog', 'Human'], remember only cat can escape from the board
        :return:
        """
        move_direction = []
        new_locs = []
        is_even_row = int(loc[0]%2)
        for direction in DIRECTIONS[is_even_row]:
            i = loc[0] + direction[0]
            j = loc[1] + direction[1]
            if utils.check_valid_move(self.loc_dict, self.n, (i, j), who):
                move_direction.append(direction)
                new_locs.append((i, j))
        return move_direction, new_locs


class Human:
    def __init__(self):
        pass

    def move(self, board):
        while True:
            input_str = input("Enter your move : ")
            i, j = input_str.split(',')
            input_move = (int(i), int(j))
            if utils.check_valid_move(board.loc_dict, board.n, input_move, CONST_OBSTACLE):
                return input_move
            print('Please enter a valid move')


class Cat:
    def __init__(self, loc, is_eat):
        self.loc = loc
        self.eat_mouse = is_eat
        self.met_dog = False

    def minimax(self):
        pass

    def move(self):
        is_even_row = int(self.loc % 2)
        random_move = random.sample(DIRECTIONS[is_even_row], 1)[0]
        return self.loc[0] + random_move[0], self.loc[1] + random_move[1]


class Dog:
    def __init__(self, loc):
        self.loc = loc

    def get_new_loc(self):
        is_even_row = int(self.loc % 2)
        direction = random.sample(DIRECTIONS[is_even_row], 1)[0]
        new_loc = self.loc[0] + direction[0], self.loc[1] + direction[1]
        return new_loc


class Game:
    def __init__(self, n, n_food, n_mouse, n_dog, dog_move_interval):
        assert n_food == 0, "sorry, this version doesn't support food"
        self.size = n
        # board
        self.status = Board(n, n_food, n_mouse, n_dog)
        self.status.init_board()
        # human
        self.human = Human()



        # smart cat
        cat_init_pos = self.status.get_loc(CONST_CAT)[0]  # there will only be one cat
        if n_mouse == 0:
            self.cat = Cat(cat_init_pos, is_eat=True)
        else:
            self.cat = Cat(cat_init_pos, is_eat=False)

        # dogs
        self.dogs = []
        if n_dog != 0:
            dog_init_pos = self.status.get_loc(CONST_DOG)
            for pos in dog_init_pos:
                new_dog = Dog(pos)
                self.dogs.append(new_dog)

        # get the location and degree of freedom of mouse
        self.mouse_loc = self.status.get_loc(CONST_MOUSE)
        self.mouse_df = {loc: 6 for loc in self.mouse_loc}
        self.init_mouse_df()


        # interval
        # if dog_move_interval == MAX_INT, means dog should be keep stationary
        self.interval = dog_move_interval


    def init_mouse_df(self):
        """
        initialize the freedom of mice
        """
        n_mouse = len(self.mouse_loc)
        for i in range(n_mouse):
            base_mouse_loc = self.mouse_loc[i]
            x, y = base_mouse_loc

            # if the mouse is on the boarder
            if x % 2 == 0:
                if y == 0:
                    self.mouse_df[base_mouse_loc] -= 1
                elif y == self.size - 1:
                    self.mouse_df[base_mouse_loc] -= 3
            else:
                if y == 0:
                    self.mouse_df[base_mouse_loc] -= 3
                else:
                    self.mouse_df[base_mouse_loc] -= 1
            # if x == 0 or x == self.size:
            #     self.mouse_df[base_mouse_loc] -= 2
            # if y == 0 or y == self.size:
            #     if x % 2 == 0:
            #         self.mouse_df[base_mouse_loc] -= 3
            #     else:
            #         self.mouse_df[base_mouse_loc] -= 2

            for dog in self.dogs:
                dog_loc = dog.loc
                if utils.is_adjacent(dog_loc, base_mouse_loc):
                    self.mouse_df[base_mouse_loc] -= 1

            for j in range(i + 1, n_mouse):
                new_mouse_loc = self.mouse_loc[j]
                if utils.is_adjacent(base_mouse_loc, new_mouse_loc):
                    self.mouse_df[base_mouse_loc] -= 1
                    self.mouse_df[new_mouse_loc] -= 1



    def play_game(self):
        num_round = 0
        print("GAME start!!")
        self.status.show_board()
        while True:
            # human round
            print("HUMAN's turn")
            human_move = self.human.move(self.status)
            self.status.update_board_human(human_move)
            self.status.show_board()

            for loc in self.mouse_loc:
                if utils.is_adjacent(loc, human_move):
                    self.mouse_df[loc] -= 1
            if sum(self.mouse_df.values()) == 0:
                print("cat can't eat any mouse, starved to death...")
                print("You win!")
                break

            # dog round
            if len(self.dogs) != 0 and (num_round+1) % self.interval == 0:
                for i in range(len(self.dogs)):
                    print('DOG no.{} round'.format(i))
                    new_dog = self.dogs[i]
                    new_dog_loc = new_dog.get_new_loc()
                    self.status.update_board_animal(new_dog.loc, new_dog_loc, CONST_DOG)
                    self.dogs[i].loc = new_dog_loc
                    if utils.is_adjacent(new_dog_loc, self.cat.loc):
                        print("CAT was caught by DOGS!!")
                        print("You win by chance")
                        self.status.show_board()
                        return

                self.status.show_board()
            # cat round
            print('CAT round')
            while True:
                new_cat_loc = self.cat.move()
                if new_cat_loc not in self.status.loc_dict:
                    break
            if new_cat_loc[0] < 0 or new_cat_loc[0] >= self.size or \
                    new_cat_loc[1] < 0 or new_cat_loc[1] >= self.size:
                print("Ooops! You let the cat escaped!")
                print("You lost")
                break

            self.status.update_board_animal(self.cat.loc, new_cat_loc, CONST_CAT)
            self.cat.loc = new_cat_loc
            self.status.show_board()
            for loc in self.mouse_loc:
                if utils.is_adjacent(loc, new_cat_loc):
                    self.cat.eat_mouse = True
                    break

            num_round += 1


if __name__ == "__main__":
    size = 6
    n_food = 0
    n_mouse = 1
    n_dog = 0
    # if dog_move_interval == MAX_INT, means dog should be keep stationary
    dog_move_interval = 1
    my_game = Game(size, n_food, n_mouse, n_dog, dog_move_interval)  # 8x8 grid, 2 food, 3 mice, 1 dog, 2 interval
    my_game.play_game()
