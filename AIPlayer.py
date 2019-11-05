from main import Game
import numpy as np
from collections import deque
import random
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam
import os


class AIPlayer:
    def __init__(self, state_size, action_size, load=False):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = .95
        self.epsilon = 1
        self.action_bias = 60
        self.epsilon_min = .01
        self.epsilon_decay = .99995
        self.learning_rate = .001
        self.model = self._build_model(load)

    def _build_model(self, load):
        if load and os.path.exists("flappy_model.h5"):
            return load_model("flappy_model.h5")
        model = Sequential()
        model.add(Dense(100, input_dim=self.state_size,
                        activation='relu'))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(75, activation='relu'))
        model.add(Dense(20, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, next_state, done, reward):
        self.memory.append((state, action, next_state, done, reward))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            x = np.random.rand() * self.action_bias
            return 1 if x < 1 else 0
        else:
            act_values = self.model.predict(state)
            # maybe take a look at what act_values looks like
            print(act_values[0], np.argmax(act_values[0]))
            return np.argmax(act_values[0])

    def replay(self, batch_size):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        mini_batch = random.sample(self.memory, batch_size)

        for state, action, next_state, done, reward in mini_batch:
            target = reward
            if not done:
                # look into adding more depth to this function
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))

            target_f = self.model.predict(state)
            target_f[0][action] = target
            # try verbose to see some good shit
            self.model.fit(state, target_f, epochs=1, verbose=0)

    @staticmethod
    def action_choice(bird, pipe1, pipe2):
        dist1 = pipe1.right - bird.x
        dist2 = pipe2.right - bird.x

        if 0 < dist1 < dist2 or dist2 < 0 < dist1:
            if bird.y < pipe1.gap_bottom + 30:
                return 1

        if 0 < dist2 < dist1 or dist1 < 0 < dist2:
            if bird.y < pipe2.gap_bottom + 30:
                return 1

        return 0


if __name__ == '__main__':
    Game(ai_player=AIPlayer(6, 2, load=False)).run()
