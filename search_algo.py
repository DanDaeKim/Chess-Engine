from opening_book import opening_book

class ChessEngine:
    def __init__(self, board, time_management):
        self.board = board
        self.time_manager = time_manager
        self.transposition_table = {}
        
    def make_move(self):
        num_moves_left = self.estimate_moves_left()
        time_for_move = self.time_manager.time_for_move(num_moves_left)
        best_move = self.find_best_move(max_depth, time_limit=time_for_move)
        self.board.make_move(best_move)
        
    def estimate_moves_left(self):
        num_pieces, num_pawns, material_balance = self.analyze_position()
        phase_factor = self.calculate_phase_factor(num_pieces, num_pawns, material_balance)

        if phase_factor < 0.3:
            return 50  # Opening phase
        elif phase_factor < 0.7:
            return 35  # Middle game
        else:
            return 20  # Endgame

    def analyze_position(self):
        num_pieces = 0
        num_pawns = 0
        material_balance = 0

        piece_values = {'P': 1, 'p': -1, 'N': 3, 'n': -3, 'B': 3, 'b': -3,
                        'R': 5, 'r': -5, 'Q': 9, 'q': -9, 'K': 0, 'k': 0}

        for row in self.board.board:
            for piece in row:
                if piece != '-':
                    num_pieces += 1
                    material_balance += piece_values[piece]

                    if piece.upper() == 'P':
                        num_pawns += 1

        return num_pieces, num_pawns, material_balance

    def calculate_phase_factor(self, num_pieces, num_pawns, material_balance):
        max_pieces = 32
        max_pawns = 16
        max_material_balance = 72  # 2 knights, 2 bishops, 2 rooks, 1 queen, 8 pawns for each side

        piece_factor = num_pieces / max_pieces
        pawn_factor = num_pawns / max_pawns
        material_factor = (material_balance + max_material_balance) / (2 * max_material_balance)

        return (piece_factor + pawn_factor + material_factor) / 3


    def order_moves(self, moves):
        # Sort moves based on a simple heuristic or previous search results
        # For example, you can sort the moves based on captures first
        return sorted(moves, key=lambda move: self.board.is_capture(move), reverse=True)


    def alpha_beta_search(self, depth, alpha, beta, maximizing_player):
        zobrist_hash = self.board.zobrist_hash()
        if zobrist_hash in self.transposition_table:
            tt_entry = self.transposition_table[zobrist_hash]
        if tt_entry['depth'] >= depth:
            return tt_entry['score']

        if depth == 0 or self.board.is_game_over():
            return self.board.evaluate_board()
        if depth == 0 or self.board.is_game_over():
            return self.board.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.board.generate_legal_moves():
                self.board.make_move(move)
                eval = self.alpha_beta_search(depth - 1, alpha, beta, False)
                self.board.unmake_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.board.generate_legal_moves():
                self.board.make_move(move)
                eval = self.alpha_beta_search(depth - 1, alpha, beta, True)
                self.board.unmake_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval
        self.transposition_table[zobrist_hash] = {'depth': depth, 'score': best_score}
        return best_score
        
    def find_best_move(self, max_depth, time_limit=None):
        best_move = None
        start_time = time.time()

        for depth in range(1, max_depth + 1):
            best_move = self.find_best_move_at_depth(depth)
            if time_limit and (time.time() - start_time) >= time_limit:
                break

        return best_move

    def find_best_move_at_depth(self, depth):
        best_eval = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        legal_moves = self.order_moves(self.board.generate_legal_moves())
        for move in legal_moves:
            self.board.make_move(move)
            eval = self.alpha_beta_search(depth - 1, alpha, beta, False)
            self.board.unmake_move()
            if eval > best_eval:
                best_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff

    return best_move

