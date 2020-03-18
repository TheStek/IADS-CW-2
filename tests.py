import math
import graph
import random


def generateRandomEuclidianGraph(n, size):
    with open(f"generated-{n}-{size}", 'w') as f:
        for i in range(n):
            x = random.randrange(size)
            y = random.randrange(size)
            f.write(f"{x} {y}\n")


def generateRandomMetricGraph(n):
    with open(f"generated-{n}", 'w') as f:
        for i in range(n):
            for j in range(n):
                if j>i:
                    f.write(f"{i} {j} {random.randrange(25)}\n")

