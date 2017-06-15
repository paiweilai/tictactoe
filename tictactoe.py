import math
import random


class TicTacToe:

    def __init__(self, board_size, ai_side):
        """
        None for empty
        True for O
        False for X
        """
        self.board_size = board_size
        self.num_positions = board_size * board_size
        self.board = [None] * self.num_positions
        self.ai_side = ai_side

    def display(self, input_list):
        assert len(input_list) == self.num_positions
        for i in xrange(0, self.num_positions, self.board_size):
            print '|'.join(str(x) for x in input_list[i:i+self.board_size])

    def display_movement(self):
        print "Movement Key:"
        self.display(range(1, self.num_positions + 1))

    def display_board(self):
        print "Board:"
        input_list = [
            ' ' if piece is None else 'O' if piece is True else 'X'
            for piece in self.board
        ]
        self.display(input_list)

    def index2position(self, index):
        if self.is_valid_index(index):
            row = (index - 1) / self.board_size
            col = (index - 1) % self.board_size
            return row, col
        else:
            return -1, -1

    def is_valid_index(self, index):
        assert isinstance(index, int)
        return 1 <= index <= self.num_positions

    def position2index(self, row, col):
        if self.is_valid_position(row, col):
            return row * self.board_size + col + 1
        else:
            return -1

    def is_valid_position(self, row, col):
        assert isinstance(row, int)
        assert isinstance(col, int)
        return (
            0 <= row < self.board_size and
            0 <= col < self.board_size
        )

    def get_position(self):
        while True:
            try:
                index = int(raw_input("Where to? "))
            except ValueError:
                print "Invalid movement key."
            else:
                if not self.is_valid_index(index):
                    print "Movement key out of range."
                elif not self.is_valid_move(index):
                    print "Position already taken."
                else:
                    return index

    def is_valid_move(self, index):
        return self.board[index-1] is None

    def ai_move(self, debug=False):
        # squared scores work better
        gain = [x * x for x in self.compute_scores(self.ai_side)]
        risk = [x * x for x in self.compute_scores(not self.ai_side)]
        scores = [x + y for x, y in zip(gain, risk)]
        if debug:
            print "Potential gain:"
            self.display(gain)
            print "Potential risk:"
            self.display(risk)
            print "Move scores:"
            self.display(scores)

        max_score = max(scores)
        max_idx = [
            index for index in xrange(len(scores))
            if scores[index] == max_score and self.board[index] is None
        ]
        if len(max_idx) > 0:
            return random.choice(max_idx) + 1
        else:
            return None  # no more move

    def place_piece(self, index, piece):
        assert isinstance(index, int)
        assert isinstance(piece, bool)
        if not self.is_valid_move(index):
            print "Position %d already taken" % index
            return False
        else:
            self.board[index - 1] = piece
            self.display_board()
            return True

    def is_game_over(self, index):
        return self.compute_score(index, None) >= self.board_size

    def compute_scores(self, piece):
        return [
            self.compute_score(index, piece) if self.is_valid_move(index) else 0
            for index in xrange(1, self.num_positions + 1)
        ]

    def compute_score(self, index, piece):
        if piece is None:
            piece = self.board[index - 1]
        print self.board
        # checking 8 directions
        # ul, u, ur, r, dr, d, dl, l
        ul = self.check_one_direction(index, -1, -1, piece)
        u = self.check_one_direction(index, -1,  0, piece)
        ur = self.check_one_direction(index, -1, +1, piece)
        r = self.check_one_direction(index,  0, +1, piece)
        dr = self.check_one_direction(index, +1, +1, piece)
        d = self.check_one_direction(index, +1,  0, piece)
        dl = self.check_one_direction(index, +1, -1, piece)
        l = self.check_one_direction(index,  0, -1, piece)
        print ul, u, ur
        print l, r
        print dl, d, dr
        # import pdb
        # pdb.set_trace()
        x = max([ul + dr + 1, ur + dl + 1, l + r + 1, u + d + 1])
        print x
        return x

    def check_one_direction(self, index, d_row, d_col, piece=None):
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

    t = TicTacToe(board_size=3, ai_side=ai_side)
    t.display_board()

    while True:
        t.display_movement()

        index = t.get_position()
        print "You have put an X at position %d." % index
        t.place_piece(index, human_side)

        if t.is_game_over(index):
            print "You have beaten my poor AI."
            break

        index = t.ai_move(debug=False)
        if index is None:
            print "No more moves, it's a draw."
            break
        else:
            print "I will put an O at position %d." % index
            t.place_piece(index, ai_side)

        if t.is_game_over(index):
            print "You lose to a computer!"
            break
