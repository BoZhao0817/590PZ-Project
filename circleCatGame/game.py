import random
import copy
import heapq

from utils import check_valid_move, generate_random_locations, is_adjacent, is_on_border
# from utils import *

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


class Board:
    def __init__(self, n, n_food, n_mouse, n_dog, n_obstacle=6):
        self.n = n
        self.n_food = n_food
        self.n_mouse = n_mouse
        self.n_dog = n_dog
        self.n_obstacle = n_obstacle
        self.loc_dict = {}

    def get_nodeType(self, loc):
        if loc in self.loc_dict:
            return self.loc_dict[loc]
        return CONST_EMPTY

    def random_place_mouse_food_dog(self, n_times, nodeType):
        for i in range(n_times):
            if len(self.loc_dict) > 0.5 * (self.n * self.n):
                break
            loc = generate_random_locations(self.n, self.loc_dict)
            self.loc_dict[loc] = nodeType

    def init_board(self):
        # place cat in the center of the board
        cat_loc = int(self.n / 2)
        self.loc_dict[(cat_loc, cat_loc)] = CONST_CAT

        # place mouses and food
        self.random_place_mouse_food_dog(self.n_mouse, CONST_MOUSE)
        self.random_place_mouse_food_dog(self.n_food, CONST_FOOD)
        self.random_place_mouse_food_dog(self.n_obstacle, CONST_OBSTACLE)
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
        print("   " + ' '.join([str(i) for i in range(self.n)]))
        for i in range(self.n):
            to_print = [str(i) + " "]
            # draw the board to hexagon
            if i % 2 == 0:
                to_print.insert(1, "")
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
            "input must be in [{},{},{},{},{}]".format(CONST_FOOD, CONST_CAT, CONST_MOUSE, CONST_OBSTACLE, CONST_DOG)

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
        is_even_row = int(loc[0] % 2)
        for direction in DIRECTIONS[is_even_row]:
            i = loc[0] + direction[0]
            j = loc[1] + direction[1]
            if check_valid_move(self.loc_dict, self.n, (i, j), who):
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
            if check_valid_move(board.loc_dict, board.n, input_move, CONST_OBSTACLE):
                return input_move
            print('Please enter a valid move')


