import math
import random


class TicTacToe:
    """
    a class for the TicTacToe game
    """
    def __init__(self, board_size = 3, win_length = 3, ai = True):
        """
        None for empty
        True for O
        False for X
        """
        self.board_size = board_size
        self.num_positions = board_size * board_size
        self.board = [None] * self.num_positions
        self.win_length = win_length
        # ai side
        self.ai = ai

    def display(self, input_list):
        assert len(input_list) == self.num_positions
        for row in xrange(self.board_size):
            start_pos = row * self.board_size
            end_pos = start_pos + self.board_size
            row_str = '|'.join(map(str, input_list[start_pos:end_pos]))
            print row_str

    def display_movement(self):
        print "Movement Key:"
        self.display(range(1, self.num_positions+1))

    def display_board(self):
        print "Board:"
        input = [' ' if piece is None else 'O' if piece == True else 'X'
                    for piece in self.board]
        self.display(input)

    def index2position(self, index):
        assert isinstance(index, int)
        if index < 1 or index > self.num_positions:
            # invalid index
            return -1, -1
        row = (index - 1) / self.board_size
        col = (index - 1) % self.board_size
        return row, col

    def position2index(self, row, col):
        assert isinstance(row, int)
        assert isinstance(col, int)
        if row < 0 or row >= self.board_size or \
            col < 0 or col >= self.board_size:
            # invalid row or col
            return -1
        return row * self.board_size + col + 1

    def get_position(self):
        try:
            index = int(raw_input("Where to? "))
        except ValueError:
            print "invalid movement key"
            return self.get_position()

        if index < 1 or index > self.num_positions:
            print "movement key out of range"
            return self.get_position()
        elif self.board[index-1] is not None:
            print "position already taken"
            return self.get_position()
        else:
            return index

    def ai_move(self, debug=False):
        # squared scores work better
        gain = map(lambda x: x*x, self.compute_scores(piece=self.ai))
        risk = map(lambda x: x*x, self.compute_scores(piece=not self.ai))
        scores = [gain[idx] + risk[idx] for idx in xrange(len(gain))]
        if debug:
            print "potential gain:"
            self.display(gain)
            print "potential risk:"
            self.display(risk)
            print "move scores:"
            self.display(scores)

        max_score = max(scores)
        max_idx = [index for index in xrange(len(scores))
                        if scores[index] == max_score and self.board[index] is None]
        if len(max_idx) > 0:
            idx = random.choice(max_idx) + 1
        else:
            return None
        print "I will put an O at position %d" % idx
        self.place_piece(idx, True)
        if self.is_game_over(idx):
            return True     # ai wins
        else:
            return False

    def place_piece(self, index, piece):
        assert isinstance(index, int)
        assert isinstance(piece, bool)
        if self.board[index-1] is not None:
            print("position %d already taken" % index)
            return False
        else:
            self.board[index-1] = piece
            self.display_board()
            return True

    def is_game_over(self, index):
        if self.compute_score(index) >= self.win_length:
             return True
        else:
             return False

    def compute_scores(self, piece=None):
        scores = []
        for index in xrange(1, self.num_positions+1):
            if self.board[index-1] is None:
                scores.append(self.compute_score(index, piece))
            else:
                scores.append(0)
        return scores

    def compute_score(self, index, piece=None):
        if piece is None:
            piece = self.board[index-1]
        # checking 8 directions
        # ul, u, ur, r, dr, d, dl, l
        ul = self.check_one_direction(index, -1, -1, piece)
        u  = self.check_one_direction(index, -1,  0, piece)
        ur = self.check_one_direction(index, -1, +1, piece)
        r  = self.check_one_direction(index,  0, +1, piece)
        dr = self.check_one_direction(index, +1, +1, piece)
        d  = self.check_one_direction(index, +1,  0, piece)
        dl = self.check_one_direction(index, +1, -1, piece)
        l  = self.check_one_direction(index,  0, -1, piece)
        return max([ul + dr + 1, ur + dl + 1, l + r + 1, u + d + 1])

    def check_one_direction(self, index, d_row, d_col, piece=None):
        # 1 <= index <= self.num_positions
        row, col = self.index2position(index)
        if d_row > 0:
            row_end = self.board_size - 1
        elif d_row < 0:
            row_end = 0
        else:
            row_end = row

        if d_col > 0:
            col_end = self.board_size - 1
        elif d_col < 0:
            col_end = 0
        else:
            col_end = col

        if d_row == 0:
            limit = int(math.fabs(col_end - col))
        elif d_col == 0:
            limit = int(math.fabs(row_end - row))
        else:
            limit = int(min(math.fabs(row_end-row), math.fabs(col_end-col)))

        if piece is None:
            piece = self.board[index-1]
        for i in xrange(1, limit+1):
            r = row + i * d_row
            c = col + i * d_col
            idx = self.position2index(r, c)
            if self.board[idx-1] != piece:
                return i-1
        return limit


if __name__ == "__main__":
    print "Welcome to Tic-Tac-Toe. Please make your move selection by " \
          "entering a number corresponding to the movement key on the right."
    human_side = False
    ai_side = not human_side

    b = TicTacToe(board_size=3, win_length=3, ai=ai_side)
    b.display_movement()
    b.display_board()

    idx = b.get_position()
    print "You have put an X at position %d" % idx
    b.place_piece(idx, human_side)
    while not b.is_game_over(idx):
        state = b.ai_move(debug=False)
        if state is None:
            print "No more moves, it's a draw"
            exit()
        elif state:
            print "You lose to a computer!"
            exit()
        b.display_movement()
        idx = b.get_position()
        print "You have put an X at position %d" % idx
        b.place_piece(idx, human_side)
    print "You have beaten my poor AI"
