import numpy as np
import matplotlib.pyplot as plt


def draw_table(sudoku):
    result = ''.join(["|" for _ in range(10)])
    result += '\n|'
    result += '|'.join([":---:" for _ in range(9)])
    result += '|\n'
    reshaped = np.array(sudoku).reshape(9, 9)
    for row in reshaped:
        result += '|'
        for d in row:
            result += ' {} |'.format(d if d != 0 else '.')
        result += '\n'

    return result


STEP = 5000

its = []
rests = []

for i in range(11):
    with open('./solutions/hardest-{}'.format(i)) as solution:
        print("# Hardest #{}\n\n## Puzzle \n".format(i + 1))
        print(draw_table([int(d) for d in solution.readline().split(' ')]))
        print('\n ## Solution \n')
        print(draw_table([int(d) for d in solution.readline().split(' ')]))
        score = [int(d) for d in solution.read().split('\n')]
        restarts = score[-1]
        rests.append(restarts)
        its.append(len(score) * 5000)
        file_name = './assets/hardest-{}.png'.format(i)
        print('\n\n## Annealing schema: ![]({})'.format(file_name))
        print('\n\nRestarts: {}\n'.format(restarts))
        print('\n\nIterations: {}\n'.format(len(score) * 5000))
        print("------\n")
        score[-1] = 162
        x = [i * 5000 for i in range(len(score))]
        plt.ylim([140, 162])
        plt.xlabel('Iterations')
        plt.ylabel('Score')
        plt.plot(x, score)
        plt.savefig(file_name)
        plt.clf()

print(np.mean(np.array(its)))
print(np.mean(np.array(rests)))