class Cat:
    def __init__(self, loc, is_eat):
        self.loc = loc
        self.eat_mouse = is_eat
        self.met_dog = False
        # each position corresponding a score
        # each key is location, each value is a score
        self.minimax_score = {}

    def rearrange_direction(self, loc, directions):
        direction_score = {}
        for d in directions:
            new_loc = loc[0] + d[0], loc[1] + d[1]
            final_score = float("-inf")
            for key, val in self.mouse_df.items():
                dist = abs(key[0] - new_loc[0]) + abs(key[1] - new_loc[1])
                if dist == 0:  # the cat is next to a mouse, of course eat it
                    break
                final_score = max(final_score, val / dist)
            direction_score[-final_score] = d
        sorted_direction = [direction_score[key] for key in sorted(direction_score.keys())]
        return sorted_direction

    def minimax_move(self):
        curr_direction = DIRECTIONS[int(self.loc[0] % 2)]
        curr_direction = self.rearrange_direction(self.loc, curr_direction)
        next_loc = self.loc
        score = float("-inf")
        init_alpha, init_beta = float("-inf"), float("inf")
        visited = {"human": set([]), "cat": set([])}
        for directions in curr_direction:
            new_loc = (self.loc[0] + directions[0], self.loc[1] + directions[1])

            if new_loc not in self.board.loc_dict:  # this position is empty
                self.board.loc_dict.pop(self.loc)
                self.board.loc_dict[new_loc] = CONST_CAT
                # visited["cat"].add(new_loc)
                new_score = self.minimax(new_loc, self.search_depth, init_alpha, init_beta, visited, is_cat=False)
                self.board.loc_dict.pop(new_loc)
                self.board.loc_dict[self.loc] = CONST_CAT

            elif self.board.loc_dict.get(new_loc, 0) == CONST_MOUSE:  # this position is a mouse
                self.board.loc_dict.pop(self.loc)
                self.board.loc_dict[new_loc] = CONST_CAT
                # visited["cat"].add(new_loc)
                new_score = self.minimax(new_loc, self.search_depth, init_alpha, init_beta, visited, is_cat=False)
                self.board.loc_dict[new_loc] = CONST_MOUSE
                self.board.loc_dict[self.loc] = CONST_CAT
            else:
                continue

            if new_score > score:
                next_loc = new_loc
                score = new_score
                print("find a better one:", next_loc, new_loc, score)
        return next_loc

    def minimax(self, loc, depth, alpha, beta, visited, is_cat=True):
        # current position: self.loc
        # maximum depth: self.search_depth
        # status: used to find available next step
        # mouse_df: used to find the final score --
        #           currently the score is set to the degree of freedom of each mouse
        if loc in self.mouse_df:
            print("find a mouse to eat:", loc)
            return float("inf")

        if depth == 0:
            # score is calculated as df / Euclidean distance
            # probably need to be improved
            final_score = float("-inf")
            print("reaches the maximum depth")
            for key, val in self.mouse_df.items():
                dist = abs(key[0] - loc[0]) + abs(key[1] - loc[1])
                final_score = max(final_score, val / dist)
                print(val, dist, key, loc)
                print(val / dist, key)
            return final_score

        curr_directions = DIRECTIONS[int(loc[0] % 2)]
        curr_directions = self.rearrange_direction(self.loc, curr_directions)
        if is_cat:
            max_val = float("-inf")
            for directions in curr_directions:
                next_loc = loc[0] + directions[0], loc[1] + directions[1]
                if next_loc[0] < 0 or next_loc[0] >= self.board.n - 1 or next_loc[1] < 0 or next_loc[
                    1] >= self.board.n - 1:
                    continue
                if next_loc in visited["cat"]:
                    continue
                print("cat attemped move:", next_loc)
                if next_loc not in self.board.loc_dict:
                    # visited["cat"].add(next_loc)

                    self.board.loc_dict.pop(loc)
                    self.board.loc_dict[next_loc] = CONST_CAT
                    print("cat move:", loc, next_loc)
                    self.board.show_board()
                    score = self.minimax(next_loc, depth - 1, alpha, beta, visited,
                                         is_cat=False)

                    self.board.loc_dict.pop(next_loc)
                    self.board.loc_dict[loc] = CONST_CAT

                elif self.board.loc_dict.get(next_loc, 0) == CONST_MOUSE:
                    self.board.loc_dict.pop(loc)
                    self.board.loc_dict[next_loc] = CONST_CAT
                    print("cat move:", loc, next_loc)
                    self.board.show_board()
                    score = self.minimax(next_loc, depth - 1, alpha, beta, visited,
                                         is_cat=False)

                    self.board.loc_dict[next_loc] = CONST_MOUSE
                    self.board.loc_dict[loc] = CONST_CAT
                else:
                    continue

                max_val = max(max_val, score)
                alpha = max(alpha, score)
                print("alpha, beta for cat turn:", alpha, beta)
                if beta <= alpha:
                    break
            print("cat returned", max_val, alpha, beta, next_loc)
            self.minimax_score[loc] = max_val
            return max_val

        else:  # it's human's turn. Has n^2 choices.
            min_val = float("inf")
            for i in range(self.board.n):
                for j in range(self.board.n):
                    if check_valid_move(self.board.loc_dict, self.board.n, (i, j), who=CONST_OBSTACLE,
                                        verbose=False) and \
                            ((i, j) not in visited["human"]):
                        # visited["human"].add((i, j))
                        self.board.loc_dict[(i, j)] = CONST_OBSTACLE
                        print("human's choice:", (i, j))
                        self.board.show_board()
                        score = self.minimax(loc, depth - 1, alpha, beta, visited,
                                             is_cat=True)
                        self.board.loc_dict.pop((i, j))
                        # visited["human"].remove((i, j))
                        min_val = min(min_val, score)
                        beta = min(beta, score)
                        print("alpha, beta for human turn:", alpha, beta)
                        if beta <= alpha:
                            print("human returned:", (i, j), min_val, alpha, beta, score)
                            return min_val
            print("human used all loop returned:", (i, j), min_val, alpha, beta, score)
            return min_val

    def dijkstra_dist(self, loc, target):
        # calculate distance from a specific loc to borders
        # using bfs
        bfs_q = [loc]
        visited = set([])
        heapq.heapify(bfs_q)
        dist = 0
        reach_target = False
        while bfs_q:
            if reach_target:
                break
            dist += 1
            curr_len = len(bfs_q)
            for i in range(curr_len):
                new_node = heapq.heappop(bfs_q)
                visited.add(new_node)
                if target == "border":
                    if is_on_border(self.board.n, new_node):
                        reach_target = True
                        break
                elif target == CONST_MOUSE:
                    if self.board.loc_dict.get(new_node, 0) == CONST_MOUSE:
                        reach_target = True
                        break

                is_even_row = int(new_node[0] % 2)
                directions = DIRECTIONS[is_even_row]
                for d in directions:
                    next_node = new_node[0] + d[0], new_node[1] + d[1]
                    if check_valid_move(self.board.loc_dict, self.board.n, next_node, who=CONST_OBSTACLE,
                                        verbose=False) or \
                            self.board.loc_dict.get(next_node, 0) == CONST_MOUSE:
                        if next_node in visited:
                            continue
                        heapq.heappush(bfs_q, next_node)
                        visited.add(next_node)
        return dist

    def dijkstra_move(self, target="border"):
        #  check if the cat is on the border
        if self.loc[0] == 0:
            return self.loc[0] - 1, self.loc[1]
        elif self.loc[0] == self.board.n - 1:
            return self.loc[0] + 1, self.loc[1]
        elif self.loc[1] == 0:
            return self.loc[0], self.loc[1] - 1
        elif self.loc[1] == self.board.n - 1:
            return self.loc[0], self.loc[1] + 1

        # if not on the border
        # using bfs
        # first calculate one step ahead possible location
        directions = DIRECTIONS[int(self.loc[0] % 2)]
        possible_loc = []
        for d in directions:
            next_loc = self.loc[0] + d[0], self.loc[1] + d[1]
            if check_valid_move(self.board.loc_dict, self.board.n, next_loc) or \
                    self.board.loc_dict.get(next_loc, 0) == CONST_MOUSE:
                if target == "border":
                    if is_on_border(self.board.n, next_loc):
                        return next_loc
                elif target == CONST_MOUSE:
                    if self.board.loc_dict.get(next_loc, 0) == CONST_MOUSE:
                        return next_loc
                possible_loc.append(next_loc)

        final_loc = self.loc
        min_dist = float("inf")
        for loc in possible_loc:
            dist = self.dijkstra_dist(loc, target=target)
            print("possible location:", loc, dist)
            if dist < min_dist:
                min_dist = dist
                final_loc = loc
        return final_loc

    def move(self, status, score, method="minimax", search_depth=3):
        # first should detect is there a mouse around
        # if yes, must go to the mouse
        # strategy:
        # 1. use MinMax to find which mouse to eat
        # 2. if self.eat_mouse = True, use Djikstra's algorithm to get out
        #    reference: https://stackoverflow.com/questions/8641388/classic-game-circle-the-cat-algorithm
        # TODO: improve this strategy, because this might be a trap by human
        # TODO: if got food, can move two steps
        self.board = status
        self.mouse_df = score
        self.search_depth = search_depth
        if not self.eat_mouse:
            if method == "minimax":
                next_loc = self.minimax_move()
            elif method == "Dijkstra":
                next_loc = self.dijkstra_move(target=CONST_MOUSE)
            else:  # randomly pick one direction
                curr_direction = DIRECTIONS[int(self.loc[0] % 2)]
                next_direction = random.sample(curr_direction, 1)[0]
                next_loc = (self.loc[0] + next_direction[0], self.loc[1] + next_direction[1])
        else:
            next_loc = self.dijkstra_move()

        return next_loc


