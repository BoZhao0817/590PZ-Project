import math
import random
import utils

CONST_FOOD = "F"  # cat food
CONST_CAT = "C"  # cat
CONST_MOUSE = "M"  # mouse
CONST_EMPTY = "-"  # empty
CONST_OBSTACLE = "X"  # obstacle
CONST_DOG = "D"  # dog
# 6 possible direction for a singe move
DIRECTIONS = {(-1, -1), (-1, 0), (0, -1),
              (0, 1), (1, -1), (1, 0)}


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
        for direction in DIRECTIONS:
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
            if utils.check_valid_move(board, input_move):
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
        move_to = self.minimax()
        return 0, 0

    def is_lose(self):
        return False
    # win or lose
    # cat win, human lose - cat escaped + eat mouse
    # human win, cat lose - cat no where to go
    # careful with this situation:
    #  cat can still go, but no chance to win


class Dog:
    def __init__(self, loc):
        self.loc = loc

    def get_new_loc(self):
        direction = random.sample(DIRECTIONS, 1)[0]
        new_loc = self.loc[0] + direction[0], self.loc[1] + direction[1]
        return new_loc


class Game:
    def __init__(self, n, n_food, n_mouse, n_dog, dog_move_interval):
        assert n_dog == 1, "sorry, we only support one dog mode so far"

        # board
        self.status = Board(n, n_food, n_mouse, n_dog)
        self.status.init_board()
        # human
        self.human = Human()

        # smart cat
        cat_init_pos = self.status.get_loc(CONST_CAT)
        if n_mouse == 0:
            self.cat = Cat(cat_init_pos, is_eat=True)
        else:
            self.cat = Cat(cat_init_pos, is_eat=False)

        # get the location and degree of freedom of mouse
        self.mouse_loc = self.status.get_loc(CONST_MOUSE)
        self.mouse_df = {loc: 6 for loc in self.mouse_loc}
        for i in range(n_mouse):
            base_mouse_loc = self.mouse_loc[i]
            x, y = base_mouse_loc
            if x == 0 or x == n:
                self.mouse_df[base_mouse_loc] -= 1
            if y == 0 or y == n:
                self.mouse_df[base_mouse_loc] -= 1

            for j in range(i + 1, n_mouse):
                new_mouse_loc = self.mouse_loc[j]
                if utils.is_adjacent(base_mouse_loc, new_mouse_loc):
                    self.mouse_df[base_mouse_loc] -= 1
                    self.mouse_df[new_mouse_loc] -= 1

        # dogs
        if n_dog != 0:
            self.dogs = []
            dog_init_pos = self.status.get_loc(CONST_DOG)
            for pos in dog_init_pos:
                new_dog = Dog(pos)
                self.dogs.append(new_dog)
        # interval
        # if dog_move_interval == MAX_INT, means dog should be keep stationary
        self.interval = dog_move_interval

    def play_game(self):
        num_round = 0
        print("GAME start!!")
        self.status.show_board()
        while True:
            # human round
            print('HUMAN round')
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

            # cat round
            print('CAT round')
            new_cat_loc = self.cat.move()
            self.status.update_board_animal(self.cat.loc, new_cat_loc, CONST_CAT)
            self.cat.loc = new_cat_loc
            self.status.show_board()
            for loc in self.mouse_loc:
                if utils.is_adjacent(loc, new_cat_loc):
                    self.cat.eat_mouse = True
                    break
            # cat tell us if we win
            if self.cat.is_lose():
                print('Congratulations! Victory')
                return

            # dog round
            if num_round % self.interval == 0:
                for i in range(len(self.dogs)):
                    print('DOG no.{} round'.format(i))
                    new_dog = self.dogs[i]
                    new_dog_loc = new_dog.get_new_loc()
                    self.status.update_board_animal(new_dog.loc, new_dog_loc, CONST_DOG)
                    self.dogs[i].loc = new_dog_loc
                    if utils.is_adjacent(new_dog_loc, self.cat.loc):
                        print("CAT was catched by DOGS!!")
                        print("You win by chance")
                        self.status.show_board()
                        return
                self.status.show_board()

            num_round += 1


if __name__ == "__main__":
    my_game = Game(11, 0, 0, 0, 1)  # 8x8 grid, 2 food, 3 mice, 1 dog, 2 interval
    my_game.play_game()
