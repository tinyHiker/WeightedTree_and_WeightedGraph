

## WeightedGraph Class

### Overview
The `WeightedGraph` class provides a structured way to work with weighted graphs, representing them internally via a modified adjacency matrix approach. Note that the graph considered here is simple, meaning the adjacency matrix will be symmetric.

### Key Characteristics
- **Simplicity:** The graph does not have loops.
- **Weights:** Edges may have associated positive integer weights.
- **Adjacency Matrix Representation:** The graph is internally stored as an adjacency matrix, where the entry \(a(i, j)\) is:
    - 0 if there is no edge between vertices \(i\) and \(j\), or
    - A positive integer representing the weight of the edge between vertices \(i\) and \(j\).

### Usage
This class is capable of:
- Creating new instances through data extracted from a given file.
- Instantiating a random graph based on specified parameters like the seed, vertex count, density, and maximum edge weight.
- Clearing visited vertices and edges in the graph to perform fresh graph visitations.
- Writing its representation into a file.

### Methods
1. **fromFile(filename: str) -> WeightedGraph**
    - Instantiates a `WeightedGraph` object based on graph data read from a specified file.
    
2. **readGraph(filename: str) -> tuple**
    - Reads graph data from a file and returns a tuple with the vertex count and the edges.

3. **newRandom(seed: int, vertices: int, density: int, maxweight: int) -> WeightedGraph**
    - Creates a new random `WeightedGraph` according to the given parameters.

4. **clearVisited()**
    - Resets matrices used to track visited vertices and edges, preparing for a new graph visitation.

5. **toFile(filename: str)**
    - Saves the `WeightedGraph` object into a specified file.

6. **isConnected() -> bool**
    - Checks if the graph is connected, returning `True` if it is and `False` otherwise.

7. **DFSvisit(vertex: int)**
    - Conducts a Depth-First Search (DFS) visit starting from a specified vertex.

8. **isSubgraph(graph: WeightedGraph) -> bool**
    - Checks if the current graph (`self`) is a subgraph of another specified graph.

### Handling of Incorrect Data
- The `WeightedGraph` class is designed to handle incorrect data judiciously by issuing error messages and making necessary adjustments. For example:
    - It handles asymmetric adjacency matrices by ensuring symmetry.
    - Negative weights and looped edges are removed and appropriate error messages are displayed.

### Usage Restrictions
- This class is not to be modified, circulated, or posted without the permission of Sophie Quigley.
- There is an exception for modifying the `isSubgraph` method at the end of the class.

### Example Usage
```python
# Instantiating a WeightedGraph from a file.
wg_from_file = WeightedGraph.fromFile("graph_data.txt")

# Creating a new random WeightedGraph.
wg_random = WeightedGraph.newRandom(seed=42, vertices=5, density=60, maxweight=10)

# Checking if the graph is connected.
is_conn = wg_random.isConnected()

# Saving the graph to a file.
wg_random.toFile("saved_graph.txt")
```

### Contribution & Modification
Contribute or modify only the `isSubgraph` method unless permission is granted by Sophie Quigley for further modifications.

### Note
Always validate and ensure the correctness of your graph data before utilizing this class to avoid unintentional behaviors or errors in your graph algorithms.

## WeightedTree Class
The `WeightedTree` class extends a `WeightedGraph` to represent a tree. This particular implementation comes with a suite of methods that support adding edges, checking for a path between two vertices, and more. But, I noticed a couple of points that might need further attention or explanation:

### Multiple `__init__` Methods

There are two `__init__` methods, which isn't typical in Python classes. When multiple `__init__` methods are defined, only the last one is used. Instead, consider using default values or `*args`/`**kwargs` to allow different sets of parameters:

```python
def __init__(self, vertices, edges=None):
    self.inPath = [0] * vertices 
    if edges is None:
        edges = [[0] * vertices for _ in range(vertices)]
    super().__init__(vertices, edges)
```

### Class Method for Creating Minimum Spanning Tree (MST)

The `MSTfromGraph(cls, graph)` class method is designed to create a Minimum Spanning Tree from a graph. Here, it is crucial to ensure that the MST is formed correctly, considering the sorted edges and avoiding cycles.

### Sorting Edges

The method `sortEdges(cls, graph)` aims to create a list of all edges and then sort them by weight. This is straightforward and will be crucial in creating an MST using algorithms like Kruskal's.

### Method for Adding Edges

The method `addEdge(self, newedge)` modifies the graph by adding a new edge between two vertices with a specific weight.

### Method for Checking Paths

`isPath(self, i, j)` recursively checks if there's a path from vertex `i` to vertex `j`. The DFS (Depth-First Search) method named `DFSvisit` is mentioned but isn't provided in the code snippet. Make sure that it's implemented in either `WeightedTree` or `WeightedGraph`.

### Additional Methods from Lab 6

- `isTree(self)`: Ensures the graph is connected and edges equal vertices minus one, which are characteristics of a tree in graph theory.
  
- `isSpanningTree(self, graph)`: Checks whether `self` is a spanning tree of `graph`. Note that the method name is using camelCase and should be `is_spanning_tree` to be consistent with Python naming conventions.

### General Note

Make sure that all needed methods from `WeightedGraph` are correctly implemented and accessible, considering that `WeightedTree` extends it. Ensure proper testing for all the methods, especially those involving the creation and validation of the MST, as these can be prone to logical errors that might be hard to debug without thorough testing.

Lastly, it's good practice to use snake_case for function and method names in Python (e.g., `is_spanning_tree