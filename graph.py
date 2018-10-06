class Node:
    """mixin class for A*"""
    
    def heuristic(self, goal):  # must be monotonic
        return 0

    def decorated_neighbors(self):
        def complete(u, way=None, dist=1):
            return u, way, dist
        for neighbor in self.neighbors():
            if type(neighbor) is tuple:
                yield complete(*neighbor)
            elif isinstance(neighbor, Node):
                yield neighbor, None, 1
            else:
                yield type(self)(neighbor), None, 1

    def is_goal(self):
        return False

    def astar(self, goal=None):
        cl, op, parent = set(), {self}, {}
        g, f = {self: 0}, {self: self.heuristic(goal)}
        while op:
            t = min(op, key=f.get)
            op.remove(t)
            if t == goal or t.is_goal():
                path = []
                while t is not self:
                    t, way = parent[t]
                    path.append(way)
                path.reverse()
                return path
            cl.add(t)
            for u, way, dist in t.decorated_neighbors():
                if u not in cl:
                    gu = g[t] + dist
                    if u not in op or gu < g[u]:
                        parent[u] = t, way
                        g[u], f[u] = gu, gu + u.heuristic(goal)
                        op.add(u)

    def bfs(self):
        import collections
        queue = collections.deque([(self, 0)])
        visited = set()
        while queue:
            visit = start, start_dist = queue.popleft()
            if start not in visited:
                yield visit
                visited.add(start)
                for u, way, dist in start.decorated_neighbors():
                    queue.append((u, start_dist + dist))
            elif start.is_goal():
                return start
