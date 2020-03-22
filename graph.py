import math
import time

def euclid(p,q):
    x = p[0]-q[0]
    y = p[1]-q[1]
    return math.sqrt(x*x+y*y)
                
class Graph:

    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.
    def __init__(self,n,filename):
        with open(filename, 'r') as f:
            lines = f.read().splitlines()

        if n != -1:
            self.n = n
            self.dists = [[10000000 for i in range(self.n)] for i in range(self.n)]
            
            for l in lines:
                data = list(map(int, l.split()))
                self.dists[data[0]][data[1]] = data[2]
                self.dists[data[1]][data[0]] = data[2]



        else:
            self.n = len(lines)
            self.dists = self.dists = [[10000000 for i in range(self.n)] for i in range(self.n)]

            for i in range(self.n):
                for j in range(self.n):
                    n1 = list(map(float, lines[i].split()))
                    
                    n2 = list(map(float, lines[j].split()))
          
                    self.dists[i][j] = euclid(n1, n2)

        self.perm = list(range(self.n))


    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
        val = 0
        for i in range(self.n):
            start = self.perm[i]
            end = self.perm[(i+1) % self.n]
            val += self.dists[start][end]
        return val


    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self,i):
        origPerm = self.perm.copy()
        orig = self.tourValue()
        self.perm[i], self.perm[(i+1) % self.n] = self.perm[(i+1) % self.n], self.perm[i]
        new = self.tourValue()
        
        if orig < new:
            self.perm = origPerm
            return False
        else:
            return True

    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.              
    def tryReverse(self,i,j):
        if ((self.dists[self.perm[i-1]][self.perm[i]] + self.dists[self.perm[j]][self.perm[j+1]]) > 
                (self.dists[self.perm[i-1]][self.perm[j]] + self.dists[self.perm[i]][self.perm[j+1]])):
            self.perm[i:j+1] = reversed(self.perm[i:j+1])
            return True
        return False



    def swapHeuristic(self):
        better = True
        while better:
            better = False
            for i in range(self.n):
                if self.trySwap(i):
                    better = True

    def TwoOptHeuristic(self):
        better = True
        while better:
            better = False
            for j in range(self.n-1):
                for i in range(j):
                    if self.tryReverse(i,j):
                        better = True
                

    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):
        perm = [self.perm[0]]
        unvisited = self.perm[1:]
        
        for i in range(self.n-1):
            costs = list(zip(unvisited, [self.dists[perm[i]][x] for x in unvisited]))
            costs.sort(key = lambda x: x[1])
            perm.append(costs[0][0])
            unvisited.remove(costs[0][0])
        
        self.perm = perm



    def shortestArcs(self):

        visited = []
        unvisited = list(range(self.n))

        arcsToUse = []


        arcs = [(self.dists[i][j], i, j) for i in unvisited for j in unvisited if i != j]

        while len(unvisited) > 1:
            arcs = list(filter(lambda x: (x[1] in unvisited) and (x[2] in unvisited), arcs))

            (d, a, b) = min(arcs, key = lambda x: x[0])

            if a in unvisited and b in unvisited:
                arcsToUse.append((a, b))
                unvisited.remove(a)
                unvisited.remove(b)


        visited.append(arcsToUse[0][0])
        visited.append(arcsToUse[0][1])

        while len(visited) < self.n-len(unvisited):
            last = visited[-1]

            arcsToUse = list(filter(lambda x: not (x[0] in visited or x[1] in visited), arcsToUse))

            arcPosition = [(self.dists[last][a], a, b) for (a, b) in arcsToUse] + [(self.dists[last][b], b, a) for (a, b) in arcsToUse]
            (d, x, y) = min(arcPosition, key = lambda x: x[0])
            visited.append(x)
            visited.append(y)

        if len(unvisited) == 1:
            visited.append(unvisited[-1])
            
        self.perm = visited




g = Graph(-1, "cities75")
print(f"Original tour cost - {g.tourValue()}")


g.shortestArcs()
print(f"Cost after shortestArcs heuristic - {g.tourValue()}")
