class ChessEngine:
    def __init__(self, board, time_management):
        self.board = board
        self.time_manager = time_manager
        self.transposition_table = {}
        
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

