class WebInterface:
    def __init__(self):
        self.inputlabel = None
        self.btnlabel = None
        self.errmsg = None
        self.board = None



class Board:
    '''
    The game board is represented as an 8×8 grid,
    with each position on the grid described as
    a pair of ints (range 0-7): col followed by row
    07  17  27  37  47  57  67  77
    06  16  26  36  46  56  66  76
    05  15  25  35  45  55  65  75
    04  14  24  34  44  54  64  74
    03  13  23  33  43  53  63  73
    02  12  22  32  42  52  62  72
    01  11  21  31  41  51  61  71
    00  10  20  30  40  50  60  70
    '''
    def __init__(self):
        self.position = {}
        self.turn = "white"
        self.winner = None
        self.debug = False

    # 
    def start(self):
        '''Set up the pieces and start the game.'''
        colour = 'black'
        self.add((0, 7), Rook(colour))
        self.add((1, 7), Knight(colour))
        self.add((2, 7), Bishop(colour))
        self.add((3, 7), Queen(colour))
        self.add((4, 7), King(colour))
        self.add((5, 7), Bishop(colour))
        self.add((6, 7), Knight(colour))
        self.add((7, 7), Rook(colour))
        for x in range(0, 8):
            self.add((x, 6), Pawn(colour))

        colour = 'white'
        self.add((0, 0), Rook(colour))
        self.add((1, 0), Knight(colour))
        self.add((2, 0), Bishop(colour))
        self.add((3, 0), Queen(colour))
        self.add((4, 0), King(colour))
        self.add((5, 0), Bishop(colour))
        self.add((6, 0), Knight(colour))
        self.add((7, 0), Rook(colour))
        for x in range(0, 8):
            self.add((x, 1), Pawn(colour))

    def display(self):
        '''
        Displays the contents of the board.
        Each piece is represented by a coloured symbol.
        '''
        # helper function to generate symbols for piece
        # Row 7 is at the top, so print in reverse order
        str = ' '
        for row in range(8, -1, -1):
            for col in range(0,8):
                if row == 8 and col == 0:
                    str += '  '
                    # print('  ', end = '')
                if row == 8:
                    str += f'{col}'
                    # print(col, end = '')
                if col == 0 and row != 8:
                    str += f' {row} '
                    # print(row, end = ' ')
                coord = (col, row)  # tuple
                if coord in self.coords():
                    piece = self.get_piece(coord)
                    str += f'{piece.symbol()}'
                    # print(f'{piece.symbol()}', end='')
                else:
                    piece = None
                    str += ' '
                    # print(' ', end='')
                if col == 7:     # Put line break at the end
                    str += '\n'
                    # print('')
                else:            # Print a space between pieces
                    if row != 8:
                        str += ' '
                        # print(' ', end='')
        return str.split("\n")

    def coords(self):
        '''Return list of piece coordinates.'''
        return self.position.keys()

    def pieces(self):
        '''Return list of board pieces.'''
        return self.position.values()

    def get_piece(self, coord):
        '''
        Return the piece at coord.
        Returns None if no piece at coord.
        '''
        return self.position.get(coord, None)

    def find_piece(self, name, colour):
        '''
        Return the coord of a specific piece
        '''
        coord = None
        for el in self.position:
            if self.get_piece(el).name == name:
                if self.get_piece(el).colour  == colour:
                    coord = el
                    break
        return coord

    def add(self, coord, piece):
        '''Add a piece at coord.'''
        self.position[coord] = piece

    def remove(self, coord):
        '''
        Remove the piece at coord, if any.
        Does nothing if there is no piece at coord.
        '''
        if coord in self.coords():
            del self.position[coord]

    def move(self, start, end):
        '''
        Move the piece at start to end.
        Validation should be carried out first
        to ensure the move is valid.
        '''
        piece = self.get_piece(start)
        self.remove(start)
        self.add(end, piece)

    def prompt(self):
        '''
        Input format should be two ints,
        followed by a space,
        then another 2 ints
        e.g. 07 27
        '''

        def valid_format(inputstr):
            '''
            Ensure input is 5 characters: 2 numerals,
            followed by a space,
            followed by 2 numerals
            '''
            return len(inputstr) == 5 and inputstr[2] == ' ' \
                   and inputstr[0:1].isdigit() \
                   and inputstr[3:4].isdigit()

        def valid_num(inputstr):
            '''Ensure all inputted numerals are 0-7.'''
            for char in (inputstr[0:2] + inputstr[3:5]):
                if char not in '01234567':
                    return False
            return True

        def split_and_convert(inputstr):
            '''Convert 5-char inputstr into start and end tuples.'''
            start, end = inputstr.split(' ')
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            return (start, end)

        while True:
            inputstr = self.inputf(f'{self.turn.title()} player: ')
            if not valid_format(inputstr):
                self.printf('Invalid input. Please enter your move in the '
                      'following format: __ __, _ represents a digit.')
            elif not valid_num(inputstr):
                self.printf('Invalid input. Move digits should be 0-7.')
            else:
                start, end = split_and_convert(inputstr)
                if self.valid_move(start, end):
                    left, right = inputstr.split(' ')
                    left = str(left)
                    right = str(right)
                    with open('moves.txt','a') as f:
                        f.write(f'{self.turn.title()}'.lower() + ' ' + left + ' --> ' + right + '\n')
                    return start, end
                else:
                    self.printf(f'Invalid move for {self.get_piece(start)}.')

    def valid_move(self, start, end):
        '''
        Returns True if all conditions are met:
        1. There is a start piece of the player's colour
        2. There is no end piece, or end piece is not of player's colour
        3. The move is not valid for the selected piece
        Returns False otherwise
        '''
        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        if end_piece == None:
            empty = True
        else:
            empty = False
        if start_piece is None or start_piece.colour != self.turn:
            return False
        elif end_piece is not None and end_piece.colour == self.turn:
            return False
        elif not start_piece.isvalid(start, end, empty):
            return False
        return True


    def update(self, start, end):
        '''
        Update board information with the player's move.
        '''
        self.remove(end)
        self.move(start, end)
        self.promotion(end)
        self.checkmate(end)
        self.win()


    def win(self):
        """
        Checks for a winner
        """
        white_king = self.find_piece('king', 'white')
        black_king = self.find_piece('king', 'black')
        if white_king is None:
            piece = self.get_piece(black_king)
            self.winner = piece.colour
        elif black_king is None:
            piece = self.get_piece(white_king)
            self.winner = piece.colour
        else:
            self.winner = None

    def promotion(self, end):
        """
        Checks for available pawns to be promoted and prompts player for choice of promotion.
        """
        if end[1] in (0, 7):
            piece = self.get_piece(end)
            colour = piece.colour
            if piece.name == Pawn(colour).name:
                self.remove(end)
                self.add(end, Queen(colour))

    def next_turn(self):
        '''
        Hand the turn over to the other player.
        '''
        if self.turn == 'white':
            self.turn = 'black'
        elif self.turn == 'black':
            self.turn = 'white'


    def checkmate(self, end):
        '''
        Determines if a player has been checkmated.
        '''
        piece = self.get_piece(end)
        if piece.colour == 'black':
            colour = 'White'
        else:
            colour = 'Black'
        king_coord = self.find_piece('king', colour.lower())
        if not king_coord is None:
            if piece.isvalid(end, king_coord, None):
                self.printf(f"{colour} is checkmated!")



