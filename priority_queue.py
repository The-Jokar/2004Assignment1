class PriorityQueue():

    def __init__(self):
        self.queue = []

    def append(self, data: tuple) -> None:
        self.queue.append(data)
    
    def pop(self) -> int:
        try:
            min_value = float('inf')
            for i in range(len(self.queue)):
                if self.queue[i][1] < min_value:
                    min_value = self.queue[i][1]
                    min_key = self.queue[i][0]

            data = (min_key, min_value)

            self.queue.remove(data)

            return min_key
        
        except IndexError:
            return
        
    def is_empty(self):
        return len(self.queue) < 1
                
    def __str__(self):
        return str(self.queue)