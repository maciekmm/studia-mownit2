import math
import random
import imageio as imageio
import numpy as np

REPORT_EVERY = 500


def neighborhood(shape, point, range):
    return np.s_[max(0, point[0] - range):min(shape[0], point[0] + range + 1),
           max(0, point[1] - range):min(shape[1], point[1] + range + 1)]


def neighborhood_intersection(shape, p1, p2, range):
    x = np.r_[neighborhood(shape, p1, range)[0]]
    y = np.r_[neighborhood(shape, p1, range)[1]]
    x1 = np.r_[neighborhood(shape, p2, range)[0]]
    y1 = np.r_[neighborhood(shape, p2, range)[1]]
    return [(a, b) for a in x for b in y if a in x1 and b in y1]


def acceptance_probability(cp, cn, temp):
    if cn < cp:
        return 1.0

    return math.exp((cp - cn) / temp)


class Metric():
    def radius(self):
        pass

    def score(self, image, point):
        pass


class CrossMetric():
    def radius(self):
        return 1

    def score(self, image: np.ndarray, point):
        if image[point]:
            return 0
        return np.count_nonzero(image[neighborhood(image.shape, point, 2)])


class steMetric():
    def radius(self):
        return 2

    def score(self, image: np.ndarray, point):
        if image[point]:
            return 0
        return np.count_nonzero(image[neighborhood(image.shape, point, 3)]) - 2 * np.count_nonzero(
            image[neighborhood(image.shape, point, 2)])


class BinaryImage():

    def __init__(self, metric, shape, black_density):
        self.image = np.random.rand(*shape) <= black_density
        self.shape = shape
        self.metric = metric
        self.black_density = black_density
        self._prepare()

    def _prepare(self):
        self.energy = np.array(
            [[self.metric.score(self.image, (row, col)) for col in range(self.shape[1])] for row in
             range(self.shape[0])],
            dtype=int)
        self.total_energy = np.sum(self.energy)

    def _random_position(self):
        return random.randrange(0, self.shape[0]), random.randrange(0, self.shape[1])

    def _swap_points(self, p1, p2, commit=True):
        self.image[p1] = not self.image[p1]
        self.image[p2] = not self.image[p2]
        diff = 0
        for p in [p1, p2]:
            nbhd = self._point_neighborhood(p)
            curr = self.energy[nbhd]
            new = self._energy_around(nbhd)
            diff += np.sum(new - curr)
            if commit:
                self.energy[nbhd] = new
        if commit:
            self.total_energy += diff
        else:
            self.image[p1] = not self.image[p1]
            self.image[p2] = not self.image[p2]
        return diff

    def _point_neighborhood(self, p):
        return neighborhood(self.shape, p, 2 * self.metric.radius())

    def _energy_around(self, nbhd):
        return np.array(
            [[self.metric.score(self.image, (row, col)) for col in np.r_[nbhd[1]]] for row in np.r_[nbhd[0]]])

    def next_state(self):
        p1 = self._random_position()
        p2 = self._random_position()
        while self.image[p1] == self.image[p2]:
            p2 = self._random_position()

        diff = self._swap_points(p1, p2, commit=False)
        return p1, p2, self.total_energy + diff

    def anneal(self, temp, max_it=int(1e8)):
        costs = []
        for i in range(max_it):
            p1, p2, cost = self.next_state()
            ap = acceptance_probability(self.total_energy, cost, temp)

            if temp < 0.01:
                return costs

            if ap > random.random():
                self._swap_points(p1, p2)

            if i % REPORT_EVERY == 0:
                costs.append(self.total_energy)
                print(self.total_energy, ap, temp, i)

            temp = temp * .9999
        return costs

    def save(self, file):
        imageio.imwrite(file, self.image.astype(int))
        pass



if __name__ == "__main__":
    bin = BinaryImage(steMetric(), (50, 50), 0.3)
    costs = bin.anneal(1000)
    with open("./costs", "w+") as f:
        f.write('\n'.join(list(map(lambda x: str(x), costs))))
    bin.save('./output.bmp')
