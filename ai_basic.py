import random
import numpy as np

class MinesweeperAI:
    def __init__(self, rows, cols):
        # Initialize the agent
        self.rows = rows
        self.cols = cols
        self.q_table = {}  # This will store the Q-values for state-action pairs
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 1.0  # Exploration rate (higher means more exploration)
        self.max_epsilon = 1.0  # Maximum exploration rate
        self.min_epsilon = 0.1  # Minimum exploration rate
        self.epsilon_decay = 0.995  # Decay factor for epsilon

    def get_state_key(self, revealed):
        """Generate a unique state representation from the revealed grid."""
        return tuple(tuple(row) for row in revealed)
    
    def choose_move(self, revealed):
        """Choose the next move based on the Q-table using epsilon-greedy."""
        state_key = self.get_state_key(revealed)
        
        if random.uniform(0, 1) < self.epsilon:
            # Exploration: Choose a random move
            valid_moves = [(r, c) for r in range(self.rows) for c in range(self.cols) if not revealed[r][c]]
            if valid_moves:
                return random.choice(valid_moves)
        else:
            # Exploitation: Choose the best known move
            if state_key not in self.q_table:
                return None  # No moves if state is unknown yet
            q_values = self.q_table[state_key]
            best_move = max(q_values, key=q_values.get, default=None)
            return best_move
    
    def update(self, prev_revealed, move, reward, revealed):
        """Update the Q-table using the Q-learning formula."""
        state_key = self.get_state_key(prev_revealed)
        next_state_key = self.get_state_key(revealed)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        
        if move not in self.q_table[state_key]:
            self.q_table[state_key][move] = 0.0  # Initialize Q-value if not present
        
        # Q-learning formula: Q(s, a) = Q(s, a) + alpha * (reward + gamma * max(Q(s', a')) - Q(s, a))
        future_reward = max(self.q_table.get(next_state_key, {}).values(), default=0)
        self.q_table[state_key][move] += self.alpha * (reward + self.gamma * future_reward - self.q_table[state_key][move])
    
    def reset_model(self):
        """Reset the Q-table and learning parameters to start fresh."""
        self.q_table = {}
        self.epsilon = self.max_epsilon  # Reset epsilon to maximum for fresh exploration
        self.alpha = 0.1  # Reset learning rate
        self.gamma = 0.9  # Reset discount factor
        print("Model reset!")
    
    def decay_epsilon(self):
        """Decay epsilon after each episode to move from exploration to exploitation."""
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
    
    def save_model(self, filename="q_table.npy"):
        """Save the Q-table to a file."""
        np.save(filename, self.q_table)
    
    def load_model(self, filename="q_table.npy"):
        """Load the Q-table from a file."""
        try:
            self.q_table = np.load(filename, allow_pickle=True).item()
            print("Model loaded successfully!")
        except FileNotFoundError:
            print("No pre-trained model found, starting fresh.")
    
    def get_valid_moves(self, revealed):
        """Helper function to get all valid moves (unrevealed cells)."""
        return [(r, c) for r in range(self.rows) for c in range(self.cols) if not revealed[r][c]]
