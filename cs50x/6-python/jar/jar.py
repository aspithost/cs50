def main():
    jar = Jar()
    jar.deposit(4)
    # print(str(jar))
    jar.withdraw(2)
    # print(str(jar))


class Jar:
    def __init__(self, capacity=12):
        self._capacity = capacity
        self._size = 0

    def __str__(self):
        return f"🍪" * self._size

    def deposit(self, n):
        if (n + self._size > self._capacity):
            raise ValueError("Can\'t fit in the cookie jar")
        self._size += n

    def withdraw(self, n):
        if (n > self._size):
            raise ValueError("Not that many cookies in jar")
        self._size -= n

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._size


main()