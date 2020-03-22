import math
import graph
import random
import matplotlib.pyplot as plt


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



def shortestArcEuclidianTest(n, size=1000, runs=10, output = True):

    av = 0

    print(f"Running tests using n={n}, size={size} with {runs} graphs\n")

    for i in range(runs):
        generateRandomEuclidianGraph(n, size)
        g = graph.Graph(-1, f"generated-{n}-{size}")
        orig = g.tourValue()
        g.shortestArcs()
        new = g.tourValue()
        reduc = 100* (orig-new) / orig
        av += reduc
        if output:
            print(f"Graph {i} : {reduc}% cost reduction")

    av = av/runs

    if output:
        print(f"\nAverage reduction of {av}%")

    return av

x = [shortestArcEuclidianTest(i, output = False) for i in range(5, 120, 5)]

plt.plot(range(5, 120, 5), x)

plt.xlabel("n")
plt.ylabel("Average Percentage Reduction in Cost")


plt.show()