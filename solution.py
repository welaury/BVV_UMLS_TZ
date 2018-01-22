#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script uses nqueens.py module for solving 8-queens problem by using 
a genetic algorithm
"""
import sys
print('Python version:', sys.version)

import nqueens as nq

input_pop = nq.Solver_8_queens()

print(input_pop.solve().reshape(10,8,8))
