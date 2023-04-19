class Move:
  def __init__(self, start, target):
          self.start = start
          self.target = target

  def is_king_in_check(self):
          king_square = None
          for row in range(8):
              for col in range(8):
                  piece = self.board[row][col]
                  if (self.white_to_move and piece == 'K') or (not self.white_to_move and piece == 'k'):
                      king_square = (row, col)
                      break
              if king_square is not None:
                  break

          for move in self.generate_moves():
              if move.target == king_square:
                  return True
          return False

  def generate_moves(self):
          moves = []

          for row in range(8):
              for col in range(8):
                  piece = self.board[row][col]

                  if (self.white_to_move and piece.isupper()) or (not self.white_to_move and piece.islower()):
                      piece_type = piece.lower()

                      if piece_type == 'p':
                          moves.extend(self.generate_pawn_moves(row, col))
                      elif piece_type == 'n':
                          moves.extend(self.generate_knight_moves(row, col))
                      elif piece_type == 'b':
                          moves.extend(self.generate_bishop_moves(row, col))
                      elif piece_type == 'r':
                          moves.extend(self.generate_rook_moves(row, col))
                      elif piece_type == 'q':
                          moves.extend(self.generate_queen_moves(row, col))
                      elif piece_type == 'k':
                          moves.extend(self.generate_king_moves(row, col))

          return moves

      def generate_pawn_moves(self, row, col):
        legal_moves = []
        moves = []
        if self.white_to_move:
            if row > 0 and self.board[row - 1][col] == '-':
                moves.append(Move((row, col), (row - 1, col)))
                if row == 6 and self.board[row - 2][col] == '-':
                    moves.append(Move((row, col), (row - 2, col)))
            if col > 0 and row > 0 and self.board[row - 1][col - 1].islower():
                moves.append(Move((row, col), (row - 1, col - 1)))
            if col < 7 and row > 0 and self.board[row - 1][col + 1].islower():
                moves.append(Move((row, col), (row - 1, col + 1)))
        else:
            if row < 7 and self.board[row + 1][col] == '-':
                moves.append(Move((row, col), (row + 1, col)))
                if row == 1 and self.board[row + 2][col] == '-':
                    moves.append(Move((row, col), (row + 2, col)))
            if col > 0 and row < 7 and self.board[row + 1][col - 1].isupper():
                moves.append(Move((row, col), (row + 1, col - 1)))
            if col < 7 and row < 7 and self.board[row + 1][col + 1].isupper():
                moves.append(Move((row, col), (row + 1, col + 1)))
        for move in moves:
          self.make_move(move)
          if not self.is_king_in_check():
              legal_moves.append(move)
          self.unmake_move()

        return legal_moves


      def generate_knight_moves(self, row, col):
          legal_moves = []
          moves = []
          directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
          for dr, dc in directions:
              new_row, new_col = row + dr, col + dc
              if 0 <= new_row < 8 and 0 <= new_col < 8:
                  target_piece = self.board[new_row][new_col]
                  if target_piece == '-' or (self.white_to_move and target_piece.islower()) or (not self.white_to_move and target_piece.isupper()):
                      moves.append(Move((row, col), (new_row, new_col)))
          for move in moves:
          self.make_move(move)
          if not self.is_king_in_check():
              legal_moves.append(move)
          self.unmake_move()

          return legal_moves

      def generate_bishop_moves(self, row, col):
        legal_moves = []
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = self.board[new_row][new_col]
                if target_piece == '-' or (self.white_to_move and target_piece.islower()) or (not self.white_to_move and target_piece.isupper()):
                    moves.append(Move((row, col), (new_row, new_col)))
                    if target_piece != '-':
                        break
                else:
                    break
                new_row += dr
                new_col += dc

        for move in moves:
            self.make_move(move)
            if not self.is_king_in_check():
                legal_moves.append(move)
            self.unmake_move()

        return legal_moves

      def generate_rook_moves(self, row, col):
        legal_moves = []
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = self.board[new_row][new_col]
                if target_piece == '-' or (self.white_to_move and target_piece.islower()) or (not self.white_to_move and target_piece.isupper()):
                    moves.append(Move((row, col), (new_row, new_col)))
                    if target_piece != '-':
                        break
                else:
                    break
                new_row += dr
                new_col += dc

        for move in moves:
            self.make_move(move)
            if not self.is_king_in_check():
                legal_moves.append(move)
            self.unmake_move()

        return legal_moves

    def generate_queen_moves(self, row, col):
        return self.generate_rook_moves(row, col) + self.generate_bishop_moves(row, col)

    def generate_king_moves(self, row, col):
        legal_moves = []
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = self.board[new_row][new_col]
                if target_piece == '-' or (self.white_to_move and target_piece.islower()) or (not self.white_to_move and target_piece.isupper()):
                    moves.append(Move((row, col), (new_row, new_col)))

        for move in moves:
            self.make_move(move)
            if not self.is_king_in_check():
                legal_moves.append(move)
            self.unmake_move()

        return legal_moves



