class Player:
    def __init__(self):
        self.selection = 100
        self.valid_moves = []
        self.turn_step = 0
        self.turn_step_putting_poison = 0
        self.is_putting_poison_done = False
        self.can_add_values = False
        self.winner = None
        self.is_game_over = False
        self.round_counter = 1
        self.is_golden_eaten = False
        self.count_red_shield = 0
        self.count_green_shield = 0
        self.is_red_clue = False
        self.red_golden_clue_pos = []
        self.is_green_clue = False
        self.green_golden_clue_pos = []

    def reset(self):
        self.selection = 100
        self.valid_moves = []
        self.turn_step = 0
        self.turn_step_putting_poison = 0
        self.is_putting_poison_done = False
        self.can_add_values = False
        self.winner = None
        self.is_game_over = False
        self.round_counter = 1
        self.is_golden_eaten = False
        self.count_red_shield = 0
        self.count_green_shield = 0
        self.is_red_clue = False
        self.red_golden_clue_pos = []
        self.is_green_clue = False
        self.green_golden_clue_pos = []

    def select_piece(self, x, y):
        self.selection = (x, y)

    def add_valid_move(self, move):
        self.valid_moves.append(move)

    def switch_turn(self):
        self.turn_step = (self.turn_step + 1) % 4

    def set_winner(self, winner):
        self.winner = winner
        self.is_game_over = True

    def increment_round(self):
        self.round_counter += 1

    def consume_golden_apple(self):
        self.is_golden_eaten = True

    def add_red_shield(self):
        self.count_red_shield += 1

    def add_green_shield(self):
        self.count_green_shield += 1

    def set_red_clue(self, clue_pos):
        self.is_red_clue = True
        self.red_golden_clue_pos = clue_pos

    def set_green_clue(self, clue_pos):
        self.is_green_clue = True
        self.green_golden_clue_pos = clue_pos

    def clear_clues(self):
        self.is_red_clue = False
        self.red_golden_clue_pos = []
        self.is_green_clue = False
        self.green_golden_clue_pos = []
