import q1_tester as test

def fuse(fitmons: list[list]) -> int:

    num_fitmon = len(fitmons)

    fitmon_matrix = [[None for _ in range(num_fitmon)] for _ in range(num_fitmon)]

    for i in range(num_fitmon):
        fitmon_matrix[i][i] = fitmons[i]

    for L in range(2, num_fitmon + 1):
        for i in range(num_fitmon - L + 1):
            j = i + L - 1
            cuteness_max = -1
            for k in range(i, j):
                merged_fitmon = merge(fitmon_matrix[i][k], fitmon_matrix[k+1][j])
                if merged_fitmon[1] > cuteness_max:
                    cuteness_max = merged_fitmon[1]
                    fitmon_matrix[i][j] = merged_fitmon

    
    return fitmon_matrix[0][num_fitmon - 1][1]


def merge(fitmon_1: list, fitmon_2:list):
    cuteness_total = (fitmon_1[1] * fitmon_1[2]) + (fitmon_2[1] * fitmon_2[0])
    return [fitmon_1[0], cuteness_total, fitmon_2[2]]

print(test.fuse([[0, 29, 0.9], [0.9, 91, 0.8], [0.8, 48, 0]])) # 126 according to the assingment specs

print(test.fuse([[0, 48, 0.8], [0.8, 91, 0.9], [0.9, 29, 0]])) # 126 according to the assingment specs

print(test.fuse([[0, 50, 0.3], [0.3, 50, 0.3], [0.3, 50, 0]])) # 24 according to the assingment specs

print(test.fuse([[0, 50, 0.6], [0.6, 50, 0.3], [0.3, 50, 0]])) # 48 according to the assingment specs

print(test.fuse([[0, 50, 0.3], [0.3, 50, 0.3], [0.3, 80, 0]])) # 33 according to the assingment specs

print(test.fuse([[0, 50, 0.6], [0.6, 98, 0.4], [0.4, 54, 0.9], [0.9, 6, 0.3],
                [0.3, 34, 0.5], [0.5, 66, 0.3], [0.3, 63, 0.2], [0.2, 52, 0.5],
                [0.5, 39, 0.9], [0.9, 62, 0]] )
                ) # 132 according to the assingment specs