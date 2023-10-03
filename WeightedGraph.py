import random
import copy

class WeightedGraph(object):
    """
    COPYRIGHT SOPHIE QUIGLEY 2023
    THIS FILE IS NOT TO BE MODIFIED, CIRCULATED, OR POSTED WITHOUT THE PERMISSION OF SOPHIE QUIGLEY
    WeightedGraph objects can be used to work with weighted graphs.
    They are internally represented using modified adjacency matrices where each entry a(i,j) is either
    - 0 if there is no edge between vertices i and j
    - a positive integer representing the weight of the edge between i and j if there is such an edge
    Note that the graph is simple and therefore the adjacency matrix representation is symmetric
    
    DO NOT MODIFY THIS CLASS EXCEPT FOR THE ISSUBGRAPH METHOD AT THE END
    """
    seeded = False
	  

    @classmethod
    def fromFile(cls, filename):
        """
        Instantiates a WeightedGraph read from a file.  
        See the description of WeightedGraph.readGraph for the file format.
	
        Parameters:
        str filename: name of file containing the graph
	
        Returns a WeightedGraph described by the file. 
        """
        vertices, edges = WeightedGraph.readGraph(filename)
        return WeightedGraph(vertices, edges)


    @classmethod
    def readGraph(cls, filename):
        """
        Read a graph from a file and return the number of vertices and its edges.  
        The file has the following format:
        The first line contains the number of vertices in that graph
        Followed by one line for each row of the adjacency matrix of the graph: 
        in each row the elements are separated by blanks.
	
        Note: This method assumes that the file is error-free.  It will not handle mistakes.
	 
        Parameters:
          str filename: name of file containing the graph
	
        Returns a tuple with the number of vertices and the edges that are described in the file. 
        """
        f = open(filename, "r")
        with f as lines:
            row = 0
            for line in lines:
                if row == 0:
                    vertices = int(line)
                    edges = []
                    row += 1
                elif row <= vertices:
                    newrow = [int(i) for i in line.split()]
                    edges.append(newrow)
                    row += 1
                elif row > vertices:
                    break
        f.close()
        return vertices, edges;

    
    @classmethod
    def newRandom(cls, seed, vertices, density, maxweight):
        """
        Instantiates new WeightedGraph randomly as specified by parameters.
	 
        Parameters:
            int seed: seed for random number generator
            int vertices: number of vertices in the Graph
            int density: percentage from 1 to 100 of potential edge which are present
            int maxweight: maximum weight for an edge (minimum is 1)

        Returns a new graph to specifications or None if they can't be met.
        """
        if vertices <= 0:
            print("Error: Number of vertices must be positive")
            return None
        if density <= 0 or density >100:
            print("Error: density must between 1 and 100")
            return None
        if maxweight <= 0:
            print("Error: maxweight must be positive")
            return None
        # Seed the random number generator once
        if not WeightedGraph.seeded:
            random.seed(a=seed)
            WeightedGraph.seeded = True

        # Create array of 0 edges
        edges = []
        for i in range(vertices):
            edges.append(list([0]*vertices))

        # Populate non-diagonal cells of matrix
        for i in range(vertices):
            for j in range(i+1,vertices):
                if random.randint(1, 100) <= density-1:                
                    edges[i][j] = random.randint(1,maxweight)
                    edges[j][i] = edges[i][j]
        return WeightedGraph(vertices, edges)


    def __init__(self, vertices, edges):
        """Creates a new Graph from an adjacency matrix
	
        Parameters:
            int vertices: number of vertices in the Graph
            List edges: adjacency matrix of the edges
	
        Notes:
        - This constructor is not intended to be used directly.
          The two class methods fromFile and newRandomSimple should be used instead.
        - Nevertheless, if incorrect data is received, the graph information will be corrected
        """
        if vertices <= 0:
            print("Error: Number of vertices must be positive")
            return None
        
        # Total number of vertices and edges and total weight of graph
        self.totalV = vertices
        self.totalE = 0
        self.totalW = 0
        
        # Adjacency matrix of graph.
        # edges[x][y] is the weight of the edge from vertex x to vertex y or 0 if there is no edge
        self.edges = edges
        
        # Used by graph visitors to keep track of visited vertices.
        self.visitedV = [None]*vertices
        
        # Used by graph visitors to keep track of visited edge.
        self.visitedE = []
        
        # Used by graph visitors to keep track of unvisited edge
        # as an alternative to using visitedE.
        self.unvisitedE = []
        
        for i in range(vertices):
            self.visitedE.append(list([None]*vertices))
            self.unvisitedE.append(list([None]*vertices))
        self.clearVisited()
        
        # Read adjacency matrix and correct any mistakes
        for i in range(vertices):
            if edges[i][i] != 0:
                    print("Error: Weighted graph does not have loops - loop was removed.")
                    edges[i][i] = 0               
            for j in range(i+1,vertices):
                if edges[i][j] < 0:
                    print("Error: Weight of edges cannot be negative - negative weight was removed.")
                    edges[i][j] = 0
                    edges[j][i] = 0
                if edges[i][j] != edges[j][i]:
                    print("Error: adjacency matrix was not symmetric - made symmetric")
                    edges[j][i] = edges[i][j]
                if edges[i][j]>0:
                    self.totalE += 1
                    self.totalW += edges[i][j]
        

    def clearVisited(self):
        """Resets visitedV, visitedE, and unvisitedE matrices for a new visitation."""
        for i in range(self.totalV):
            self.visitedV[i] = False
            for j in range(self.totalV):
                self.visitedE[i][j] = 0
                self.unvisitedE[i][j] = self.edges[i][j]

    def toFile(self, filename):
        """
        Saves self into a file, that can be read by the class method fromFile.
        The file has the following format:
            The first line contains the number of vertices in that graph
            Followed by one line for each row of the adjacency matrix of the graph: 
                in each row the elements are separated by blanks.
	
        Parameters:
            str filename: name of file where the graph will be saved
	
        Side-Effect: file with filename is created 
        """
        f = open(filename, "w")
        f.write(str(self.totalV) + "\n")
        f.write(str(self))
        f.close()
         

    def __str__(self):
        """Returns a String representation of the graph
        which is a 2-D representation of the adjacency matrix of that graph."""
        res = ""
        for i in range(self.totalV):
            for j in range(self.totalV-1):
                res += str(self.edges[i][j])
                res += " "
            res += str(self.edges[i][self.totalV-1])
            res += "\n"
        return res

    def totalVertices(self):
        """Returns the number of vertices in the graph."""
        return self.totalV

    def totalEdges(self):
        """Returns the number of edges in the graph."""
        return self.totalE

    def totalWeight(self):
        """Returns the total weight of the graph."""
        return self.totalW

    def getEdges(self):
        """Returns a deep copy of the adjacency matrix of the graph."""
        return copy.deepcopy(self.edges)

    def getEdge(self, sourceV, destV):
        """
        Returns the edge between two vertices, i.e. the weight of the path between them

        Parameters:
            int sourceV: sourve vertex
            int destV: destination vertex

        Returns the edge from sourceV to destV
        """
        if sourceV >= 0 and sourceV < self.totalV and destV >= 0 and destV < self.totalV:
            return self.edges[sourceV][destV]
        else:
            return 0

    def isConnected(self):
        """Returns True iff graph is connected."""
        self.clearVisited()
        self.DFSvisit(0)
        for i in range(self.totalV):
            if not self.visitedV[i]:
                return False
        return True

    def DFSvisit(self, vertex):
        """
        Conducts a Depth First Search visit of the unvisited vertices.
        Ties between vertices are broken in numeric order.

        Parameters:
            int vertex: starting vertex for the DFS visit

        Side Effect:
            visitedV is updated to reflect which vertices are visited.
        """
        self.visitedV[vertex] = True
        for i in range(self.totalV):
            if self.edges[vertex][i] != 0 and not self.visitedV[i]:
                self.DFSvisit(i)


###########################  COPY YOUR LAB6 CODE FOR THIS FUNCTION  ####################################
        

    def isSubgraph(self, graph):
        """
        Checks whether self is a subgraph of graph

        Parameters:
            int graph: WeightedGraph that may be supergraph of self

        Assumptions:
            the vertices have the same numbering in both graphs
            
        Returns True if self is a subgraph of graph, and False otherwise
        
        """
        
        isSubset = True
        subgraph= self.getEdges()
        superman= graph.getEdges()

        if graph.totalVertices() < self.totalVertices():
            isSubset = False
            return isSubset
        else:
            for i in subgraph:
                for j in superman:
                    if set(i).issubset(set(j)):
                        isSubset = True
                        break
                    else:
                        isSubset = False
                    if isSubset == False and j == superman[graph.totalVertices()-1]:
                        return False
        return isSubset