class BasePiece:
    name = 'piece'
    sym = {}

    def __init__(self, colour):
        if type(colour) != str:
            raise TypeError('colour argument must be str')
        elif colour.lower() not in {'white', 'black'}:
            raise ValueError('colour must be {white, black}')
        else:
            self.colour = colour

    def __repr__(self):
        return f'BasePiece({repr(self.colour)})'

    def __str__(self):
        return f'{self.colour} {self.name}'

    def symbol(self):
        return f'{self.sym[self.colour]}'

    @staticmethod
    def vector(start, end):
        '''
        Return three values as a tuple:
        - x, the number of spaces moved horizontally,
        - y, the number of spaces moved vertically,
        - dist, the total number of spaces moved.
        positive integers indicate upward or rightward direction,
        negative integers indicate downward or leftward direction.
        dist is always positive.
        '''
        x = end[0] - start[0]
        y = end[1] - start[1]
        dist = abs(x) + abs(y)
        return x, y, dist



class King(BasePiece):
    name = 'king'
    sym = {'white': '♔', 'black': '♚'}

    def __repr__(self):
        return f"King('{self.name}')"

    def isvalid(self, start: tuple, end: tuple, empty):
        '''
        King can move one step in any direction
        horizontally, vertically, or diagonally.
        '''
        x, y, dist = self.vector(start, end)
        return (dist == 1) or (abs(x) == abs(y) == 1)


