import numpy as np
import pandas as pd

class BayesianAgent:
    def __init__(self, player_color, apple_values, locations, clues_pos):
        self.player_color = player_color
        self.apple_values = apple_values
        self.clues_pos = clues_pos 
        self.locations = set(locations)
        self.grid_size = 8  # Assuming an 8x8 grid

        # Initialize probabilities uniformly (no information initially)
        self.probabilities = np.zeros((self.grid_size, self.grid_size))
        self.probabilities[1][2] = 0.0
        self.probabilities[2][1] = 0.0
        self.probabilities[0][0] = 0.0
        self.probabilities[6][5] = 0.0
        self.probabilities[5][6] = 0.0
        self.probabilities[7][7] = 0.0
        self.sure_not_poison = [(1,2), (2,1), (0,0), (6,5), (5,6), (7,7)] + self.clues_pos
        

    def update_clue_probabilities(self, revealed_apple_location):
        print(f"revealed location: {revealed_apple_location}")
        x, y = revealed_apple_location
        self.probabilities[x][y] = 0.0
        adjacent_cells = [
            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)
        ]
        
        if self.player_color == 'green':
            adjacent_cells = [(px, py) for px, py in adjacent_cells if 0 <= px <= 3  and 0 <= py < self.grid_size and (px, py)]
            print(f'Adjacent cells: {adjacent_cells}')
            denom = len(adjacent_cells)
            numerator = len(set(adjacent_cells).difference(set(self.sure_not_poison)))
            possible_poison = set(adjacent_cells).difference(set(self.sure_not_poison))
            probability = 1/numerator

        
            for cell in possible_poison:
                i, j = cell
                self.probabilities[j][i] += probability
                
        else: # red player that is finding the green poison location
            adjacent_cells = [(px, py) for px, py in adjacent_cells if 4 <= px <= 7  and 0 <= py < self.grid_size and (px, py)]
            denom = len(adjacent_cells)
            numerator = len(set(adjacent_cells).difference(set(self.sure_not_poison)))
            possible_poison = set(adjacent_cells).difference(set(self.sure_not_poison))
            probability = 1/numerator
            
            for cell in possible_poison:
                i, j = cell
                self.probabilities[j][i] += probability
                    
        print(f"Possible poison location: {possible_poison}")
        print("Probabilities")
        df = pd.DataFrame(self.probabilities)
        print(df)

    
    def update_probability(self, revealed_apple_location):
        x, y = revealed_apple_location
        self.probabilities[x][y] = 0.0
        self.sure_not_poison.append(revealed_apple_location)
        adjacent_cells = [
            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)
        ]

        if self.player_color == 'green':
            adjacent_cells = [(px, py) for px, py in adjacent_cells if 0 <= px <= 3  and 0 <= py < self.grid_size and (px, py)]
            for cell in adjacent_cells:
                if cell in self.clues_pos:
                    self.update_clue_probabilities(cell)
                

        else: # red player that is finding the green poison location
            adjacent_cells = [(px, py) for px, py in adjacent_cells if 4 <= px <= 7  and 0 <= py < self.grid_size and (px, py)]
              
        df = pd.DataFrame(self.probabilities)
        print(df)


        
    def draw_possible_poison_locations(self):
        # Create a grid to visualize possible poison locations
        grid_with_poison = np.zeros((self.grid_size, self.grid_size))
        
        # Get indices of the top 4 highest probabilities
        flat_probs = np.array(self.probabilities).flatten()
        top_indices = np.argpartition(flat_probs, -4)[-4:]

        # Set the top 4 probabilities to 1 in the grid
        for idx in top_indices:
            x, y = np.unravel_index(idx, self.probabilities.shape)
            grid_with_poison[x, y] = 1
        
        print("Grid with Possible Poison Locations (Top 4 Probabilities):")
        print(grid_with_poison)


    def infer_next_move(self):
        max_prob = np.max(self.probabilities)
        next_moves = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.probabilities[x, y] == max_prob:
                    next_moves.append((x, y))
        return next_moves

