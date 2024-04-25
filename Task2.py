from priority_queue import PriorityQueue as pq


class TreeMap():

    def __init__(self, roads, solulus):
        
        self.unique_trees = []
        for road in roads:
            if road[0] not in self.unique_trees:
                self.unique_trees.append(road[0])

        self.num_trees = len(self.unique_trees)
        matrix_size = max(self.unique_trees) + 1

        self.trees_matrix = [[float('inf') for _ in range(matrix_size)] for _ in range(matrix_size)]

        for road in roads:
            self.trees_matrix[road[0]][road[1]] = road[2]
        
        self.solulus = solulus

    def shortest_path(self, start):
        
        Q = pq()
        Q.append((start, 0))
        
        for tree in self.unique_trees:
            if tree is not start:
                Q.append((tree, self.trees_matrix[start][tree]))

        dist = [float('inf')] * (max(self.unique_trees) + 1)
        dist[start] = 0
        
        pred = [None] * (max(self.unique_trees) + 1)
        pred[start] = "source"

        visited = [False] * (max(self.unique_trees) + 1)

        current_tree = Q.pop()
        
        min_dist = float('inf')
        min_tree = None

        for j in range(len(dist)):
            if dist[j] != float('inf'):
                if visited[j] == False and dist[j] < min_dist:
                    min_dist = dist[j]
                    min_tree = j

        visited[current_tree] = True

        for i in range(len(self.trees_matrix[current_tree])):
            if self.trees_matrix[min_tree][i] != float('inf'):
                if visited[i] == False:
                    new_dist = dist[min_tree] + self.trees_matrix[min_tree][i]
                    if new_dist < dist[i]:
                        dist[i] = new_dist

        print(dist)
        print(visited)
        print(Q)

    def print_matrix(self):
        for row in self.trees_matrix:
            print(row)


tree = TreeMap([(0,1,4), (0,3,2), (0,2,3), (3,1,2), (3,0,3), (2,0,1)],  [(0,5,1), (3,2,0), (1,3,1)])

tree.shortest_path(0)