class Queen(BasePiece):
    name = 'queen'
    sym = {'white': '♕', 'black': '♛'}

    def __repr__(self):
        return f"Queen('{self.name}')"

    def isvalid(self, start: tuple, end: tuple, empty):
        '''
        Queen can move any number of steps horizontally,
        vertically, or diagonally.
        '''
        x, y, _ = self.vector(start, end)
        return (abs(x) == abs(y) != 0) \
               or ((abs(x) == 0 and abs(y) != 0) \
                   or (abs(y) == 0 and abs(x) != 0))


class Bishop(BasePiece):
    name = 'bishop'
    sym = {'white': '♗', 'black': '♝'}

    def __repr__(self):
        return f"Bishop('{self.name}')"

    def isvalid(self, start: tuple, end: tuple, empty):
        '''Bishop can move any number of steps diagonally.'''
        x, y, _ = self.vector(start, end)
        return (abs(x) == abs(y) != 0)


class Knight(BasePiece):
    name = 'knight'
    sym = {'white': '♘', 'black': '♞'}

    def __repr__(self):
        return f"Knight('{self.name}')"

    def isvalid(self, start: tuple, end: tuple, empty):
        '''
        Knight moves 2 spaces in any direction, and
        1 space perpendicular to that direction, in an L-shape.
        '''
        x, y, dist = self.vector(start, end)
        return (dist == 3) and (abs(x) != 3 and abs(y) != 3)


class Rook(BasePiece):
    name = 'rook'
    sym = {'white': '♖', 'black': '♜'}

    def __repr__(self):
        return f"Rook('{self.name}')"

    def isvalid(self, start: tuple, end: tuple, empty):
        '''
        Rook can move any number of steps horizontally
        or vertically.
        '''
        x, y, _ = self.vector(start, end)
        return (abs(x) == 0 and abs(y) != 0) \
               or (abs(y) == 0 and abs(x) != 0)


class Pawn(BasePiece):
    name = 'pawn'
    sym = {'white': '♙', 'black': '♟'}

    def __repr__(self):
        return f"Pawn('{self.name}')"


    def isvalid(self, start: tuple, end: tuple, empty):
        '''
        Pawn can only always move 1 step forward and 2 steps during the first move. Pawn can only capture diagonally forward.
        '''
        if self.colour == "black":
            if start[1] == 6:
                first_move = True
            else:
                first_move = False
        else:
            if start[1] == 1:
                first_move = True
            else:
                first_move = False
        x, y, dist = self.vector(start, end)

        if not first_move:
            if abs(x) < 2:
                if (empty and x == 0) or (not empty and abs(x) == 1):
                    if self.colour == 'black':
                        return (y == -1)
                    elif self.colour == 'white':
                        return (y == 1)
                    else:
                        return False
                return False
            return False
        else:
            if x == 0:
                if dist == 1:
                    if (empty and x == 0) or (not empty and abs(x) == 1):
                        if self.colour == 'black':
                            return (y == -1)
                        elif self.colour == 'white':
                            return (y == 1)
                        else:
                            return False
                    return False

                elif dist == 2:
                    if empty:
                        if self.colour == 'black':
                            return (y == -2)
                        elif self.colour == 'white':
                            return (y == 2)
                        else:
                            return False
                    return False
            return False 