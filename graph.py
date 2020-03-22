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

        # Open the file and save the lines in a list

        with open(filename, 'r') as f:
            lines = f.read().splitlines()


        # If the graph is metric initialise the dists matrix and loop through data adding the costs into the 
        # correct element
        if n != -1:
            self.n = n
            self.dists = [[10000000 for i in range(self.n)] for i in range(self.n)]
            
            for l in lines:
                data = list(map(int, l.split()))
                self.dists[data[0]][data[1]] = data[2]
                self.dists[data[1]][data[0]] = data[2]




        # If the graph is euclidian find n as the number of coordinate pairs in the file and initialise the dists matrix

        else:
            self.n = len(lines)
            self.dists = self.dists = [[10000000 for i in range(self.n)] for i in range(self.n)]


            # Loop through each pair of locations and add the corresponding distances to the correct element of dists

            for i in range(self.n):
                for j in range(self.n):
                    n1 = list(map(float, lines[i].split()))
                    
                    n2 = list(map(float, lines[j].split()))
          
                    self.dists[i][j] = euclid(n1, n2)



        # Set the intial permutation to the nodes in order
        self.perm = list(range(self.n))


    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):

        # Loop through each of the nodes in self.perm and add the cost from this to the next value to val

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

        # Save the original perm and the tour value of this
        origPerm = self.perm.copy()
        orig = self.tourValue()

        # Swap the two specified elements and get the new tour value
        self.perm[i], self.perm[(i+1) % self.n] = self.perm[(i+1) % self.n], self.perm[i]
        new = self.tourValue()
        

        # If there is no improvement revert to the original
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
        # The only change in the tour value will be at the edges of the portion to reverse
        # This if statement checks if a reverse would be beneficial

        if ((self.dists[self.perm[i-1]][self.perm[i]] + self.dists[self.perm[j]][self.perm[j+1]]) > 
                (self.dists[self.perm[i-1]][self.perm[j]] + self.dists[self.perm[i]][self.perm[j+1]])):
            
            # If the reverse would be beneficial, reverse the specified section
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
        # Add the first element of the initial perm to the new perm list
        # Add all other nodes to the unvisited list

        perm = [self.perm[0]]
        unvisited = self.perm[1:]
        
        # Loop through the perm and add the closest node to the last node in perm
        for i in range(self.n-1):

            # Generate a list of unvisited nodes paired with the distance from the last node in perm
            costs = [(x, self.dists[perm[i]][x]) for x in unvisited]

            # Find the node with the smallest distance
            (minNode, d) = min(costs, key=lambda x: x[1])

            # Add the node to the perm and remove it from the unvisited list
            perm.append(minNode)
            unvisited.remove(minNode)
        
        # Set the perm attribute to the perm we built
        self.perm = perm



    def shortestArcs(self):
        # Initalise the empty visited list, the empty list of arcs to use and the unvisited list to all nodes
        visited = []
        unvisited = list(range(self.n))
        arcsToUse = []

        # Generate the list of all arcs in the graph, storing cost and both nodes
        arcs = [(self.dists[i][j], i, j) for i in unvisited for j in unvisited if i != j]

        # Loop while there are arcs to add
        while len(unvisited) > 1:

            # Remove all arcs that aren't for nodes in the unvisited list
            arcs = list(filter(lambda x: (x[1] in unvisited) and (x[2] in unvisited), arcs))

            # Find the shortest arc in the arcs list, add to arcs to use and remove nodes from unvisited
            (d, a, b) = min(arcs, key = lambda x: x[0])

            arcsToUse.append((a, b))
            unvisited.remove(a)
            unvisited.remove(b)



        # Add the first arc to the visited list
        visited.append(arcsToUse[0][0])
        visited.append(arcsToUse[0][1])

        # Loop to build up the visited list
        while len(visited) < self.n-len(unvisited):

            # Store the last node in the tour
            last = visited[-1]

            # Filter out arcs we have used already
            arcsToUse = list(filter(lambda x: not (x[0] in visited or x[1] in visited), arcsToUse))

            # Generate a list storing the distances from each arc to the last node and the nodes in each arc
            # This is done for the reverse of each arc as well
            arcPosition = [(self.dists[last][a], a, b) for (a, b) in arcsToUse] + [(self.dists[last][b], b, a) for (a, b) in arcsToUse]
            
            # Find the closest of these arcs and add it to the visited list
            (d, x, y) = min(arcPosition, key = lambda x: x[0])
            visited.append(x)
            visited.append(y)

        # Add any leftover to the end of the visited list
        if len(unvisited) == 1:
            visited.append(unvisited[-1])

        # Set the perm to the visited list
        self.perm = visited
