# -*- coding: utf-8 -*-
import numpy as np
import random


class Solver_8_queens:

    pop_size = 180
    board_width = 8
    cross_prob = 0.55
    mut_prob = 0.35

    def __init__(self, pop_size=180, cross_prob=0.55, mut_prob=0.35):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

    def solve(self, min_fitness = 72, max_epochs = 300):
        population = self.generate_population()

        fit_func_in = self.fit_func(population)

        epoch = 0

        while (np.max(fit_func_in) < min_fitness):
            if np.max(fit_func_in) >= min_fitness: break

            parent_pull = self.reproduction(fit_func_in, population)
            parent_pull = np.random.permutation(parent_pull)
            parent_fit_func = self.fit_func(parent_pull)

            crossingover_out = self.crossingover(parent_pull)
            crossingover_out = self.mutation(crossingover_out)
            fit_func_cross = self.fit_func(crossingover_out)

            population = self.reduction(parent_pull, crossingover_out, parent_fit_func, fit_func_cross)
            fit_func_in = self.fit_func(population)

            epoch+=1
            if epoch == max_epochs: break

        visualization = self.visual(population[self.pop_size-1])

        return max(fit_func_in), epoch, visualization

    def generate_population(self):
        population = np.zeros((self.pop_size, self.board_width), dtype=np.uint8)

        for hromosom in population:
            for position in range(len(hromosom)):
                hromosom[position] = random.randrange(0, self.board_width, 1)

        return population

    def fit_func(self, population):
        fit_func_result = np.zeros(len(population), dtype = np.uint64)

        for index, hromosom in enumerate(population):
            #Вертикаль
            unique, counts = np.unique(hromosom, return_counts=True)
            unique_match, counts_match = np.unique(counts, return_counts=True)
            fit_func_result[index] += counts_match[0]*2

            # Диагонали
            for x in range(0,len(hromosom)):
                for y in range(0, len(hromosom)):
                    if int(abs(x - y)) != int(abs(hromosom[x] - hromosom[y])):
                        fit_func_result[index] += 1

        return fit_func_result

    def reproduction(self, fit_func, population):
        func_p = np.zeros(len(population), dtype = np.uint8)
        parent_pull = np.zeros((len(population), self.board_width), dtype=np.uint8)

        for index, hromosom in enumerate(fit_func):
            func_p[index] = round(fit_func[index] / np.sum(fit_func) * 100)

        wheel = []

        for x in range(0, len(population)):
            for _ in range(0, func_p[x]):
                wheel.append(x)

        for x in range(0, len(population)):
            parent_pull[x] = population[wheel[random.randrange(0, len(wheel), 1)]]

        return parent_pull

    def crossingover(self, parent_pull):
        crossingover_out = np.zeros((len(parent_pull), self.board_width), dtype=np.uint8)

        for x in range(0, int(len(parent_pull)/ 2)):
            if random.randrange(0, 100, 1) < self.cross_prob * 100:
                first_parent = parent_pull[x]
                second_parent = parent_pull[int(len(parent_pull)/ 2 - 1 - x)]

                k_point = random.randrange(1, self.board_width - 1, 1)

                crossingover_out[x] = np.concatenate((first_parent[:k_point], second_parent[k_point:]))
                crossingover_out[int(len(parent_pull)/ 2 - 1 - x)] = np.concatenate((second_parent[:k_point], first_parent[k_point:]))

        return crossingover_out

    def mutation(self, crossingover_out):
        for hromosom in crossingover_out:
            if random.randrange(0, 100, 1) < self.mut_prob * 100:
                hromosom[random.randrange(0, self.board_width, 1)] = random.randrange(0, self.board_width, 1)

        return crossingover_out

    def reduction(self, population, crossingover_out, fit_func_in, fit_func_cross):
        full_hromosoms = np.vstack((population,crossingover_out))
        full_func_val = np.concatenate((fit_func_in, fit_func_cross))
        full_hromosoms = full_hromosoms[full_func_val.argsort()]

        return full_hromosoms[len(population):]

    def visual(self, hromosom):
        visual_string = ''
        for x in range(0,len(hromosom)):
            visual_string += '+'*len(hromosom)

        visual_array = list(visual_string)
        for x in range(0,len(hromosom)):
            visual_array[len(hromosom)*x + hromosom[x]] = 'Q'

        bias = 0
        for x in range(1,len(hromosom)):
            visual_array.insert(len(hromosom)*x+bias,'\n')
            bias+=1

        visual_string = ''.join(visual_array)

        return visual_string
