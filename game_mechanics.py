import pygame

class Game:
    def __init__(self, board) -> None:
        self.board = board
        self.turn_count = 0
    
    def first_click(self, mouse_location):
        """
        Determines whether a piece has been clicked. Returns new start_location to indicate to main that
        next click will be associated with the piece chosen with this click.
        """
        board = self.board

        # translate mouse coordinates with row and column on board
        location = tuple(map(lambda x: x // 75, mouse_location))
        start_col, start_row = location

        if start_col > 7 or start_row > 7:
            # click location is outside of checkerboard
            return None
        else:
            piece = board.get_checker_details(start_row, start_col)
            # check if selected square contains a piece and it's that piece color's turn
            if piece is not None and board.check_turn(piece, self.turn_count) is True:
                start_location = (start_col, start_row)
                board.highlight(start_row, start_col)

                return start_location

    def second_click(self, start_location, mouse_location):
        """
        Determines whether a piece has been clicked. Returns new start_location to indicate to main that
        next click will be associated with the piece chosen with this click.
        """
        board = self.board
        dest_location = tuple(map(lambda x: x // 75, mouse_location))
        dest_col, dest_row = dest_location
        start_col, start_row = start_location
        piece = board.get_checker_details(start_row, start_col)

        if dest_col > 7 or dest_row > 7:
            # exit out of function while preserving given start_location
            return start_location
        else:
            # check move validity
            # 1. check if moving to empty dark square only
            if board.check_coordinates(dest_row, dest_col) and board.get_checker_details(dest_row, dest_col) is None:
                # 2. validate move based on piece type
                validity = self.move_validity(start_row, start_col, dest_row, dest_col, piece)

                if validity is True:
                    # check if piece gets promoted
                    if dest_row == 0 or dest_row == 7:
                        board.promotion(dest_row, start_row, start_col, piece)

                    # finally move piece
                    board.move(start_row, start_col, dest_row, dest_col)
                    board.highlight(dest_row, dest_col)

                    # indicate which color went this turn
                    board.set_turn(piece, self.turn_count)
                    self.turn_count += 1

                else:
                    # undo highlight
                    board.highlight(start_row, start_col)
            else:
                board.highlight(start_row, start_col)

        return None       # clear click sequence

    def move_validity(self, start_row, start_col, dest_row, dest_col, piece):
        """
        Checks if a piece's movement is valid. Returns True or False.
        """
        board = self.board

        if "Triple_King" in board.get_checker_details(start_row, start_col):
            return board.validate_triple_king_move(start_row, start_col, dest_row, dest_col, piece)
        elif "king" in board.get_checker_details(start_row, start_col):
            return board.validate_king_move(start_row, start_col, dest_row, dest_col, piece)
        else:
            return board.validate_regular_move(start_row, start_col, dest_row, dest_col, piece)