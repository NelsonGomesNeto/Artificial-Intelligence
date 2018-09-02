import numpy as np
from random import randint, random

def printMatrix(m):
    for i in range(len(m)):
        print(m[i])

def printPath(path):
    for i in range(len(path)):
        print(path[i], end='')
        if (i != len(path) - 1):
            print(" -> ", end='')
        else:
            print(" (size: %d)" % len(path))

def printOptimalPaths():
    for i in range(1, len(q)):
        at = i
        path = [at]
        while (at != 0):
            action = getActions(at)
            at = getBestAction(at, action)
            path += [at]
        print("Optimal path: ", end='')
        printPath(path)

def getBestAction(state, action):
    best, to = -1, -1
    for i in action:
        if (q[state][i] > best):
            best, to = q[state][i], i
    return(to)

def getActions(state):
    action = []
    for i in range(len(r)):
        if (r[state][i] != -1):
            action += [i]
    return(action)

def prepare():
    vertices, edges = map(int, input().split())
    r = [[-1] * vertices for i in range(vertices)]
    q = [[0] * vertices for i in range(vertices)]
    for i in range(edges):
        u, v, c = map(int, input().split())
        r[u][v] = c
    return(r, q)

r, q = prepare()
print("R:")
printMatrix(r)
print("Q:")
printMatrix(q)
print("-----------")

episodes = 200
gamma = 0.8
epsilon = 0.5
for i in range(episodes):
    print("\nEpisode", i)
    state = randint(0, 6)
    path, initialState = [state], state
    goal = state == 0
    print("Initial state:", state)
    while (not goal):
        action = getActions(state)
        print("State: ", state, ", Possible actions: ", action, sep='', end='')
        if (len(action) == 0):
            print("\nNo action can be made")
            break

        if (random() > epsilon): # e-greedy
            chosen = getBestAction(state, action)
            print(", best:", chosen)
        else:
            chosen = action[randint(0, len(action) - 1)]
            print(", explore:", chosen)

        maxQ = 0
        nextAction = getActions(chosen)
        for i in nextAction:
            maxQ = max(maxQ, q[chosen][i])

        q[state][chosen] = r[state][chosen] + gamma * maxQ

        state = chosen
        path += [state]
        goal = state == 0
    print("Path done: ", end='')
    printPath(path)
    printMatrix(q)

print("\nQ:")
printMatrix(q)
printOptimalPaths()