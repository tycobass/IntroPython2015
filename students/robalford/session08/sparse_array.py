# still working on this

class SparseArray:
    def __init__(self, sequence):
        self.length = len(sequence)
        self.sequence = {}
        for i, v in enumerate(sequence):
            if v != 0:
                self.sequence[i] = v

    def __len__(self):
        return self.length

    def __getitem__(self, key):
        if type(key) is not int:
            raise TypeError
        elif key in self.sequence:
            return self.sequence[key]
        elif key < self.length:
            return 0
        elif key >= self.length:
            raise IndexError
        else:
            raise ValueError
