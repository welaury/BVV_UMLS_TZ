# -*- coding: utf-8 -*-
import numpy as np
import random
import math

'''
Данное решение должно расставлять ферзей без пересечений по вертикали и горизонтали.
Однако до конца программа этот процесс не доводит (расставляет 5 ферзей, на большем кол-ве улетает в бесконечный цикл).
Я отправил это решение, т.к. возможно вы укажете на проблему и прочие недочеты, для этого, я так понял, и установлен мягкий дедлайн.
'''

class Solver_8_queens:
    pop_size = 10
    board_size = 64
    cross_prob = 0.5
    mut_prob = 0.2
    func_val = np.zeros(pop_size, dtype = np.uint8)
    func_val_next = np.zeros(pop_size, dtype=np.uint8)
    population = np.zeros((pop_size, board_size), dtype = np.uint8)
    elite_hromosom = np.zeros((pop_size, board_size), dtype = np.uint8)
    func_p = np.zeros(pop_size, dtype=np.uint8)
    next_generations = np.zeros((pop_size, board_size),dtype=np.uint8)

    def __init__(self, pop_size=10,cross_prob = 0.5, mut_prob=0.2):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
    def solve(self):
        self.gen_pop()
        self.fit_func_pop()
        while np.max(self.get_func_val()) < 16:
            self.wheel()
            self.gen_next_gen()
            self.do_mut()
            self.fit_func_next()
            self.gen_best()
        return self.get_in()


    def gen_pop(self):
        for hromosom in self.population:
            sum_array_element = 0
            while sum_array_element < int(math.sqrt(self.board_size)):
                hromosom[random.randrange(0, self.board_size - 1, 1)] = 1
                sum_array_element = np.sum(hromosom)

    def get_in(self):
        return self.population

    def fit_func_pop(self):
        for index, hromosom in enumerate(self.population):
            value = 0
            board = hromosom.reshape(int(math.sqrt(self.board_size)), int(math.sqrt(self.board_size)))
            for x in range(0, int(math.sqrt(self.board_size))):
                if (np.sum(board[:, x]) == 1): value += 1
                if (np.sum(board[x, :]) == 1): value += 1
            self.func_val[index] = value

    def fit_func_next(self):
        for index, hromosom in enumerate(self.next_generations):
            value = 0
            board = hromosom.reshape(int(math.sqrt(self.board_size)), int(math.sqrt(self.board_size)))
            for x in range(0, int(math.sqrt(self.board_size))):
                if (np.sum(board[:, x]) == 1) and (np.sum(board[x, :]) == 1): value += 1
            self.func_val_next[index] = value

    def wheel(self):
        for index, hromosom in enumerate(self.func_val):
            self.func_p[index] = round(self.func_val[index] / np.sum(self.func_val) * 100)
        wheel = []
        for x in range(0, self.pop_size):
            for _ in range(0, self.func_p[x]):
                wheel.append(x)

        for x in range(0, self.pop_size):
            self.elite_hromosom[x] = self.population[wheel[random.randrange(0, len(wheel), 1)]]

    def gen_next_gen(self):
        self.next_generations = self.population
        for x in range(0, int(self.pop_size / 2)):
            if random.randrange(0, 100, 1) < self.cross_prob * 100:
                id_first = random.randrange(0, len(self.elite_hromosom), 1)
                id_second = random.randrange(0, len(self.elite_hromosom), 1)
                first_parent = self.elite_hromosom[id_first]
                second_parent = self.elite_hromosom[id_second]

                while id_first == id_second:
                    id_second = random.randrange(0, len(self.elite_hromosom), 1)
                    second_parent = self.elite_hromosom[id_second]

                k_point = random.randrange(1, self.board_size - 1, 1)

                self.next_generations[x] = np.concatenate((first_parent[:k_point], second_parent[k_point:]))
                self.next_generations[int(self.pop_size - 1 - x)] = np.concatenate((second_parent[:k_point], first_parent[k_point:]))

    def do_mut(self):
        for hromosom in self.next_generations:
            if random.randrange(0, 100, 1) < self.mut_prob*100:
                k_point = random.randrange(0, self.board_size, 1)
                if hromosom[k_point] == 1:
                    hromosom[k_point] = 0
                    other = random.randrange(0, self.board_size, 1)
                    while hromosom[other] == 1:
                        if hromosom[other] == 1: other = random.randrange(0, self.board_size, 1)
                        else: hromosom[other] = 1
                else:
                    hromosom[k_point] = 1
                    other = random.randrange(0, self.board_size, 1)
                    while hromosom[other] == 0:
                        if hromosom[other] == 0: other = random.randrange(0, self.board_size, 1)
                        else:hromosom[other] = 0
                        
    def gen_best(self):
        full_pop = np.vstack((self.population,self.next_generations))
        full_func_val = np.concatenate((self.func_val,self.func_val_next))
        full_pop = full_pop[full_func_val.argsort()]
        self.population = full_pop[:10]

