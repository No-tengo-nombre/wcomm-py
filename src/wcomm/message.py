class Message:
    def __init__(self, content):
        self._data = content

    def __iter__(self):
        return iter(self._data)

    def __next__(self):
        return next(self.__iter__())

    def __str__(self):
        return self._data.__str__()
