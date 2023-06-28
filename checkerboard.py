import pygame

# dimensions/sizes of board components
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE = WIDTH/ROWS

# main colors
WHITE = (255,243,255)
BLACK = (0,0,0)
PURPLE = (131,91,134)
HIGHLIGHT = (239, 239, 53)

window = pygame.display.set_mode((800, 600))

# load piece images
CROWN = pygame.transform.scale(pygame.image.load("images/crown.png").convert_alpha(), (40,40))
TRIPLE_CROWN = pygame.transform.scale(pygame.image.load("images/triple_crown.png").convert_alpha(), (50,50))

class CheckerBoard:
    def __init__(self):
        self.board = [
            [None, "White", None, "White", None, "White", None, "White"],
            ["White", None, "White", None, "White", None, "White", None],
            [None, "White", None, "White", None, "White", None, "White"],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ["Black", None, "Black", None, "Black", None, "Black", None],
            [None, "Black", None, "Black", None, "Black", None, "Black"],
            ["Black", None, "Black", None, "Black", None, "Black", None]
            ]
        
        # piece stats
        self.white = {
                "captured": 0,
                "kings": 0,
                "triple_kings": 0,
                "last_turn": None,
                "turn_capture": False
                }

        self.black = {
                "captured": 0,
                "kings": 0,
                "triple_kings": 0,
                "last_turn": None,
                "turn_capture": False
                }
            
    def draw_board(self):
        """
        Creates and displays all components of game screen.
        """
        window.fill(PURPLE)
        for row in range(len(self.board)):
            for col in range(row % 2, ROWS, 2):
                # draw white square in every other column
                pygame.draw.rect(window, WHITE, (row*SQUARE, col*SQUARE, SQUARE, SQUARE))
        
        self.draw_piece()

        # for display text on right side
        self.display_stats("White")
        self.display_stats("Black")
        self.game_winner()
 
    def display_stats(self, color):
        """
        Displays count of captured pieces, kings, and triple kings each color has.
        """
        # headers
        if color == "White":
            font = pygame.font.Font('freesansbold.ttf', 28)
            text = font.render('White', True, WHITE, None)
            window.blit(text, (665, 25))

            # set coordinates for where to display counts
            x = 625
            y = 40

            stats = self.white
            font_color = WHITE
        else: 
            font = pygame.font.Font('freesansbold.ttf', 28)
            text = font.render('Black', True, BLACK, None)
            window.blit(text, (665, 450))

            x = 625
            y = 465

            stats = self.black
            font_color = BLACK

        for key, val in stats.items():
            font = pygame.font.Font('freesansbold.ttf', 16)
            if key == "captured":
                key_val = "Captured Pieces = " + str(val)
            elif key == "kings":
                key_val = "# of Kings = " + str(val)
            elif key == "triple_kings":
                key_val = "# of Triple Kings = " + str(val)
            else: 
                continue
            # render each line of text below the previous text
            text = font.render(key_val, True, font_color, None)
            y += 20
            window.blit(text, (x,y))

    def draw_piece(self):
        """
        Creates and displays each piece on board.
        """
        for row in range(len(self.board)):
            for col in range(COLS):
                if self.board[row][col] is not None: 
                    # draw circles on designated positions on board
                    if "White" in self.board[row][col]:
                        pygame.draw.circle(window, WHITE, (SQUARE * col + SQUARE//2, SQUARE * row + SQUARE//2), 35)
                    elif "Black" in self.board[row][col]:
                        pygame.draw.circle(window, BLACK, (SQUARE * col + SQUARE//2, SQUARE * row + SQUARE//2), 35)

                    if "_king" in self.board[row][col]:
                        # add crown to base piece
                        window.blit(CROWN, (75*col+75//2-20, 75*row+75//2-20))
                    elif "White_Triple_King" in self.board[row][col]:
                        # redraw base piece to remove king's crown, then add triple crown
                        pygame.draw.circle(window, WHITE, (75*col+75//2, 75*row+75//2), 35)
                        window.blit(TRIPLE_CROWN, (75*col+75//2-25, 75*row+75//2-30))
                    elif "Black_Triple_King" in self.board[row][col]:
                        pygame.draw.circle(window, BLACK, (75*col+75//2, 75*row+75//2), 35)
                        window.blit(TRIPLE_CROWN, (75*col+75//2-25, 75*row+75//2-30))

                    if "click" in self.board[row][col]:
                        # draw highlight around circle
                        pygame.draw.circle(window, HIGHLIGHT, (75*col+75//2, 75*row+75//2), 35, 4)
                
    def check_turn(self, piece, turn_count):
        """
        Checks whether it is the given piece's turn.
        """
        if "Black" in piece:
            player = self.black
        else:
            player = self.white

        if player["last_turn"] == turn_count - 1 and player["turn_capture"] == False:
            return False

        return True

    def set_turn(self, piece, turn_count):
        """
        Updates the given piece's stats to show which color just had their turn.
        """
        if "Black" in piece:
            player = self.black
        else:
            player = self.white

        player["last_turn"] = turn_count

    def move(self, start_row, start_col, dest_row, dest_col):
        """
        Moves piece from start location to destination location. 
        Updates start location to show None.
        """
        self.board[dest_row][dest_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None

    def highlight(self, row, col):
        """
        Updates piece name on board to indicate that a piece is highlighted.
        """
        if "click" not in self.board[row][col]:
            self.board[row][col] += "_click"
        elif "click" in self.board[row][col]:
            self.board[row][col] = self.board[row][col].replace("_click", "")

    def get_checker_details(self, row, col):
        """
        Returns a string containing the name/type of a piece at a given location on the board
        """
        return self.board[row][col]

    def check_coordinates(self, row, col):
        """
        Checks if given coordinates are valid on the checker board.
        """
        if not row % 2 == 0 and col % 2 == 1:
            # even rows have dark squares only in odd-numbered positions
            return False
        elif not row % 2 == 1 and col % 2 == 0:
            # odd rows have dark squares only in even-numbered positions
            return False
            
        return True

    def validate_regular_move(self, start_row, start_col, dest_row, dest_col, piece):
        """
        Checks whether the given start and end coordinates constitute a valid move made by a normal piece.
        """
        if "Black" in piece:
            enemy_color = "White"
            player = self.black
        else:
            enemy_color = "Black"
            player = self.white

        vert_difference = dest_row - start_row
        horiz_difference = dest_col - start_col

        if ("Black" in piece and vert_difference > 0) or ("White" in piece and vert_difference < 0):
            # piece cannot move backwards
            return False

        if abs(vert_difference) == 1 and abs(horiz_difference) == 1:
            # single jump
            player["turn_capture"] = False
            return True

        elif abs(vert_difference) > 2 and abs(horiz_difference) > 2:
            # normal piece can't jump over more than 1 square per turn
            return False

        # check squares in between start and destination
        middle_row = start_row
        middle_col = start_col

        if vert_difference < 0:
            middle_row -= 1
        elif vert_difference > 0:
            middle_row += 1
        else:
            return False
            
        if horiz_difference < 0:
            middle_col -= 1
        elif horiz_difference > 0:
            middle_col += 1
        else:
            return False

        if self.board[middle_row][middle_col] is None or enemy_color not in self.board[middle_row][middle_col]:
            # cannot jump more than 1 square if not capturing an enemy piece
            return False
        self.what_is_captured(middle_row, middle_col, piece)

        player["turn_capture"] = True
        player["captured"] += 1  # add 1 to player's total captured piece count
        return True

    def validate_king_move(self, start_row, start_col, dest_row, dest_col, piece):
        """
        Checks whether the given start and end coordinates constitute a valid move made by a king.
        """
        if "Black" in piece:
            enemy_color = "White"
            player = self.black
        else:
            enemy_color = "Black"
            player = self.white

        vert_difference = dest_row - start_row
        horiz_difference = dest_col - start_col

        if abs(vert_difference) == 1 and abs(horiz_difference) == 1:
            # single jump
            player["turn_capture"] = False
            return True

        elif abs(vert_difference) == abs(horiz_difference):
            # jump along a diagonal path
            middle_row = start_row
            middle_col = start_col
            captured_piece_count = 0

            # jump along straight diagonal path from start
            for i in range(abs(vert_difference)):
                if vert_difference < 0:
                    middle_row -= 1
                else:
                    middle_row += 1

                if horiz_difference < 0:
                    middle_col -= 1
                else:
                    middle_col += 1

                if self.board[middle_row][middle_col] is None:           # empty square
                    continue
                elif enemy_color in self.board[middle_row][middle_col]:  # enemy piece captured
                    captured_piece_count += 1
                    enemy_row, enemy_col = middle_row, middle_col
                else:  
                    # cannot jump over friendly piece
                    return False

            # king can only capture 1 piece per turn
            # king can only jump multiple spaces if capturing piece
            if captured_piece_count > 1 or captured_piece_count == 0:
                return False

            # remove captured piece
            self.what_is_captured(enemy_row, enemy_col, piece)
            player["turn_capture"] = True
            player["captured"] += captured_piece_count  # add to player's total captured piece count
            return True

    def validate_triple_king_move(self, start_row, start_col, dest_row, dest_col, piece):
        """
        Checks whether the given start and end coordinates constitute a valid move made by a triple king.
        """
        if "Black" in piece:
            player = self.black
            color = "Black"
        else:
            player = self.white
            color = "White"
            
        vert_difference = dest_row - start_row
        horiz_difference = dest_col - start_col

        if abs(vert_difference) == 1 and abs(horiz_difference) == 1:
            # single jump
            player["turn_capture"] = False
            return True

        elif abs(vert_difference) == abs(horiz_difference):
            middle_row = start_row
            middle_col = start_col
            captured_piece_count = 0
            friendly_piece_count = 0
            captured_squares = []

            # jump along straight diagonal path from start
            for i in range(abs(vert_difference)):
                if vert_difference < 0:
                    middle_row -= 1
                else:
                    middle_row += 1

                if horiz_difference < 0:
                    middle_col -= 1
                else:
                    middle_col += 1

                if self.board[middle_row][middle_col] is None:             # empty square
                    continue
                elif color in self.board[middle_row][middle_col]:          # friendly piece
                    friendly_piece_count += 1
                else:                                                       # enemy piece
                    captured_piece_count += 1
                    captured_squares.append((middle_row, middle_col))

                if captured_piece_count > 2:                                # can't capture more than 2 pieces per turn
                    return False
                if captured_piece_count > 0 and friendly_piece_count > 0:   # can't jump over both friend and enemy
                    return False

            for coordinates in captured_squares:
                row, col = coordinates
                self.what_is_captured(row, col, color)

            # set whether a player can go again next turn
            if captured_piece_count > 0:
                player["turn_capture"] = True
            else:
                player["turn_capture"] = False

            player["captured"] += captured_piece_count                      # add to player's total captured piece count
            return True

    def what_is_captured(self, row, col, color):
        """
        Checks what type of piece is at a given location and removes the piece from the board.
        If the piece is a special piece, updates the piece color's king and/or triple king count accordingly.
        """
        captured_piece = self.get_checker_details(row, col)

        if "Black" in color:
            enemy = self.white
        else:
            enemy = self.black

        if "Triple" in captured_piece:
            enemy["triple_kings"] -= 1
        elif "king" in captured_piece:
            enemy["kings"] -= 1

        # remove captured piece from board
        self.board[row][col] = None

    def promotion(self, dest_row, start_row, start_col, piece):
        """
        Promotes a regular piece to a king or a king to a triple king.
        """
        if dest_row == 0 and ("Black" not in piece and "White_king" not in piece):
            return
        elif dest_row == 7 and ("White" not in piece and "Black_king" not in piece):
            return

        if "Black" in piece:
            player = self.black
        else:
            player = self.white

        if "king" in piece: 
            # promote king to triple king                        
            player["triple_kings"] += 1             # increase triple king count
            player["kings"] -= 1                    # decrease king count
            self.board[start_row][start_col] = self.board[start_row][start_col].replace("_king", "_Triple_King")
        else:
            # promote normal piece to king                                       
            player["kings"] += 1
            self.board[start_row][start_col] += "_king"

    def game_winner(self):
        """
        Checks whether either side has won. Displays text declaring winner if there is a winner.
        """
        font = pygame.font.Font('freesansbold.ttf', 50)

        if self.white["captured"] == 12:
            text = font.render('WHITE', True, HIGHLIGHT, None)
            window.blit(text, (615, 200))
        elif self.black["captured"] == 12:
            text = font.render('BLACK', True, HIGHLIGHT, None)
            window.blit(text, (615, 200))
        else:
            return

        text = font.render('WINS!', True, HIGHLIGHT, None)
        window.blit(text, (630, 275))