# python3

"""
Evacuation (Maximum flow in a network) problem.

The goal is to evacuate everybody from the city
as fast as possible and to find out what is the
maximum number of people that can be evacuated
each hour given the capacities of all the roads.

I have used Edmonds-Karp Algorithm to solve this
problem. The reason why is Ford-Fulkerson Algorithm
has good runtime but can be very slow if graph has
large capacities.
But we have a fix for this. So we use the
Ford-Fulkerson Algorithm, always choosing the
shortest path. We use Breadth First Search for
this.

So I start with zero flow, and begin repeatedly
add flow like this: I compute the residual network,
add new flow to the flow in the residual network
and see if there's a source-sink path.
If there's no source-sink path I return the flow.
"""

counter = 0

class Edge:

    def __init__(self, u, v, capacity):
        global counter
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0
        self.id = counter
        counter += 1


class FlowGraph:

    def __init__(self, n):
        self.edges = []
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        self.edges[id].capacity -= flow
        self.edges[id ^ 1].capacity += flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph


def max_flow(graph, from_, to):
    flow = 0
    while True:
        p = BFS(graph, from_, to)
        if p == -1:
            return flow
        p.sort(key=lambda x: x.capacity, reverse=True)
        x = p[-1].capacity
        for ed in p:
            graph.add_flow(ed.id, x)
        flow += x


def BFS(graph, from_, to):
    visited = [False] * (len(graph.graph))
    prev = [None] * (len(graph.graph))
    queue = []
    p = []
    queue.append(from_)
    visited[from_] = True
    while queue:
        a = queue.pop(0)
        for i in graph.graph[a]:
            if graph.edges[i].capacity != 0:
                if not visited[graph.edges[i].v]:
                    queue.append(graph.edges[i].v)
                    visited[graph.edges[i].v] = True
                    prev[graph.edges[i].v] = a
    if prev[to] is None:
        return -1
    at = to
    while prev[at] is not None:
        p.append(at)
        at = prev[at]
    p.append(at)
    p.reverse()
    path =[]
    for j in range(len(p) - 1):
        for k in graph.graph[p[j]]:
            if graph.edges[k].capacity != 0:
                if graph.edges[k].u == p[j] and graph.edges[k].v == p[j + 1]:
                    path.append(graph.edges[k])
                    break
    return path



if __name__ == '__main__':
    graph = read_data()
    print(max_flow(graph, 0, graph.size() - 1))


