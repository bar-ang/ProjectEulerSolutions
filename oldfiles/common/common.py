class BoundedQueue:
    def __init__(self, max_size):
        self._q = [None] * max_size
        self._head = 0
        self._size = 0
        self._max_size = max_size

    def __len__(self):
        return self._size

    def max_size(self):
        return self._max_size

    def insert(self, x, extract_if_queue_is_full=False):
        if extract_if_queue_is_full and len(self) >= self._max_size:
            self.extract()
        assert len(self) < self._max_size, "queue is full"
        self._q[(self._head+self._size) % self._max_size] = x
        self._size += 1

    def clear(self):
        self._head = 0
        self._size = 0

    def observe(self, i=0):
        assert i < len(self)
        return self._q[(self._head + i) % self._max_size]

    def extract(self):
        assert len(self) > 0, "queue is empty"
        x = self._q[self._head]
        self._head += 1
        self._head %= self._max_size
        self._size -= 1
        return x
