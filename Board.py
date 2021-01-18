import math, random

class Square:
    def __init__(self, start=[2,4], max_value=2048):

        self.value = random.choice(start)
        self.max = max_value
        self.color = self.assign_color(max_value)

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
        self.value = self.value * 2
        self.color = self.assign_color(self.max)


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

    def shift_left(self):
        board = self.board
        empty_spaces = [0]*4
        moved_tiles = False

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] is None:
                    empty_spaces[i] += 1
                else:
                    board[i][j-empty_spaces[i]]=board[i][j]
                    if (j-empty_spaces[i])!=j:
                        board[i][j]=None
                        moved_tiles=True
            empty_spaces = [0]*4
        return moved_tiles

    def merge_left(self):
        board = self.board
        has_marged = False

        for i in range(len(board)):
            for j in range(1,len(board[i])):
                current = board[i][j]
                previous = board[i][j-1]
                if (current is not None) & (previous is not None):
                    if current.value == previous.value:
                        previous.increment()
                        board[i][j] = None
                        has_marged = True
        return has_marged


    def reverse_board(self):
        board = self.board

        for i in range(len(board)):
            for j in range(int(len(board[i])/2)):
                current = board[i][j]
                board[i][j] = board[i][len(board[j])-j-1]
                board[i][len(board[j]) - j - 1] = current

    def transpose(self):
        board = self.board
        for i in range(len(board)):
            for j in range((i+1)):
                current = board[i][j]
                board[i][j] = board[j][i]
                board[j][i] = current


    def left_move(self):
        legal = self.shift_left()
        legal = self.merge_left() | legal
        self.shift_left()
        if legal:
            self.add_rand_square()

    def right_move(self):
        self.reverse_board()
        legal = self.shift_left()
        legal = self.merge_left() | legal
        self.shift_left()
        self.reverse_board()
        if legal:
            self.add_rand_square()

    def up_move(self):
        self.transpose()
        legal = self.shift_left()
        legal = self.merge_left() | legal
        self.shift_left()
        self.transpose()
        if legal:
            self.add_rand_square()

    def down_move(self):
        self.transpose()
        self.reverse_board()
        legal = self.shift_left()
        legal = self.merge_left() | legal
        self.shift_left()
        self.reverse_board()
        self.transpose()
        if legal:
            self.add_rand_square()

