'''

How to use the tester:

import q1_tester as test

print(test.fuse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

'''


class Fitmons:
    def __init__(self, fitmons):
        self.fitmons = fitmons
        self.original_fitmons = fitmons[:]

    def reset_fitmons(self) -> None:
        self.fitmons = self.original_fitmons[:]

    def get_fit_mons(self) -> list:
        return self.fitmons

    def create_fusioned_fitmon(self, index1, index2) -> list:
        left, right = min(index1, index2), max(index1, index2)

        affinity_left = self.fitmons[left][0]
        affinity_right = self.fitmons[right][2]
        cuteness_score = self.fitmons[left][1] * self.fitmons[left][2] + self.fitmons[right][1] * self.fitmons[right][0]
        cuteness_score = int(cuteness_score)
        new_fitmon = [affinity_left, cuteness_score, affinity_right]

        return new_fitmon

    def fusion_fitmons(self, index1, index2) -> None:
        left, right = min(index1, index2), max(index1, index2)
        new_fitmon = self.create_fusioned_fitmon(left, right)

        # Update the fitmons list 
        #   - left is the index of the new fitmon
        #   - right is the index of the fitmon that is removed
        self.fitmons[left] = new_fitmon
        self.fitmons[right] = None

    def print_fitmons(self) -> None:
        print("Fitmons:")
        for i, fitmon in enumerate(self.fitmons):
            print(f"{i}: {fitmon}")
        print()


def create_orders_of_indices_to_fuse(n):

        def generate_combinations(n):
            combinations = []
            def generate_tuple_pairs(lst) -> None:
                if len(lst) == 1:
                    combinations.append(lst[0])
                    return 
            
                for i in range(len(lst)-1):
                    pair = (lst[i], lst[i+1])
                    new_lst = lst.copy()
                    del new_lst[i+1]
                    new_lst[i] = pair
                    generate_tuple_pairs(new_lst)

            generate_tuple_pairs(list(range(n)))
            return combinations

        
        combinations = generate_combinations(n)

        # recurse to generate all possible combinations
        def get_order_of_combination(combinations):

            order = []
            def recurse_through_combinations(tuples):
                    
                left = tuples[0]
                right = tuples[1]

                if isinstance(left, int) and isinstance(right, int): # both are integers
                    order.append((left, right))

                    return left # the remainder after a fusion

                elif isinstance(left, int) and isinstance(right, tuple): # left is integer, right is tuple
                    order.append((recurse_through_combinations(right), left))
                    return left

                elif isinstance(left, tuple) and isinstance(right, int): # left is tuple, right is integer
                    remainder = recurse_through_combinations(left)
                    order.append((remainder, right))
                    return remainder

                else: # both are tuples
                    remainder = recurse_through_combinations(left)
                    order.append((remainder, recurse_through_combinations(right)))
                    return remainder

            recurse_through_combinations(combinations)
            return order

        # print("Orders:")
        # for i in range(len(combinations)):
        #     print("combination", i+1, ":" , combinations[i], end=" -> ")
        #     print("order of fusing:", get_order_of_combination(combinations[i]))
        return [get_order_of_combination(combinations[i]) for i in range(len(combinations))], combinations

def fuse(list_of_fitmons): # Gets the maximum cuteness score after fusing all fitmons

    fitmons = Fitmons(list_of_fitmons)

    create_orders_of_indices_to_fuse(len(fitmons.get_fit_mons()))

    orders, combinations = create_orders_of_indices_to_fuse(len(fitmons.get_fit_mons()))

    max_cuteness = -float("inf")
    for i in range(len(orders)):
        fitmons.reset_fitmons()

        order = orders[i]

        for index1, index2 in order:
            fitmons.fusion_fitmons(index1, index2)

        max_cuteness = max(max_cuteness, fitmons.get_fit_mons()[0][1])

    return max_cuteness