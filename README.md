# FlappyBird

My process so far looks like this:

I built the Flappy Bird game using the Kivy Python library. I made sure to make it modular enough to be easily changed later, since I didn't know how the agent was going to work just yet.

Once I finished the game, I did some research on different deep learning libraries and found Keras to be the easiest to learn and the highest probablility that I'd use it in my career.

I then read this extremely well-written article (https://keon.io/deep-q-learning/) about 30 times over. I wanted to enderstand every line of code he had written. This helped me join the understanding I gained from my Neural Network Project (https://github.com/blake27182/NeuralNetworkPrototype) to the "how to use it" knowledge.

If you look closely, you may see I adapted much of his code to my program because it was so general purpose, and concise, I didn't see why I should change it. I ended up changing much of it later on though as I figured out what would make my agent work better for my purposes.

I kept having an issue of the agent not being able to differentiate the predicted reward enough though. If it was not near any obstacles, it was too apethetic wether it should jump or not jump. This led to long bouts of repetition while training where it would choose jump over and over or choose fall over and over until it died.

The solution was found in this article (https://yanpanlau.github.io/2016/07/10/FlappyBird-Keras.html) which talked about exactly how a Q-function works and why it is able to predict future reward. It was clear to me that my agent needed to either look farther ahead or have more different rewards in its environment.

As of now, the agent receives 20 reward points for being in the pipe-gap, 1 reward point for being alive and outside of the gap, and 0 for dying. After training on this for about 30 minutes, the agent stays in the gap, but jumps as soon as it reaches the middle, resulting in occasionally hitting the pipe above.

My next steps are to try different rewards schemes and possibly changing the Q-function to get it to understand exactly what the goal of the game is and how to plan a little more ahead.
