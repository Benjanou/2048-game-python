import math, random

class Square:
    def __init__(self, start=[2,4], max_value=2048):

        self.value = random.choice(start)
        self.max = max_value
        self.color = self.assign_color(max_value)
        self.mergable = True

    def __str__(self):
        return "   " + str(self.value)

    def assign_color(self, max):
        red = 255
        value = self.value
        if value <= max:
            green = (255/math.log(max, 2))*math.log(value, 2)
        else:
            green = 255
        blue = 0
        return (red, green, blue)

    def increment(self):
        if self.mergable:
            self.value = self.value * 2
            self.color = self.assign_color(self.max)
            self.mergable = False

    def activate(self):
        self.mergable=True

    def is_active(self):
        return self.mergable

    def get_color(self):
        return self.color

class Board:
    def __init__(self, height=4, width=4, max_value=2048):
        self.max = max_value
        self.board = []
        self.create_board(height, width)

    def __str__(self):
        pres = "\t Current Board State"
        board = self.board
        for i in range(len(board)):
            pres = pres + "\r\n\t"
            pres += ', '.join(str(e) for e in board[i])
        return pres

    def create_board(self,height, width):
        board = self.board
        for i in range(height):
            board.append([])
            for j in range(width):
                board[i].append(None)
        self.add_rand_square()

    def get_item(self, x, y):
        return self.board[y][x]

    def get_height(self):
        return len(self.board)

    def get_width(self):
        return len(self.board[0])

    def add_rand_square(self):
        board = self.board
        empty_slots = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == None:
                    empty_slots.append(len(board[0])*i+j)

        if empty_slots != []:
            slot = random.choice(empty_slots)
            rand_y = slot / len(board)
            rand_x = slot % len(board[0])
            board[rand_y][rand_x] = Square()

    def move_verticly(self, is_down):
        board = self.board
        empty_spaces = []

        # initialize
        for i in range(len(board[0])):
            empty_spaces.append(0)

        for i in range(len(board)):
            y_pos = i
            direction = 1
            if is_down:
                y_pos = len(board)-i-1
                direction = -1

            for j in range(len(board[y_pos])):
                if board[y_pos][j] == None:
                    empty_spaces[j] = empty_spaces[j]+1

                else:
                    board[y_pos][j].activate()
                    push_loc = y_pos - direction * empty_spaces[j]
                    if empty_spaces[j] != 0:

                        # push down
                        board[push_loc][j] = board[y_pos][j]
                        board[y_pos][j] = None
                        #empty_spaces[j] -= 1

                    # merge
                    if self.is_in_bound(push_loc-direction, 0, len(board)-1):
                        if (board[push_loc-direction][j] is not None):  # not the bottom row
                            is_merge_condition = board[push_loc][j].value == board[push_loc-direction][j].value
                            is_mergable = board[push_loc-direction][j].is_active()
                            if is_merge_condition & is_mergable:
                                board[push_loc - direction][j].increment()
                                board[push_loc][j] = None
                                empty_spaces[j] += 1

        self.add_rand_square()

    def move_horizontally(self, is_right):
        board = self.board
        empty_spaces = []

        # initialize
        for i in range(len(board[0])):
            empty_spaces.append(0)

        for i in range(len(board)):
            for j in range(len(board[i])):
                x_pos = j
                direction = 1
                if is_right:
                    x_pos = len(board[j]) - j - 1
                    direction = -1

                if board[i][x_pos] == None:
                    empty_spaces[i] = empty_spaces[i] + 1

                else:
                    board[i][x_pos].activate()
                    push_loc = x_pos - direction * empty_spaces[i]
                    if empty_spaces[i] != 0:
                        # push down
                        board[i][push_loc] = board[i][x_pos]
                        board[i][x_pos] = None
                        #empty_spaces[i] -= 1

                    # merge
                    if self.is_in_bound(push_loc-direction, 0, len(board[j])-1):
                        if (board[i][push_loc - direction] is not None):  # not the bottom row

                            is_merge_condition = board[i][push_loc].value == board[i][push_loc - direction].value
                            is_mergable = board[i][push_loc - direction].is_active()

                            if is_merge_condition & is_mergable:
                                board[i][push_loc - direction].increment()
                                board[i][push_loc] = None
                                empty_spaces[i] += 1

        self.add_rand_square()

    def is_in_bound(self, value, low, high):
        if (value >= low) & (value <= high):
            return True
        return False
