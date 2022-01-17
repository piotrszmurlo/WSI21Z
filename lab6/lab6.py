#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from random import randint
from time import sleep as slp
import matplotlib.pyplot as plt 

MAX_GAMES = 100
ALPHA = 0.85
GAMMA = 0.75
MAX_STEPS = 300

def main():
    play(MAX_GAMES, ALPHA, GAMMA, MAX_STEPS)

def create_maze_from_txt(filename='maze.txt') -> np.ndarray:
    with open(filename, 'r') as file:
        input = file.readlines()
        for index, _ in enumerate(input):
            input[index] = _.replace('\n', '')
        size = (len(input), len(input[0]))
        maze = np.zeros(size)
        for i, _ in enumerate(maze):
            for j, _ in enumerate(maze[0]):
                maze[i][j] = input[i][j]
    return (maze, size)

def get_possible_states(maze) -> list:
    possible_states = maze == 0
    possible_states += maze == 3
    possible_states += maze == 9
    indices = np.argwhere(possible_states == True)
    return indices

def get_state_id(possible_states, _state) -> int:
    for id, state in enumerate(possible_states):
        if state[0] == _state[0] and state[1] == _state[1]:
            return id
    return -1

def get_reward(possible_states, state, final_state_id) -> int:
    if get_state_id(possible_states, state) == final_state_id:
        return 100
    else: 
        return -1

def is_action_possible(possible_states, action, state) -> bool:
    temp_state = np.array(state) + np.array(action)
    if get_state_id(possible_states, temp_state) != -1:
        return True
    return False

def play(max_games=100, alpha=0.5, gamma=0.5, max_steps=300):
    maze, maze_size = create_maze_from_txt()
    maze_copy = maze.copy()
    possible_states = get_possible_states(maze)
    final_state_id = np.argwhere(maze == 9)
    final_state_id = get_state_id(possible_states, list(final_state_id[0]))
    states_count = len(possible_states)
    actions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    Q_table = np.zeros((states_count, len(actions)))
    current_state = np.argwhere(maze == 3)
    game_count = 1
    print("\n"*(maze_size[1]))
    UP = f"\x1B[{maze_size[1]+5}A"
    CLR = "\x1B[0K"
    epsilon = 1
    steps_str = ''
    steps_arr = np.zeros(max_games)
    rewards_arr = np.zeros(max_games)
    while game_count <= max_games:
        current_state = list(np.argwhere(maze == 3))[0]
        total_reward = 0
        steps = 0
        for i in range(max_steps):
            current_state_id = get_state_id(possible_states, current_state)
            if np.random.uniform(0, 1) > epsilon:
                # action with max value
                current_action_id = np.argmax(Q_table[current_state_id])
                current_action = actions[current_action_id]
            else:
                #random action
                current_action_id = randint(0, 3)
                current_action = actions[current_action_id]
            if is_action_possible(possible_states, current_action, current_state):
                next_state = np.array(current_state) + np.array(current_action)
                reward = get_reward(possible_states, current_state, final_state_id)
            else:
                next_state = current_state
                reward = -5
            next_state_id = get_state_id(possible_states, next_state)
            Q_table[current_state_id][current_action_id] += alpha * (reward + gamma * max(Q_table[next_state_id]) - Q_table[current_state_id][current_action_id])
            total_reward += reward
            if game_count == max_games:
                steps_str += f"{current_state}->"
                maze_copy[current_state[0]][current_state[1]] = 5
                slp(0.25)
                maze_str = str(maze_copy).replace('5', '\033[0m\033[93m*\033[0m\033[96m').replace('1', 'X').replace('0', ' ').replace('.', '')
                print(f"\033[96m{UP}{maze_str}{CLR}\n\033[0m")
                maze_copy[current_state[0]][current_state[1]] = 0
            current_state = next_state
            epsilon *= 0.95
            if reward > 0:
                steps = i
                break
        if steps == 0:
            steps_arr[game_count - 1] = max_steps
        else:
            steps_arr[game_count - 1] = steps
        rewards_arr[game_count - 1] = total_reward
        game_count += 1

    fig, ax = plt.subplots()
    ax.plot(steps_arr, label='liczba kroków')
    ax.plot(rewards_arr, label='nagroda')
    ax.set(xlabel='epoka', title=f"alpha={alpha}; gamma={gamma}")
    ax.legend()
    plt.show()
    print(steps_str[:-2])


if __name__=='__main__':
    main()