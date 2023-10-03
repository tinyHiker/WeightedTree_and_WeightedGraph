from WeightedGraph import WeightedGraph

class WeightedTree(WeightedGraph):
    """
    WeightedTree objects are WeightedGraphs that are trees.
    They are internally represented using modified adjacency matrices where each entry a(i,j) is either
    - 0 if there is no edge between vertices i and j
    - a positive integer representing the weight of the edge between i and j if there is such an edge
    Note that the graph is simple and therefore the adjacency matrix representation is symmetric
    """

###########################  DO NOT MODIFY THESE FUNCTIONS  ####################################


    def __init__(self, vertices, edges):
        self.inPath = [0]*vertices # used to check for an existing path between 2 vertices
        super().__init__(vertices, edges)

    def __init__(self, vertices):
        self.inPath = [0]*vertices # used to check for an existing path between 2 vertices
        edges = []
        for i in range(vertices):
            edges.append(list([0]*vertices))
        super().__init__(vertices, edges)


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
        return WeightedTree(vertices, edges)

###########################  START YOUR CODE HERE  ####################################


    @classmethod
    def MSTfromGraph(cls, graph):
        """
	      Creates a WeightedTree that is a MST of graph.  
	
        Parameters:
            WeightedGraph graph: graph whose MST will be computed
	
        Returns a WeightedTree MST for the graph, or None if this is not possible. 
	      """
        if not graph.isConnected():
            return None
        else:
            sortedEdges= WeightedTree.sortEdges(graph)
            MST = WeightedTree(graph.totalVertices())
            while not MST.isTree():
                if MST.canAdd(sortedEdges[0]):
                    MST.addEdge(sortedEdges[0])
                sortedEdges.pop(0)
                
        return MST
 
    @classmethod
    def sortEdges(cls, graph):
        
        """
	      Sort the edges of the graph in order of increasing weight 
	
        Parameters:
            WeightedGraph graph: graph whose edges will be sorted
	
        Returns a sorted list of the edges of the graph.
        Each edge is a triple of format (weight, v1, v2) 
	      """
        edgelist=[]
        verticeCount = graph.totalVertices()
        

        for i in range(verticeCount):
            for j in range(verticeCount):
                if graph.getEdge(i,j)>0:
                    edgelist.append((graph.getEdge(i,j), i, j))


        edgelist.sort(key = lambda i:i[0]) 
        return edgelist                
            
    def canAdd(self, newedge):
        """
        Checks whether a new edge can be added to self without introducing a cycle
	
        Parameters:
            triple newedge: edge that could be added.  Its format is (weight,v1,v2)
        
        Returns True if newedge can be added to self without introducing a cycle, and False otherwise
        """
        firstVertex= newedge[1]
        secondVertex= newedge[2]

        if firstVertex == secondVertex:
            return False
        elif self.isPath(firstVertex, secondVertex):
            return False
        else:
            return True

    def isPath(self,i,j):

        """
        Determines whether there is a path from i to j in self
        by trying to find such a path recursively, backtracking when necessary
	
        Parameters:
            int i,j: vertices in self which may or may not be connected
        
        Returns True if self contains a path from i to j, and False otherwise
        
        Side-Effect:
            self.inPath[] is used and modified by this method as follows (where v is a vertex):
            - self.inPath[v] = 0 when self does not include any edges ajacent to v yet
            - self.inPath[v] = 1 when self does include at least one edge adjacent to v,
                            but v is not yet part of the path  
            - self.inPath[v] = 2 when self does include at least one edge adjacent to v,
                            and v is already part of the path   
        """
        self.clearVisited()
        self.DFSvisit(i)
        if self.visitedV[j] == False:
            return False
        else:
            return True


            


    def addEdge(self,newedge):
        """
        Adds a new edge to self
        
        Parameters:
            triple newedge: edge that will be added.  Its format is (weight,v1,v2)
            
        Retrns nothing
        """
        weight = newedge[0]
        firstVertex = newedge[1]
        secondVertex = newedge[2]

        self.edges[firstVertex][secondVertex] = weight
        self.edges[secondVertex][firstVertex] = weight
        self.totalW += weight
        self.totalE +=1




###########################  COPY YOUR LAB6 CODE FOR THESE FUNCTIONS  ####################################

    def isTree(self):
        """
        Checks whether self is tree
            
        Returns True if self is a tree, and False otherwise
        """
        if not self.isConnected():
            return False
        if not(self.totalEdges() == self.totalVertices()-1):
            return False
        return True
            
    def isSpanningtree(self,graph):
        """
        Checks whether self is a spanning tree of a graph

        Parameters:
            int graph: WeightedGraph that may have self as a spanning tree

        Assumptions:
            the vertices have the same numbering in both graphs
                
        Returns True if self is a spanning tree of graph, and False otherwise
        """
        if self.isTree() and (self.totalVertices() == graph.totalVertices()) and self.isSubgraph(graph):
            return True
        else:
            return False
