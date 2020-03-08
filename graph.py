import math

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

        if n!= -1:
            c1 = []
            c2 = []
            c3 = []
            for l in lines:
                data = self.stripVals(l)
                c1.append(data[0])
                c2.append(data[1])
                c3.append(data[2])

            nodes = set(c1).union(set(c2))
            self.n = n

            nodeReference = {node : i for (node, i) in zip(nodes, range(self.n))}

            self.dists = [[10000000 for i in range(self.n)] for i in range(self.n)]

            for i in range(len(c1)):
                n1 = c1[i]
                n2 = c2[i]
                d = c3[i]
                self.dists[nodeReference[n1]][nodeReference[n2]] = int(d)


        else:
            self.n = len(lines)
            self.dists = self.dists = [[10000000 for i in range(self.n)] for i in range(self.n)]

            for i in range(self.n):
                for j in range(self.n):
                    n1 = self.stripVals(lines[i])
                    n2 = self.stripVals(lines[j])
                    self.dists[i][j] = euclid(n1, n2)

        self.perm = list(range(self.n))

    def stripVals(self, line):
        l = line.split(' ')
        return list(map(float, filter(lambda x: x != '', l)))

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

        origPerm = self.perm.copy()

        orig = self.tourValue()

        s1 = i
        s2 = j

        while s1<s2:
            self.perm[s1], self.perm[s2] = self.perm[s2], self.perm[s1]
            s1 += 1
            s2 -= 1

        new = self.tourValue()

        if orig < new:
            self.perm = origPerm
            return False
        else:
            return True


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
        pass


g = Graph(-1, "cities50")
print(g.tourValue())
g.swapHeuristic()
g.TwoOptHeuristic()
print(g.tourValue())