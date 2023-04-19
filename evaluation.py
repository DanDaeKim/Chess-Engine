def evaluate(self):
        piece_values = {
            'P': 100, 'p': -100,
            'N': 320, 'n': -320,
            'B': 330, 'b': -330,
            'R': 500, 'r': -500,
            'Q': 900, 'q': -900,
            'K': 0, 'k': 0
        }

        # Piece square tables
        pawn_table = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        knight_table = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20, 0, 5, 5, 0, -20, -40],
            [-30, 5, 10, 15, 15, 10, 5, -30],
            [-30, 0, 15, 20, 20, 15, 0, -30],
            [-30, 5, 15, 20, 20, 15, 5, -30],
            [-30, 0, 10, 15, 15, 10, 0, -30],
            [-40, -20, 0, 0, 0, 0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ]

        bishop_table = [
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10, 5, 0, 0, 0, 0, 5, -10],
            [-10, 10, 10, 10, 10, 10, 10, -10],
            [-10, 0, 10, 10, 10, 10, 0, -10],
            [-10, 5, 5, 10, 10, 5, 5, -10],
            [-10, 0, 5, 10, 10, 5, 0, -10],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
        ]

        rook_table = [
            [0, 0, 0, 5, 5, 0, 0, 0],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [5, 10, 10, 10, 10, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        queen_table = [
            [-20, -10, -10, -5, -5, -10, -10, -20],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-10, 5, 5, 5, 5, 5, 0, -10],
            [0, 0, 5, 5, 5, 5, 0, -5],
            [0, 0, 5, 5, 5, 5, 0, -5],
            [-10, 0, 5, 5, 5, 5, 0, -10],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-20, -10, -10, -5, -5, -10, -10, -20]
        ]

        king_table = [
            [20, 30, 10, 0, 0, 10, 30, 20],
            [20, 20, 0, 0, 0, 0, 20, 20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30]
        ]
        
        score = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                value = piece_values[piece]

                # Add material balance
                score += value

                # Add piece positioning
                if piece == 'P':
                    score += pawn_table[row][col]
                elif piece == 'p':
                    score -= pawn_table[7 - row][col]
                elif piece == 'N':
                    score += knight_table[row][col]
                elif piece == 'n':
                    score -= knight_table[7 - row][col]
                elif piece == 'B':
                    score += bishop_table[row][col]
                elif piece == 'b':
                    score -= bishop_table[7 - row][col]
                elif piece == 'R':
                    score += rook_table[row][col]
                elif piece == 'r':
                    score -= rook_table[7 - row][col]
                elif piece == 'Q':
                    score += queen_table[row][col]
                elif piece == 'q':
                    score -= queen_table[7 - row][col]
                elif piece == 'K':
                    score += king_table[row][col]
                elif piece == 'k':
                    score -= king_table[7 - row][col]

                # Add pawn structure evaluation
                if piece in {'P', 'p'}:
                    # Example: Penalize doubled pawns
                    if 0 <= row - 1 < 8 and self.board[row - 1][col] == piece:
                        score -= 10 if piece == 'P' else 10

                # Add king safety evaluation
                if piece in {'K', 'k'}:
                    # Example: Encourage castling
                    if col == 2 or col == 6:
                        score += 15 if piece == 'K' else -15

        return score
