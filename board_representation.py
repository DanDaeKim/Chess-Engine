from moves import Move

class ChessBoard:
    def __init__(self):
        self.board = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]
        self.move_history = []
        self.white_to_move = True
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None

    def make_move(self, move):
        if self.is_valid_move(move):
            start_row, start_col = move.start
            target_row, target_col = move.target

            # Save the move data for unmake_move()
            self.move_history.append((move, self.board[target_row][target_col], self.en_passant_target))

            # Move the piece
            self.board[target_row][target_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = '-'

            # Update castling rights
            if self.board[target_row][target_col].lower() == 'k':
                self.castling_rights['K' if self.white_to_move else 'k'] = False
                self.castling_rights['Q' if self.white_to_move else 'q'] = False
            elif self.board[target_row][target_col].lower() == 'r':
                if start_row == 0 and start_col == 0:
                    self.castling_rights['Q'] = False
                elif start_row == 0 and start_col == 7:
                    self.castling_rights['K'] = False
                elif start_row == 7 and start_col == 0:
                    self.castling_rights['q'] = False
                elif start_row == 7 and start_col == 7:
                    self.castling_rights['k'] = False

            # Update en passant target
            self.en_passant_target = None
            if self.board[target_row][target_col].lower() == 'p' and abs(target_row - start_row) == 2:
                self.en_passant_target = ((start_row + target_row) // 2, target_col)

            # Switch the active player
            self.white_to_move = not self.white_to_move

    def unmake_move(self):
        if not self.move_history:
            return

        move, captured_piece, prev_en_passant_target = self.move_history.pop()
        start_row, start_col = move.start
        target_row, target_col = move.target

        # Move the piece back
        self.board[start_row][start_col] = self.board[target_row][target_col]
        self.board[target_row][target_col] = captured_piece

        # Restore castling rights and en passant target
        self.castling_rights = self.move_history[-1][0].castling_rights if self.move_history else {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = prev_en_passant_target

        # Switch the active player
        self.white_to_move = not self.white_to_move

    def is_valid_move(self, move):
        # This is a basic implementation of move validation
        # It does not account for all the rules of chess, such as checks, castling, en passant, etc.
        start_row, start_col = move.start
        target_row, target_col = move.target

        # Check if the starting square contains a piece
        if self.board[start_row][start_col] == '-':
            return False

        # Check if the piece belongs to the active player
        if self.white_to_move and self.board[start_row][start_col].islower():
            return False
        if not self.white_to_move and self.board[start_row][start_col].isupper():
            return False

        # Check if the target square is occupied by the active player's piece
        if self.white_to_move and self.board[target_row][target_col].isupper():
            return False
        if not self.white_to_move and self.board[target_row][target_col].islower():
            return False

        # Check if the move is valid based on the piece's movement rules
        piece = self.board[start_row][start_col].lower()
        row_diff = abs(target_row - start_row)
        col_diff = abs(target_col - start_col)

        if piece == 'p':  # Pawn
            if self.white_to_move:
                if col_diff == 0 and self.board[target_row][target_col] == '-' and start_row - target_row == 1:
                    return True
                if start_row == 6 and col_diff == 0 and self.board[target_row][target_col] == '-' and start_row - target_row == 2 and self.board[start_row - 1][start_col] == '-':
                    return True
                if col_diff == 1 and start_row - target_row == 1 and self.board[target_row][target_col].islower():
                    return True
            else:
                if col_diff == 0 and self.board[target_row][target_col] == '-' and target_row - start_row == 1:
                    return True
                if start_row == 1 and col_diff == 0 and self.board[target_row][target_col] == '-' and target_row - start_row == 2 and self.board[start_row + 1][start_col] == '-':
                    return True
                if col_diff == 1 and target_row - start_row == 1 and self.board[target_row][target_col].isupper():
                    return True

        elif piece == 'n':  # Knight
            if (row_diff == 1 and col_diff == 2) or (row_diff == 2 and col_diff == 1):
                return True

        elif piece == 'b':  # Bishop
            if row_diff == col_diff:
                row_step = 1 if target_row > start_row else -1
                col_step = 1 if target_col > start_col else -1
                for i in range(1, row_diff):
                    if self.board[start_row + i * row_step][start_col + i * col_step] != '-':
                        return False
                return True

        elif piece == 'r':  # Rook
            if row_diff == 0 or col_diff == 0:
                row_step = 0 if row_diff == 0 else (1 if target_row > start_row else -1)
                col_step = 0 if col_diff == 0 else (1 if target_col > start_col else -1)
                for i in range(1, max(row_diff, col_diff)):
                    if self.board[start_row + i * row_step][start_col + i * col_step] != '-':
                        return False
                return True

        elif piece == 'q':  # Queen
            # Combines the movement rules of a rook and a bishop
            if row_diff == col_diff or row_diff == 0 or col_diff == 0:
                row_step = 0 if row_diff == 0 else (1 if target_row > start_row else -1)
                col_step = 0 if col_diff == 0 else (1 if target_col > start_col else -1)
                elif piece == 'q':  # Queen
        # Combines the movement rules of a rook and a bishop
        if row_diff == col_diff or row_diff == 0 or col_diff == 0:
            row_step = 0 if row_diff == 0 else (1 if target_row > start_row else -1)
            col_step = 0 if col_diff == 0 else (1 if target_col > start_col else -1)
            for i in range(1, max(row_diff, col_diff)):
                if self.board[start_row + i * row_step][start_col + i * col_step] != '-':
                    return False
            return True

        elif piece == 'k':  # King
            if row_diff <= 1 and col_diff <= 1:
                return True

        return False

