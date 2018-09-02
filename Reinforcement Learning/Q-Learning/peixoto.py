# Author: Kyle Kastner
# License: BSD 3-Clause
# Implementing http://mnemstudio.org/path-finding-q-learning-tutorial.htm
# Q-learning formula from http://sarvagyavaish.github.io/FlappyBirdRL/
# Visualization based on code from Gael Varoquaux gael.varoquaux@normalesup.org
# http://scikit-learn.org/stable/auto_examples/applications/plot_stock_market.html

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


# defines the reward/connection graph
r = np.array([[100, -1, -1, -1, -1, -1, -1],
              [-1, -1, -1, -1, 0, -1, 0],
              [-1, -1, -1, -1, 0, -1, 0],
              [100, -1, -1, -1, -1, -1, -1],
              [-1, 0, 0, -1, -1, 0, 0],
              [100, -1, -1, -1, -1, -1, -1],
              [-1, -1, -1, 0, -1, -1, -1]]).astype("float32")
q = np.zeros_like(r)
print(q)


def update_q(state, next_state, action, alpha, gamma):
    rsa = r[state, action]
    qsa = q[state, action]
    new_q = qsa + alpha * (rsa + gamma * max(q[next_state, :]) - qsa)
    q[state, action] = new_q
    # renormalize row to be between 0 and 1
    rn = q[state][q[state] > 0] / np.sum(q[state][q[state] > 0])
    q[state][q[state] > 0] = rn
    return r[state, action]


def show_traverse():
    # show all the greedy traversals
    for i in range(len(q)):
        current_state = i
        traverse = "%i -> " % current_state
        n_steps = 0
        while current_state != 0 and n_steps < 20:
            next_state = np.argmax(q[current_state])
            current_state = next_state
            traverse += "%i -> " % current_state
            n_steps = n_steps + 1
        # cut off final arrow
        traverse = traverse[:-4]
        print("Greedy traversal for starting state %i" % i)
        print(traverse)
        print("")


# Core algorithm
gamma = 0.8
alpha = 1.
n_episodes = 1E4
n_states = 7
n_actions = 7
epsilon = 0.05
random_state = np.random.RandomState(1999)
for e in range(int(n_episodes)):
    states = list(range(n_states))
    print("New episode")
    print(states)
    random_state.shuffle(states)
    print(states)
    current_state = states[0]
    goal = False
    print(q)
    while not goal:
        # epsilon greedy
        valid_moves = r[current_state] >= 0
        if random_state.rand() < epsilon:
            print("B")
            actions = np.array(list(range(n_actions)))
            print(actions)
            actions = actions[valid_moves == True]
            print(actions)
            if type(actions) is int:
                actions = [actions]
            random_state.shuffle(actions)
            print(actions)
            action = actions[0]
            print("action chosed", action)
            input("Press to continue...")
            next_state = action
        else:
            if np.sum(q[current_state]) > 0:
                action = np.argmax(q[current_state])
                print("My action", action)
            else:
                # Don't allow invalid moves at the start
                # Just take a random move
                actions = np.array(list(range(n_actions)))
                print("A")
                print(current_state)
                print(actions)
                print(valid_moves)
                actions = actions[valid_moves == True]
                print("Pre shuffle")
                print(actions)
                random_state.shuffle(actions)
                print("Pos shuffle")
                print(actions)
                action = actions[0]
                print("action chosed", action)
                input("Press to continue...")
            next_state = action
        reward = update_q(current_state, next_state, action,
                          alpha=alpha, gamma=gamma)
        # Goal state has reward 100
        if reward > 1:
            goal = True
        current_state = next_state

print(q)
show_traverse()
for i in range(7) :
    print(r[i])