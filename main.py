from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from random import randint
from kivy.clock import Clock
from kivy.core.window import Window
import numpy as np
import sys


def collision(a, b):
    if a.right < b.x:
        return False
    if a.x > b.right:
        return False
    if a.top < b.gap_top and a.y > b.gap_bottom:
        return False
    return True


class Bird(Widget):
    pass


class Pipe(Widget):
    pass


class Background(Widget):
    def __init__(self, ai_player=None, **kwargs):
        super(Background, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed,
            self
        )
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.ai_player = ai_player
        self.bird_speed = 0
        self.game_speed = 3
        self.num_episodes = 2000
        self.curr_episode = 0
        self.done = 0
        self.prev_state = None
        self.prev_action = 0
        self.elapsed = 0

        self.pipe1.center_y = randint(-600, -100)
        self.pipe2.center_y = randint(-600, -100)

    best_score = NumericProperty(0)
    epsilon = NumericProperty(1)
    score = NumericProperty(0)
    bird = ObjectProperty(None)
    pipe1 = ObjectProperty(None)
    pipe2 = ObjectProperty(None)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar':
            self.jump()

    def update(self, dt):
        self.game_speed = 3 + self.score * .5
        self.pipe1.x -= self.game_speed
        self.pipe2.x -= self.game_speed
        self.bird.y += self.bird_speed
        self.bird_speed -= .5

        # new pipe area
        if self.pipe1.x < -200:
            self.pipe1.x = self.width
            self.pipe1.center_y = randint(-600, -100)
            self.score += 1
        if self.pipe2.x < -200:
            self.pipe2.x = self.width
            self.pipe2.center_y = randint(-600, -100)
            self.score += 1
        if self.score > self.best_score:
            self.best_score = self.score

        if self.bird.y < 0 or self.bird.top > self.height:
            self.done = 1

        # comment this out to remove obstacles
        if collision(self.bird, self.pipe1) \
                or collision(self.bird, self.pipe2):
            self.done = 1

        if self.ai_player:
            self.epsilon = int(self.ai_player.epsilon * 1000) / 1000
            self.elapsed += 1
            if self.curr_episode < self.num_episodes:
                dist1 = self.pipe1.right - self.bird.x
                dist2 = self.pipe2.right - self.bird.x
                if 0 < dist1 < dist2 or dist2 < 0 < dist1:
                    closest_pipe = self.pipe1
                else:
                    closest_pipe = self.pipe2

                state = np.reshape(np.array([
                    # self.bird_speed,
                    self.bird.y,
                    closest_pipe.x,
                    closest_pipe.gap_bottom,
                    closest_pipe.gap_top,
                    # self.game_speed
                ]), [1, 4])
                if self.done:
                    reward = 0
                else:
                    # trying out a higher reward when the bird is
                    # in the pipe gap
                    if closest_pipe.gap_top > self.bird.top\
                            and closest_pipe.gap_bottom < self.bird.y:
                        reward = 20
                    else:
                        reward = 1

                print("reward:", reward)

                if self.prev_state is not None:
                    self.ai_player.remember(
                        self.prev_state,
                        self.prev_action,
                        state,
                        self.done,
                        reward,
                    )

                self.prev_action = action = self.ai_player.act(state)
                self.prev_state = state
                # if self.elapsed > 32:
                #     self.ai_player.replay(32)

                if self.elapsed % 1000 == 0:
                    self.ai_player.model.save("flappy_model.h5")

                if action:
                    self.jump()

            else:
                print("Best Score: ", self.best_score)
                sys.exit()

        if self.done:
            self.game_over()

    def jump(self):
        self.bird_speed = 10

    def game_over(self):
        self.reset_game()
        self.curr_episode += 1
        print("~~~game end")

    def reset_game(self):
        self.score = 0
        self.done = 0
        self.bird_speed = 0
        self.bird.center_y = self.center_y
        self.pipe1.center_x = self.center_x - 100
        self.pipe1.center_y = randint(-600, -100)
        self.pipe2.center_x = self.width
        self.pipe2.center_y = randint(-600, -100)
        self.prev_state = None
        self.prev_action = 0


class Game(App):
    def __init__(self, ai_player=None, **kwargs):
        super().__init__(**kwargs)
        self.ai_player = ai_player

    def build(self):
        display = Background(ai_player=self.ai_player)
        Clock.schedule_interval(display.update, 1/60)
        return display


if __name__ == '__main__':
    Game().run()
