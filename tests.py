import math
import graph
import random
import matplotlib.pyplot as plt
import time


# Generate n random points in a square of given size and save to a file
def generateRandomEuclideanGraph(n, size):
    with open(f"generated-{n}-{size}", 'w') as f:
        for i in range(n):
            x = random.randrange(size)
            y = random.randrange(size)
            f.write(f"{x} {y}\n")


# Generate a connected graph of n points with random edge costs and save in a file
def generateRandomGraph(n):
    with open(f"generated-{n}", 'w') as f:
        for i in range(n):
            for j in range(n):
                if j>i:
                    f.write(f"{i} {j} {random.randrange(100)}\n")


# Generate a given number of random euclidean graphs with a given number of nodes in a given size
# Calculate either the reduction in cost or runtimes with optional display
# Display and/or return the average of these
def shortestArcEuclideanTest(n, size=1000, runs=10, output = True, mode="reduction"):
    av = 0

    if output:
        print(f"Running tests using n={n}, size={size} with {runs} graphs\n")

    for i in range(runs):
        generateRandomEuclideanGraph(n, size)
        g = graph.Graph(-1, f"generated-{n}-{size}")

        if mode == "reduction":
            orig = g.tourValue()
            g.shortestArcs()
            new = g.tourValue()
            reduc = 100* (orig-new) / orig
            av += reduc
            if output:
                print(f"Graph {i} : {reduc}% cost reduction")

        elif mode == "runtime":
            start = time.time()
            g.shortestArcs()
            t = time.time() - start
            if output:
                print(f"Graph {i} : {t}s runtime")
            av += t


    av = av/runs

    if output:
        if mode == "reduction": 
            print(f"\nAverage reduction of {av}%\n")
        elif mode == "runtime":
            print(f"\nAverage runtime of {av}s\n")

    return av



# Generate a given number of random connected graphs with a given number of nodes in a given size
# Calculate either the reduction in cost or runtimes with optional display
# Display and/or return the average of these
def shortestArcTest(n, runs=10, output = True, mode="reduction"):
    av = 0

    if output:
        print(f"Running tests using n={n}, with {runs} graphs\n")

    for i in range(runs):
        generateRandomGraph(n)
        g = graph.Graph(n, f"generated-{n}")

        if mode == "reduction":
            orig = g.tourValue()
            g.shortestArcs()
            new = g.tourValue()
            reduc = 100* (orig-new) / orig
            av += reduc
            if output:
                print(f"Graph {i} : {reduc}% cost reduction")

        elif mode == "runtime":
            start = time.time()
            g.shortestArcs()
            t = time.time() - start
            if output:
                print(f"Graph {i} : {t}s runtime")
            av += t


    av = av/runs

    if output:
        if mode == "reduction": 
            print(f"\nAverage reduction of {av}%")
        elif mode == "runtime":
            print(f"\nAverage runtime of {av}s")

    return av


# Plot either the cost reduction or runtime for random euclidean graphs of default (1000) size
# with n in a given range and step
def plotEuclideanGraph(start, end, step, mode="reduction"):
    x = [shortestArcEuclideanTest(i, output = False, mode = mode) for i in range(start, end, step)]

    plt.plot(range(start, end, step), x)

    plt.xlabel("n")
    if mode == "reduction":
        plt.ylabel("Average Percentage Reduction in Cost")
    elif mode == "runtime":
        plt.ylabel("Average Runtime")

    plt.show()


# Plot either the cost reduction or runtime for random connected graphs of default (1000) size
# with n in a given range and step
def plotRandomGraph(start, end, step, mode="reduction"):
    x = [shortestArcTest(i, output = False, mode = mode) for i in range(start, end, step)]

    plt.plot(range(start, end, step), x)

    plt.xlabel("n")
    if mode == "reduction":
        plt.ylabel("Average Percentage Reduction in Cost")
    elif mode == "runtime":
        plt.ylabel("Average Runtime")

    plt.show()



# All the tests used in the experiment section of the report

shortestArcTest(100, runs=20)
shortestArcTest(100, runs=20, mode="runtime")


shortestArcEuclideanTest(100, runs=20)
shortestArcEuclideanTest(100, runs=20, mode="runtime")


plotRandomGraph(5, 120, 5)
plotEuclideanGraph(5, 120, 5)


plotRandomGraph(5, 120, 5, mode="runtime")
plotEuclideanGraph(5, 120, 5, mode="runtime")