class Dog:
    def __init__(self, loc):
        self.loc = loc

    def get_new_loc(self, board):
        is_even_row = int(self.loc[0] % 2)
        direction = random.sample(DIRECTIONS[is_even_row], 1)[0]
        new_loc = self.loc[0] + direction[0], self.loc[1] + direction[1]
        while not check_valid_move(board.loc_dict, board.n, new_loc, who=CONST_DOG):
            direction = random.sample(DIRECTIONS[is_even_row], 1)[0]
            new_loc = self.loc[0] + direction[0], self.loc[1] + direction[1]
        return new_loc


class Game:
    def __init__(self, n, n_obstacle, n_food, n_mouse, n_dog, dog_move_interval):
        assert n_food == 0, "sorry, this version doesn't support food"

        self.size = n
        # board
        self.status = Board(n, n_food, n_mouse, n_dog, n_obstacle=n_obstacle)
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

            if x == 0 and y == 0:
                self.mouse_df[base_mouse_loc] = 3
            elif x == 0 and y == self.size - 1:
                self.mouse_df[base_mouse_loc] = 2
            elif (self.size - 1) % 2 == 1 and x == self.size - 1 and y == 0:
                self.mouse_df[base_mouse_loc] = 2
            elif (self.size - 1) % 2 == 1 and x == self.size - 1 and y == self.size - 1:
                self.mouse_df[base_mouse_loc] = 3
            elif (self.size - 1) % 2 == 0 and x == self.size - 1 and y == 0:
                self.mouse_df[base_mouse_loc] = 3
            elif (self.size - 1) % 2 == 0 and x == self.size - 1 and y == self.size - 1:
                self.mouse_df[base_mouse_loc] = 2
            elif x == 0 or x == self.size - 1:
                self.mouse_df[base_mouse_loc] -= 2
            elif x % 2 == 0 and y == 0:
                self.mouse_df[base_mouse_loc] -= 1
            elif x % 2 == 0 and y == self.size - 1:
                self.mouse_df[base_mouse_loc] -= 3
            elif x % 2 == 1 and y == 0:
                self.mouse_df[base_mouse_loc] -= 3
            elif x % 2 == 0 and y == self.size - 1:
                self.mouse_df[base_mouse_loc] -= 1

            for dog in self.dogs:
                dog_loc = dog.loc
                if is_adjacent(dog_loc, base_mouse_loc):
                    self.mouse_df[base_mouse_loc] -= 1

            for j in range(i + 1, n_mouse):
                new_mouse_loc = self.mouse_loc[j]
                if is_adjacent(base_mouse_loc, new_mouse_loc):
                    self.mouse_df[base_mouse_loc] -= 1
                    self.mouse_df[new_mouse_loc] -= 1

    def play_game(self, method, max_depth):
        num_round = 0
        print("GAME start!!")
        self.status.show_board()
        while True:
            # human round
            print("HUMAN's turn, round: {}".format(num_round + 1))
            human_move = self.human.move(self.status)
            self.status.update_board_human(human_move)
            self.status.show_board()

            for loc in self.mouse_loc:
                if is_adjacent(loc, human_move):
                    self.mouse_df[loc] -= 1
            if sum(self.mouse_df.values()) == 0 and (not self.cat.eat_mouse):
                print("cat can't eat any mouse, starved to death...")
                print("You win!")
                break

            # dog round
            for i in range(len(self.dogs)):
                dog_loc = self.dogs[i].loc
                if is_adjacent(dog_loc, self.cat.loc):
                    print("CAT was caught by DOGS!!")
                    print("You win by chance")
                    self.status.show_board()
                    return

            if len(self.dogs) != 0 and (num_round + 1) % self.interval == 0:
                for i in range(len(self.dogs)):
                    print("DOG no.{}'s turn, round: {}".format(i, num_round + 1))
                    new_dog = self.dogs[i]
                    new_dog_loc = new_dog.get_new_loc(self.status)
                    self.status.update_board_animal(new_dog.loc, new_dog_loc, CONST_DOG)
                    self.dogs[i].loc = new_dog_loc
                    if is_adjacent(new_dog_loc, self.cat.loc):
                        print("CAT was caught by DOGS!!")
                        print("You win by chance")
                        self.status.show_board()
                        return

                self.status.show_board()
            # cat round
            print("CAT's turn, round:{}".format(num_round + 1))
            while True:
                # check if there are available move for cat
                is_even_num = int(self.cat.loc[0] % 2)
                can_escape = False
                for move in DIRECTIONS[is_even_num]:
                    next_loc = self.cat.loc[0] + move[0], self.cat.loc[1] + move[1]
                    if check_valid_move(self.status.loc_dict, self.status.n, next_loc) or \
                            self.status.loc_dict.get(next_loc, 0) == CONST_MOUSE:
                        can_escape = True
                        break

                if not can_escape:
                    print("CAT was trapped by you!!")
                    return
                if not self.cat.eat_mouse:
                    new_cat_loc = self.cat.move(copy.deepcopy(self.status), copy.deepcopy(self.mouse_df),
                                                method=method, search_depth=max_depth)
                else:
                    new_cat_loc = self.cat.move(copy.deepcopy(self.status), copy.deepcopy(self.mouse_df),
                                                method="Dijkstra")

                if new_cat_loc in self.status.loc_dict and \
                        self.status.loc_dict[new_cat_loc] == CONST_MOUSE:  # cat eats a mouse
                    self.cat.eat_mouse = True
                    self.status.loc_dict.pop(new_cat_loc)
                    break

                if new_cat_loc not in self.status.loc_dict:
                    break

            if new_cat_loc[0] < 0 or new_cat_loc[0] >= self.size or \
                    new_cat_loc[1] < 0 or new_cat_loc[1] >= self.size:
                print("Ooops! You let the cat escaped!")
                print("You lost")
                break

            self.status.update_board_animal(self.cat.loc, new_cat_loc, CONST_CAT)
            self.cat.loc = new_cat_loc
            print("===========================")
            self.status.show_board()

            num_round += 1


if __name__ == "__main__":
    n_mouse = 2
    board_size = 5
    n_dog = 0
    n_food = 0
    n_obstacle = 5
    method1 = "minimax"
    max_depth = 3
    method2 = "Dijkstra"
    game = Game(n=board_size, n_obstacle=n_obstacle, n_food=n_food, n_mouse=n_mouse,
                n_dog=n_dog, dog_move_interval=2)
    game.play_game(method=method2, max_depth=max_depth)

