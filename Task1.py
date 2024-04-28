def fuse(fitmons: list) -> int:
    """
		Function description: This functon takes a list of fitmon and calculates the maximum cuteness score that can be achieved by merging the fitmon together two at a time. 

		Approach description: As there is a number of merges being performed and the same result will be used multiple times dynamic programming was the main basis used in optimally calculating the result,
        using a bottom up iterative approach it starts by solving the base level merges before building up level by level, all based on the optimal matrix multiplication algorithm which calculates the minimum 
        number of multiplications needed to multiply all the given matricies, instead using fitmon and finding the max cuteness score I could develop a similar algorithm to synamically solve the probelm.

		Input: 
			fitmons: a list of lists  that contains fitmon, each fitmon has the format [left affinity score, cuteness, right affinity score]
		
		Output: An integer which represents the max cuteness score that can be achieved from the given list of fitmon 
		
		Time complexity: O(n^3), where n is the number of fitmon in the input list 

		Time complexity analysis : Given n is the number of fitmon in the input list,
		
			The base case costs n time as it iterates through the length of the list once 

			The iterative step cost n^3 where the outer most for loop iterate from 2 (the step after the base case) to n + 1 which is simplified to jsut n
            the inner for loop iterates from n - L (the value of the outer for loop) + 1 which is also simplfied to n and the inner most for loop operates from 
            i to j which at max can be range n the merge routing inside runs in O(1) thus giving O(n*n*n) = O(n^3)
			
		Space complexity: O(n^2),  where n is the number of fitmon in the input list

		Space complexity analysis: the fitmon are stored in matrix which is n * n in size giving O(n^2)
		
	"""
    #gets the total number of fitmon
    num_fitmon = len(fitmons)

    #intitialise a matrix containing all None used to store results of fusions between two fitmon with size num_fitmon x num_fitmon
    fitmon_matrix = [[None for _ in range(num_fitmon)] for _ in range(num_fitmon)]

    #base case, stores each fitmon in matrix at appropriate location across the diagonal of the matrix
    for i in range(num_fitmon):
        fitmon_matrix[i][i] = fitmons[i]

    #outer most loop iterates through the level of multiplication taking place, e.g at 2, 2 fitmon have been merged up to num_fitmon + 1 (the total number of fitmon, all fitmon are merged)
    for L in range(2, num_fitmon + 1):
        #inner loops iterate through all possible combinations of i (one fitmon) and j (another fitmon) based on the chain length
        #the reuslt which produces the largest cuteness score is input into the matrix at the current level
        #e.g if we are at chain length three what combination of ABC gives us a higher cuteness score, A x BC or AB x C
        for i in range(num_fitmon - L + 1):
            j = i + L - 1
            #stores the max cuteness for the current combinations intially -1
            cuteness_max = -1
            for k in range(i, j):
                #performs merging routine between the two fitmon and stores current merge result
                merged_fitmon = merge(fitmon_matrix[i][k], fitmon_matrix[k+1][j])
                #if the result of the merged fitmon is greater than the current max score
                #then update the max score and store it in the matrix at the appropriate loaction
                if merged_fitmon[1] > cuteness_max:
                    cuteness_max = merged_fitmon[1]
                    fitmon_matrix[i][j] = merged_fitmon

    #return the final merged fitmons cuteness score as integer which is the maximum possible
    return int(fitmon_matrix[0][num_fitmon - 1][1])


def merge(fitmon_1: list, fitmon_2:list) -> list:
    """
		Function description: This function performs the merging operation of two fitmon and returns the new merged fitmon 

		Input: 
			fitmon_1: the left firmon to be merged
            fitmon_2: the right fitmon to be merged
		
		Output: a fitmon wiht the updates left affinity cuteness score and right affinity
		
		Time complexity: O(1)

		Time complexity analysis : performs a number of simple operations all of which are O(1)
			
		Space complexity: O(1)

		Space complexity analysis: does not create anny new arrays only a new fitmon
		
	"""
    #calculates the new cuteness score based on a merge between 2 fitmon
    cuteness_total = int((fitmon_1[1] * fitmon_1[2]) + (fitmon_2[1] * fitmon_2[0]))
    #returns the next fitmon with updated left and right affinity scores and new cuteness
    return [fitmon_1[0], cuteness_total, fitmon_2[2]]