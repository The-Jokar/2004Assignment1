#import heapq to use min heap
import heapq

class TreeMap():

    def __init__(self, roads: list, solulus: list) -> None:
        """
            Function description: This function initialises a number of class variables which are used in calculating the shortest path 

            Approach description: The problem required findimg the shortest path so dijkstra's algorithm was the most optimal way to do this as it was a graph with non-negative weights.
            The main part of the approach involves modifying the input to a slightly modified djikstras in orer to make sure there is only one dijkstras call neded to calculate the shortest path
            and ensuring a good worst case. The input is modified so that the adjacency list used when calculating the shortest path contain two layers, both layers are inside the same adjacency list the
            first layer being from 0 to T and the second layer being from T + 1 to 2T. both layers contian the same roads e.g from 0 to 1 takes 2 in the second layer from T + 1 to T + 2 takes 2 as well.
            The only way to access the seocnd layer is through the solulus which are implemented into the adjacency list as roads where the tree it teleports to is the end of the road and the road takes
            desturction time to travel. Finally in the escape function the exits are modified to be in the seocnd layer of the graph thus the shortest path calculated ensures at least one solulu
            tree is destroyed before exiting the forest. 

            Input: 
                roads: a list of directed roads (edges) denoted by (start tree, end tree, time to travel)
                solulus: a list of solulus, special nodes which one needs to be destroyed to reach the exit and after destoryiung teleports to a differrent node, denoted by (solulu tree, time to destroy, node to teleport to)
            
            Output: None
            
            Time complexity: O(T + R) where T is the number of unique tree and R is the number of roads

            Time complexity analysis : Given T is the number fo unique tree and R is the number of roads,
            
                The creation of the adjacency list costs T time to make and adding each road into the adjacency list costs a total of 2R time as the list adds the roads twice one for each
                layer which is simplified to R
                
            Space complexity: O(T + R) where T is the number of unique tree and R is the number of roads

            Space complexity analysis: The creation of the adjacency list costs T + R as there are T lists with a total of R tuples in them
		
	    """
        #initialises a blank list which will contian all the trees
        self.trees = []

        #adds all possible trees to the list
        for road in roads:
            self.trees.append(road[0])
            self.trees.append(road[1])

        #gets the largest tree
        self.num_trees = max(self.trees)
        #calculates the size of the adjacency list making it twice as big as the max so it can contain two layers
        list_size = (max(self.trees) + 1) * 2

        #creates the adjaceny list based on the calculated size
        self.trees_list = [[] for _ in range(list_size)]

        #inputs roads into the adjaceny list, inputs each road twice once in the frist layer and once in the second layer 
        for road in roads:
            self.trees_list[road[0]] += [(road[1], road[2])]
            self.trees_list[road[0] +  self.num_trees + 1] += [(road[1] +  self.num_trees + 1, road[2])]
        
        #iserts the solulus as roads into the adjaceny list creating a path between the first layer adn the second layer where the solulu node to teleport node takes destruction time
        for solulu in solulus:
            self.trees_list[solulu[0]] += [(solulu[2] + self.num_trees + 1, solulu[1])]


    def escape(self, start: int, exits: list) -> tuple:
        """
            Function description: This function takes a starting tree and a list of exits and then using a grpah it finds the shortest distance from the source to an exit
            after destroying one solulu tree then returns the minimum time to exit the forest and the route it took 

            Input: 
                start: the starting tree represented as an integer
                exits: a list of exit trees 
            
            Output: a tuple containing the exit time and exit route starting from the start tree
            
            Time complexity: O(Rlog(T)), where R is the total number of roads and T is number of unique trees

            Time complexity analysis : Given R is the total number of roads and T is number of unique trees,
            
                The outer most while loop runs in T time as each vertex is run throiugh once, and each time poping the current min costs log(R) as a min heap is used,
                the inner for loop visits each road once giving O(R) and the cost of updating the priority Q is log(T), thus the overall time complexity is
                O(Tlog(R) + Rlog(T)) however, the Rlog(T) term dominates with a worst worse case giving the time complexity O(Rlog(T))
                
            Space complexity: O(R + T),  where R is the total number of roads and T is number of unique trees

            Space complexity analysis: as the min heap takes up R space and pred and time both take up 2T space with a total 4t space simplified to T giving O(R + T)
            
        """
        #updates the exits so they are in the second layer of the graph
        updated_exits = []
        for exit in exits:
            updated_exits.append(exit + self.num_trees + 1)

        #initialises a time matrix which stores the current time it takes to get to a given tree, initialised all times to infinity
        time = [float('inf')] * ((max(self.trees) + 1) * 2)
        #sets starting distance to 0
        time[start] = 0
        
        #stores the predecessor of a given tree initialised to none
        pred = [None] * ((max(self.trees) + 1) * 2)
        #sets the starting node to be source
        pred[start] = "source"

        #creates the min heap which will store the next tree to be explored
        Q = []
        heapq.heappush(Q, (0, start))

        #while there are still trees to be explored keep exploring
        #exits loop after every possible tree is explored
        while len(Q) > 0:
            #pop the tree which has the least time from the start and store it in current_tree
            current_tree = heapq.heappop(Q)[1]

            #iterates through each adjacent tree to the current tree
            #exits loop after all adjacent trees to the current trees have been explored
            for i in range(len(self.trees_list[current_tree])):
                #attempts to relax an edge between the current tree and an adjacent tree
                relaxed_edge = self.relax((current_tree, self.trees_list[current_tree][i][0], self.trees_list[current_tree][i][1]), time, pred)
                #if the edge/road is relaxed push the tree to the min heap with the updated time from the start
                if relaxed_edge:
                    heapq.heappush(Q, (time[i], self.trees_list[current_tree][i][0]))

        #initialises a fastest exit time to be infinity and the fastes exit to be none
        fastest_exit_time = float("inf")
        fastest_exit = None
        
        #loop iterates through each exit and finds which is the fastest and the amount of itme it takes
        for exit in updated_exits:
            #if the current exit is faster than current fastes exit time
            #then update fastest exit time to new time and fastest exit to current exit
            if time[exit] < fastest_exit_time:
                fastest_exit_time = time[exit]
                fastest_exit = exit

        #if there is no exit, or the exit cannot be reached, or time to exit is infinity then no path
        if fastest_exit == None or fastest_exit_time == float('inf'):
            return None

        #intitalise the index i to start at fastes exit and list which will contain the exit route
        i = fastest_exit
        exit_route = []

        #while loop which continues iterating until the full exit route is found
        while i != 'source':
            #if this is not first item to be added run extra check
            if exit_route != []:
                #check if the previous tree added is the same as the current tree
                #stops edge case where the solulu teleports to itself resulting in the tree being added twice
                #if its this case move to next predecessor and dont add duplicate
                if exit_route[0] == i:
                    i = pred[i]
                
                #else not edge case run normal
                else:
                    #if the current value is in the second layer adjust the index to make it the appropriate value it would be in the first layer
                    if i >= (self.num_trees + 1):
                        #adds the predecessor to the exit route
                        exit_route = [i - (self.num_trees + 1)] + exit_route
                    else:
                        #if in teh first layer add without updating value
                        exit_route = [i] + exit_route
                    #update i to be the next predecessor
                    i = pred[i]

            #else this is the first item and cant be a duplicate so run normal
            else:
                if i >= (self.num_trees + 1):
                        exit_route = [i - (self.num_trees + 1)] + exit_route
                else:
                    exit_route = [i] + exit_route
                i = pred[i]
                
        #returns fastest exit time and the route it took
        return (fastest_exit_time, exit_route)


    def relax(self, road: tuple, time: list, pred: list) -> bool:
        """
            Function description: This function takes a givin road and calulates the new time based on the current tree and updates time and pred if the new time is faster than the current
            stored time, relaxes a road (edge) 

            Input: 
                road: a tuple containing (start tree, end tree, time to travel)
                time: a list containing the current fastest time taken to reach a node
                pred: a list containing the current predecessor for each node
            
            Output: boolean value, true if the dge is relaxed and flase if its not 
            
            Time complexity: O(1)

            Time complexity analysis : performs a number of O(1) operations such as updating values and simple calculations
                
            Space complexity: O(1)

            Space complexity analysis: does not create any new arrays only updates existing ones
            
        """
        #calculates the new time to be the current time it took to get to the first tree (road[0]) + the time from the first tree to the next tree (road[2])
        new_time = time[road[0]] + road[2]
        #if the calculated time is faster than the current time its take to get to the tree then update the time and the predecessor to reflect faster route
        if new_time < time[road[1]]:
            time[road[1]] = new_time
            pred[road[1]] = road[0]
            #return true if the edge/road was relaxed
            return True
        #return false if the edge/road was not relaxed
        return False