class MinimaxAgent(BayesianAgent):
    def __init__(self, player_color, apple_values, locations, clues_pos):
        super().__init__(player_color, apple_values, locations, clues_pos)
    
    def minimax_action(self, valid_moves):
        best_action = None
        best_value = -float('inf')
        
        for cell in valid_moves:
            x, y = cell
                
            # Calculate value for this action
            value = self.calculate_value(cell)
            
            # Update best action if this one is better
            if value > best_value:
                best_value = value
                best_action = (x, y)
        
        return best_action
    
    def calculate_value(self, action):
        x, y = action
        # Calculate value based on the probability of getting a poison and apple value
        probability = self.probabilities[y][x]
        apple_value = self.apple_values.get((x, y), 0)
        
        # Inverse probability (lower is better for poison) and apple value
        value = 1.0 / (1.0 + probability) + apple_value
        
        return value
    
    
# Example usage:
if __name__ == '__main__':
    red_poison_locations = [(2, 2), (1, 4), (3, 4), (1, 7)]  # Example initial positions of red poisons
    red_apple_values = {(3, 1): 1, (0, 3): 1, (3, 3): 1, (2, 7): 1, (1, 0): 5, (2, 0): 2, (3, 0): 9, (0, 1): 3, (1, 1): 6, (2, 1): 3, (0, 2): 9, (1, 2): 2, (2, 2): 2, (3, 2): 9, (1, 3): 9, (2, 3): 8, (0, 4): 4, (1, 4): 8, (2, 4): 5, (3, 4): 6, (0, 5): 2, (1, 5): 7, (2, 5): 2, (3, 5): 8, (0, 6): 2, (1, 6): 7, (2, 6): 9, (3, 6): 9, (0, 7): 6, (1, 7): 5, (3, 7): 7}
    red_locations = [(x, y) for y in range(8) for x in range(4)]
    red_apple_clues_pos = [pos for pos, val in red_apple_values.items() if val == 1]

    green_poison_locations = [(4, 4), (6, 4), (6, 5), (5, 6)]  # Example initial positions of green poisons
    green_apple_values = {(5, 4): 1, (7, 5): 1, (5, 5): 1, (6, 7): 1, (4, 0): 3, (5, 0): 3, (6, 0): 2, (7, 0): 7, (4, 1): 5, (5, 1): 6, (6, 1): 3, (7, 1): 9, (4, 2): 3, (5, 2): 7, (6, 2): 9, (7, 2): 3, (4, 3): 6, (5, 3): 6, (6, 3): 8, (7, 3): 2, (4, 4): 3, (6, 4): 8, (7, 4): 2, (4, 5): 6, (6, 5): 7, (4, 6): 7, (5, 6): 9, (6, 6): 8, (7, 6): 7, (4, 7): 3, (5, 7): 3}
    green_locations = [(x, y) for y in range(8) for x in range(4, 8)]
    green_apple_clues_pos = [pos for pos, val in green_apple_values.items() if val == 1]

    # Initialize Bayesian agents for red and green players
    # red_bayesian_agent = BayesianAgent('red', red_apple_values, red_locations)
    green_bayesian_agent = MinimaxAgent('green', red_apple_values, red_locations, red_apple_clues_pos)

    # Example update based on revealed apple location (just for demonstration)
    # red_bayesian_agent.update_probabilities((4, 5))
    for clue_pos in red_apple_clues_pos:
        green_bayesian_agent.update_clue_probabilities(clue_pos)

    # Draw possible poison locations for both agents
    # print("Red Player's Poison Locations:")
    # red_bayesian_agent.draw_possible_poison_locations()
    valid_moves = [(6,5), (5,6)]
    print("Red Player's Poison Locations:")
    green_bayesian_agent.draw_possible_poison_locations()
    best_action = green_bayesian_agent.minimax_action(valid_moves)
    print(f"Best Action chosen by Minimax: {best_action}")
