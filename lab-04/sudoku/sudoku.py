import math
import os
import random
from copy import deepcopy

import numpy as np


def populate(sudoku):
    segments = reshape_to_segments(sudoku)
    empty = []
    for i, segment in enumerate(segments):
        flat_segment = segment.reshape(9)
        empty.append([i for i in range(9) if flat_segment[i] == 0])
        to_fill = [i for i in range(1, 10) if i not in set(flat_segment)]
        random.shuffle(to_fill)
        segments[i] = np.array([i if i != 0 else to_fill.pop() for i in flat_segment]).reshape(3, 3)
    return segments, empty


def score(sudoku: np.ndarray):
    """
    Score is calculated as the number of unique entries in each row/column;
    """
    reshaped = flatten(sudoku).reshape(9, 9)
    score = sum([len(set(row)) for row in reshaped])
    score += sum([len(set(row)) for row in reshaped.T])
    return score


def reshape_to_segments(sudoku):
    sud = sudoku.reshape(9, 9)
    return np.array([sud[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3] for i in range(3) for j in range(3)])


def flatten(sudoku: np.ndarray):
    segs = sudoku.reshape(3, 3, 3, 3)
    indexes = []
    for seg_y in range(3):
        for y in range(3):
            for seg_x in range(3):
                for x in range(3):
                    indexes.append(segs[seg_y][seg_x][y][x])
    return np.array(indexes)


def generate_state(sudoku: np.ndarray, empty):
    """
    Swap two values in random square
    """
    new_state = deepcopy(sudoku)
    square_i = random.randrange(0, 9)
    square = new_state[square_i].reshape(9)
    empty_values = empty[square_i]
    swap_from = empty_values[random.randrange(0, len(empty_values))]
    swap_to = empty_values[random.randrange(0, len(empty_values))]
    square[swap_from], square[swap_to] = square[swap_to], square[swap_from]
    new_state[square_i] = square.reshape(3, 3)
    return new_state


def acceptance_probability(score, new_score, temperature):
    if new_score > score:
        return 1.0

    return math.exp((new_score - score) / temperature)


def solve(sudoku):
    initial_temperature = 1 / 2
    temperature = initial_temperature
    # temperature = 1 \
    current_state, empty = populate(sudoku)
    scores = []

    i = 0
    same = 0
    restarts = 0
    while True:
        old_score = score(current_state)
        if i % 10 == 0:
            scores.append(old_score)
        if i % 5000 == 0:
            print(i, old_score)
        new_state = generate_state(current_state, empty)
        new_score = score(new_state)

        same = same + 1 if abs(new_score - old_score) <= 4 and new_score > 150 else 0;
        if same > 50000:
            temperature = initial_temperature
            current_state, empty = populate(sudoku)
            i = 0
            scores = []
            same = 0
            restarts += 1
            continue

        if acceptance_probability(old_score, new_score, temperature) >= random.random():
            current_state = new_state

        if new_score == 162:
            return flatten(current_state), scores, restarts

        temperature /= 1.00002
        i += 1


# with open('./sudokus/sudokus.txt') as file:
#     while True:
#         title = file.readline()
#         if title is None or title == "":
#             break
#         sud = [[int(digit) for digit in file.readline().replace('\n', '').replace(' ', '')] for _ in range(9)]
#         sudoku = [y for x in sud for y in x]
#         file_name = './solutions/{}'.format(title.replace('\n', ''))
#         if os.path.isfile(file_name):
#             print("Skipping {}".format(file_name))
#             continue
#         flattened, scores, restarts = solve(np.array(sudoku))
#         with open(file_name, 'w+') as solution:
#             solution.write(' '.join([str(t) for t in sudoku]))
#             solution.write('\n')
#             solution.write(' '.join([str(t) for t in flattened]))
#             solution.write('\n')
#             solution.writelines(['{}\n'.format(t) for t in scores])
#             solution.write('{}'.format(restarts))
#         print(title)

with open('./sudokus/hardest_2.txt') as file:
    for i in range(11):
        sud = [int(digit) for digit in file.readline().replace('\n', '').replace('x', '0').replace(' ', '')]
        file_name = './solutions/hardest-{}'.format(i)
        if os.path.isfile(file_name):
            print("Skipping {}".format(file_name))
            continue
        flattened, scores, restarts = solve(np.array(sud))
        with open(file_name, 'w+') as solution:
            solution.write(' '.join([str(t) for t in sud]))
            solution.write('\n')
            solution.write(' '.join([str(t) for t in flattened]))
            solution.write('\n')
            solution.writelines(['{}\n'.format(t) for t in scores])
            solution.write('{}'.format(restarts))
        print(i)
