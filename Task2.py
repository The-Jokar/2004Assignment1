import heapq


class TreeMap():

    def __init__(self, roads: list, solulus: list) -> None:
        
        self.unique_tree = [True] * len(roads)
        self.trees = []
        for road in roads:
            if self.unique_tree[road[0]] == True:
                self.trees.append(road[0])
                self.unique_tree[road[0]] = False

        self.num_trees = len(self.trees)
        matrix_size = max(self.trees) + 1

        self.trees_matrix = [[float('inf') for _ in range(matrix_size)] for _ in range(matrix_size)]

        for road in roads:
            self.trees_matrix[road[0]][road[1]] = road[2]
        
        
        self.solulus = solulus

    def escape(self, start: int, exits: list) -> tuple:
        
        time = [float('inf')] * (max(self.trees) + 1)
        time[start] = 0
        
        pred = [None] * (max(self.trees) + 1)
        pred[start] = "source"

        Q = []
        heapq.heappush(Q, (0, start))

        for tree in self.trees:
            if tree is not start:
                heapq.heappush(Q, (self.trees_matrix[start][tree], tree))

        while len(Q) > 0:
            current_tree = heapq.heappop(Q)[1]

            for i in range(len(self.trees_matrix[current_tree])):
                if self.trees_matrix[current_tree][i] is not float('inf'):
                    relaxed_edge = self.relax((current_tree, i, self.trees_matrix[current_tree][i]), time, pred)
                    if relaxed_edge:
                        heapq.heappush(Q, (time[i], i))

        print(time)
        print(pred)

    def relax(self, road: tuple, time: list, pred: list) -> bool:
        new_time = time[road[0]] + road[2]
        if new_time < time[road[1]]:
            time[road[1]] = new_time
            pred[road[1]] = road[0]
            return True
        return False

    def print_matrix(self):
        for row in self.trees_matrix:
            print(row)


tree = TreeMap([(0,1,4), (0,3,2), (3,2,2), (3,0,3), (2,0,1)],  [(0,5,1), (3,2,0), (1,3,1)])

tree.escape(0, [1, 3])
