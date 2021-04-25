# python3

"""
Stock Charts Problem.

This problem is from the Google Code Jam —
the annual worldwide programming competition
held by Google.

You want to make an overlaid chart and show
the prices of multiple stocks. In order to
avoid confusion between the stocks shown in
a chart, the lines in an overlaid chart may
not cross or touch. Determine the minimum
number of overlaid charts you need to show
all of the stocks’ prices.

In mathematical language given set A
containing n line segments, find set B such
that no pair of line segments intersect of
maximum length.

I use Bipartite Matching Algorithm to solve
this problem. I simply add an extra source
and extra sink to the Directed Aciclic Graph.
"""

class StockCharts:
    def read_data(self):
        n, k = map(int, input().split())
        stock_data = [list(map(int, input().split())) for i in range(n)]
        return stock_data


    def write_response(self, result):
        print(result)


    def min_charts(self, stock_data):
        max_flow = 0
        adj_matrix = self.make_adj_matrix(stock_data)
        graph = self.make_connections(adj_matrix, stock_data)
        s = len(graph) - 2
        t = len(graph) - 1
        path = self.BFS(s, t, graph)
        while path:
            max_flow += 1
            for ind in range(len(path) - 1):
                self.add_flow(path[ind], path[ind + 1], graph)
            path = self.BFS(s, t, graph)
        c = self.BFS(t, s, graph)
        return len(stock_data) - max_flow


    def make_adj_matrix(self, stock_data):
        adj_matrix = []
        n = len(stock_data)
        for i in range(len(stock_data) * 2 + 2):
            adj_matrix.append([0] * (len(stock_data) * 2 + 2))
        for j in range(n):
            adj_matrix[-2][j] = 1
        for k in range(n):
            adj_matrix[n+k][-1] = 1
        return adj_matrix


    def make_connections(self, adj_matrix, stock_data):
        less_matrix = []
        count = -1
        for i in range(len(stock_data)):
            for k in range(len(stock_data)):
                if i != k:
                    less_matrix.append([(i, k)])
                    count += 1
                else:
                    continue
                for j in range(len(stock_data[i])):
                    if stock_data[i][j] < stock_data[k][j]:
                        less_matrix[count].append(1)
                    else:
                        less_matrix[count].append(0)
        for l in less_matrix:
            if 0 not in l:
                a, b = l[0]
                b += len(stock_data)
                adj_matrix[a][b] = 1
        return adj_matrix


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
        stock_data = self.read_data()
        result = self.min_charts(stock_data)
        self.write_response(result)

if __name__ == '__main__':
    stock_charts = StockCharts()
    stock_charts.solve()


