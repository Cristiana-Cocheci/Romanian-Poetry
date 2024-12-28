import numpy as np
import tensorflow as tf
from keras import layers, models
from collections import deque
import random

class DQLAgent:
    def __init__(self, state_size, action_size, learning_rate=0.001, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        """
        Initialize the DQL Agent.

        Args:
            state_size: Size of the state space.
            action_size: Size of the action space (vocabulary size).
            learning_rate: Learning rate for the Q-network.
            gamma: Discount factor for future rewards.
            epsilon: Initial exploration rate.
            epsilon_decay: Decay rate for epsilon.
            epsilon_min: Minimum exploration rate.
        """
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        # Replay buffer for experience replay
        self.memory = deque(maxlen=2000)

        # Q-network and target network
        self.q_network = self.build_model()
        self.target_network = self.build_model()
        self.update_target_network()

    def build_model(self):
        """
        Build the Q-network.
        """
        model = models.Sequential([
            layers.Input(shape=(self.state_size,)),
            layers.Dense(128, activation="relu"),
            layers.Dense(64, activation="relu"),
            layers.Dense(self.action_size, activation="linear")  # Output Q-values for all actions
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate), loss="mse")
        return model

    def update_target_network(self):
        """
        Copy weights from the Q-network to the target network.
        """
        self.target_network.set_weights(self.q_network.get_weights())

    def act(self, state):
        """
        Choose an action based on the current state and epsilon-greedy policy.

        Args:
            state: Current state.

        Returns:
            action: Index of the chosen word in the vocabulary.
        """
        if np.random.rand() < self.epsilon:
            return random.randint(0, self.action_size - 1)  # Explore
        q_values = self.q_network.predict(state[np.newaxis, :], verbose=0)
        return np.argmax(q_values[0])  # Exploit

    def remember(self, state, action, reward, next_state, done):
        """
        Store an experience in the replay buffer.

        Args:
            state, action, reward, next_state, done: Components of the experience.
        """
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        """
        Train the Q-network using experience replay.

        Args:
            batch_size: Number of samples to use for training in each iteration.
        """
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in batch:
            target = self.q_network.predict(state[np.newaxis, :], verbose=0)[0]
            if done:
                target[action] = reward  # No future rewards if done
            else:
                future_q = np.max(self.target_network.predict(next_state[np.newaxis, :], verbose=0)[0])
                target[action] = reward + self.gamma * future_q

            # Update the Q-network
            self.q_network.fit(state[np.newaxis, :], target[np.newaxis, :], epochs=1, verbose=0)

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

print("done")