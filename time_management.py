import time

class TimeManager:
    def __init__(self, total_time, increment):
        self.total_time = total_time
        self.increment = increment
        self.start_time = time.time()

    def remaining_time(self):
        return self.total_time - (time.time() - self.start_time)

    def time_for_move(self, num_moves_left):
        remaining = self.remaining_time()
        time_per_move = (remaining / num_moves_left) + self.increment
        return time_per_move
