class GifsQueue(object):
    def __init__(self):
        self.queue = []
    def add(self, gif):
        self.queue.insert(0, gif)
    def pop(self):
        return self.queue.pop()
    def get(self, index):
        if abs(index) < len(self.queue):
            return self.queue[index]
    def all(self):
        return self.queue
    def len(self):
    	return len(self.queue)
    def __str__(self):
    	return str(self.queue)
