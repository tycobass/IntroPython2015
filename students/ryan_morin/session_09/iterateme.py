class IterateMe_1(object):
    """
    About as simple an iterator as you can get:

    returns the sequence of numbers from zero to 4
    ( like range(4) )
    """
    def __init__(self, stop=10, step=1):
        self.current = -1
        self.stop = stop
        self.step = step
    def __iter__(self):
        return self
    def __next__(self):
        self.current = (self.current + self.step)
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

if __name__ == "__main__":

    print("Testing the iterator")
    it = IterateMe_1(20,2)
    for i in it:
        if i > 10: break
        print (i)

    for i in it:
        print(i)