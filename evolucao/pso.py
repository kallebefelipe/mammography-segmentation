from __future__ import division
from skimage import io
import scipy.misc
import skimage
import random


def fitnessFunction(individual):
    soma = 0
    for i in range(0, num_dimensions):
        if (i % 2) == 0:
            soma += image[individual[i]][individual[i+1]]
    return soma


class Particle:
    def __init__(self, max_x, max_y):
        self.position_i = []
        self.velocity_i = []
        self.pos_best_i = []
        self.err_best_i = -1
        self.err_i = -1

        for i in range(0, num_dimensions):
            self.velocity_i.append(random.uniform(-1, 1))
            if (i % 2) == 0:
                self.position_i.append(random.randint(0, max_x-1))
            else:
                self.position_i.append(random.randint(0, max_y-1))

    def evaluate(self, costFunc):
        self.err_i = costFunc(self.position_i)
        if self.err_i > self.err_best_i or self.err_best_i == -1:
            self.pos_best_i = self.position_i
            self.err_best_i = self.err_i

    def update_velocity(self, pos_best_g, max_x, max_y):
        w = 0.5       # constant inertia weight (how much to weigh the previous velocity)
        c1 = 1        # cognative constant
        c2 = 2        # social constant

        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = c1*r1*(self.pos_best_i[i]-self.position_i[i])
            vel_social = c2*r2*(pos_best_g[i]-self.position_i[i])
            self.velocity_i[i] = w*self.velocity_i[i]+vel_cognitive+vel_social
            if (i % 2) == 0:
                self.velocity_i[i] = round(abs(self.velocity_i[i]) % max_x)
            else:
                self.velocity_i[i] = round(abs(self.velocity_i[i]) % max_y)

    def update_position(self, max_x, max_y):
        for i in range(0, num_dimensions):
            if (i % 2) == 0:
                self.position_i[i] = \
                    (self.position_i[i]+self.velocity_i[i]) % max_x
            else:
                self.position_i[i] = \
                    (self.position_i[i]+self.velocity_i[i]) % max_y

            if self.position_i[i] < 0:
                self.position_i[i] = 0


class PSO():
    def run(self, costFunc, max_x, max_y, dimensions,
                 num_particles, maxiter, image_atual):
        global num_dimensions
        global image
        num_dimensions = dimensions
        image = image_atual

        err_best_g = -1
        pos_best_g = []

        swarm = []
        for i in range(0, num_particles):
            swarm.append(Particle(max_x, max_y))

        i = 0
        while i < maxiter:
            for j in range(0, num_particles):
                swarm[j].evaluate(costFunc)

                if swarm[j].err_i > err_best_g or err_best_g == -1:
                    pos_best_g = list(swarm[j].position_i)
                    err_best_g = float(swarm[j].err_i)

            for j in range(0, num_particles):
                swarm[j].update_velocity(pos_best_g, max_x, max_y)
                swarm[j].update_position(max_x, max_y)
            i += 1

        return pos_best_g

# image_atual = io.imread('mdb019.bmp')
# max_x = image_atual.shape[0]
# max_y = image_atual.shape[1]
# PSO(fitnessFunction, max_x, max_y, dimensions=10,
#     num_particles=30, maxiter=3000, image_atual=image_atual)
