# python3

"""
Assigning Airline Crews to Flights Problem.

In this problem we have bunch of flights and
has a set of crews that can work on those
flights and we need to assign crews to as
many flights as possible and output all the
assignments.

In mathematical words we are given a bipartite
graph and we need to apply an algorithm for
finding maximum matching.

I use Bipartite Matching algorithm.
First I start with bipartite graph, direct all
the edges left to right, add a source and a
sink node, connect them to the graph and set
all the capacities of edges to 1.
Secondly I compute Maxflow.
And finally I return corresponding matching.
"""

class MaxMatching:
    def read_data(self):
        n, m = map(int, input().split())
        adj_matrix = [list(map(int, input().split())) for i in range(n)]
        return adj_matrix


    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))


    def find_matching(self, adj_matrix):
        max_flow = 0
        result = [-1] * (len(adj_matrix))
        n = len(adj_matrix)
        matching = [-1] * n
        graph = from_adj_to_graph(adj_matrix)
        s = len(graph) - 2
        t = len(graph) - 1
        path = self.BFS(s, t, graph)
        while path:
            for ind in range(len(path) - 1):
                self.add_flow(path[ind], path[ind + 1], graph)
            path = self.BFS(s, t, graph)
        c = self.BFS(t, s, graph)
        while c:
            result[c[2]] = c[1] - len(adj_matrix)
            for ind in range(len(c) - 1):
                self.add_flow(c[ind], c[ind + 1], graph)
            c = self.BFS(t, s, graph)
        return result


    def add_flow(self, x, y, graph):
        graph[x][y] = 0
        graph[y][x] = 1


    def BFS(self, s, t, graph):
        prev = [None] * len(graph)
        visited = [False] * len(graph)
        queue = []
        queue.append(s)
        visited[s] = True
        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(graph[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    prev[ind] = u
        path = []
        if visited[t]:
            path.append(t)
            b = prev[t]
            while b is not None:
                path.append(b)
                b = prev[b]
            path.reverse()
            return path
        else:
            return False


    def solve(self):
        adj_matrix = self.read_data()
        matching = self.find_matching(adj_matrix)
        self.write_response(matching)


def from_adj_to_graph(adj_matrix):
    graph2 = []
    for i in range(len(adj_matrix) + len(adj_matrix[0]) + 2):
        graph = [0] * (len(adj_matrix) + len(adj_matrix[0]) + 2)
        graph2.append(graph)
    n = len(adj_matrix)
    for k in range(len(adj_matrix)):
        for h in range(len(adj_matrix[k])):
            graph2[k][n+h] = adj_matrix[k][h]
    for q in range(len(adj_matrix)):
        graph2[-2][q] = 1
    for w in range(len(adj_matrix[0])):
        graph2[n+w][-1] = 1
    return graph2


if __name__ == '__main__':
    max_matching = MaxMatching()
    max_matching.solve()

