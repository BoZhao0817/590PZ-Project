import utils

CONST_FOOD = "F" # cat food
CONST_CAT = "C" # cat
CONST_MOUSE = "M" # mouse
CONST_EMPTY = "-" # empty
CONST_OBSTACLE = "X" # obstacle
CONST_DOG = "D" # dog
POSSIBLE_DIRECTIONS = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'DOWN': (0, 1), 'UP-LEFT': (-1, -1),
                       'UP-RIGHT': (-1, 1)}


class board():
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

    def random_place_mouse_food_dog(self, n_times, noodeType):
        for i in range(n_times):
            loc = utils.generate_random_locations(self.n, self.loc_dict)
            self.loc_dict[loc] = noodeType

    def init_board(self):
        # place cat in the center of the board
        self.loc_dict[(self.n / 2, self.n / 2)] = CONST_CAT
        # place mouses and  food
        self.random_place_mouse_food_dog(self.n_mouse, CONST_MOUSE)
        self.random_place_mouse_food_dog(self.n_food, CONST_FOOD)
        self.random_place_mouse_food_dog(self.n_dog, CONST_DOG)

    def show_board(self):
        for i in range(self.n):
            to_print = []
            for j in range(self.n):
                if (i, j) in self.loc_dict:
                    to_print.append(self.loc_dict[(i, j)])
                else:
                    to_print.append('-')
            print(' '.join(to_print))

    def add_obstacle(self, loc):
        self.loc_dict[loc] = CONST_OBSTACLE

    def get_cat_loc(self):
        pass

    def get_dog_loc(self):
        pass

    # FOR CAT
    def get_valid_moves(self, loc):
        moves = []
        new_locs = []
        for direction in POSSIBLE_DIRECTIONS:
            i = loc[0] + direction[0]
            j = loc[1] + direction[1]
            if (i,j) not in self.loc_dict:
                # can reach outside, no need to check i,j index
                moves.append(direction)
                new_locs.append((i, j))
        return moves, new_locs


class human:
    def __init__(self, board):
        self.board = board
        self.n = board.n

    def check_valid_move(self, board, input_move):
        i, j = input_move
        if (i, j) not in board.loc_dict and i >= 0 and i < board.n and j >= 0 and j < board.n:
            return True
        return False

    def where_to_move(self, board):
        while True:
            input_str = input("Enter your move : ")
            i, j = input_str.split(',')
            input_move = (int(i), int(j))
            if self.check_valid_move(board, input_move):
                return input_move
            print('Please enter a valid move')

    def human_move(self):
        move_to = self.where_to_move(self.board)
        self.board.add_obstacle(move_to)

class cat:
    def __init__(self, board):
        self.board = board

    def minimax(self):
        pass

    def cat_move(self):
        move_to = self.minimax()
        pass

    def is_lose(self):
        return False
    # win or lose
        # cat win, human lose - cat escaped + eat mouse
        # human win, cat lose - cat no where to go
    # careful with this situation:
    #  cat can still go, but no chance to win


class game:
    def __init__(self, n, n_food, n_mouse, n_dog, interval):
        # board
        self.board = board(n, n_food, n_mouse, n_dog)
        self.board.init_board()
        # human
        self.human = human(self.board)
        # smart cat
        self.cat = cat(self.board)
        # interval
        self.interval = interval

    def show(self):
        self.board.show_board()

    def play_game(self):
        while True:
            # human round
            print('HUMAN round')
            self.show()
            self.human.human_move()
            # cat round
            print('CAT round')
            self.cat.cat_move()
            self.show()
            # cat tell us if we win
            if self.cat.is_lose():
                print('Congratulations! Victory')
                return
            # dog round
            print('DOG round')
            # add your codes
            self.show()


my_game = game(8, 2, 3, 1, 2) # 8x8 grid, 2 food, 3 mice, 1 dog, 2 interval
my_game.play_game()
