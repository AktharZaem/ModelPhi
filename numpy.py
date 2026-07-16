class NDArray(list):
    @property
    def shape(self):
        return (len(self),)

    def _operate(self, other, operator):
        if isinstance(other, (int, float)):
            return NDArray([operator(value, other) for value in self])
        return NDArray([operator(left, right) for left, right in zip(self, other)])

    def __truediv__(self, other):
        return self._operate(other, lambda left, right: left / right)

    def __add__(self, other):
        return self._operate(other, lambda left, right: left + right)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self._operate(other, lambda left, right: left - right)

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return NDArray([other - value for value in self])
        return NDArray([left - right for left, right in zip(other, self)])

    def __mul__(self, other):
        return self._operate(other, lambda left, right: left * right)

    def __rmul__(self, other):
        return self.__mul__(other)


def array(values):
    return NDArray(list(values))


def arange(*args):
    if len(args) == 1:
        start = 0
        stop = args[0]
        step = 1
    elif len(args) == 2:
        start, stop = args
        step = 1
    elif len(args) == 3:
        start, stop, step = args
    else:
        raise TypeError("arange expected 1 to 3 arguments")
    return NDArray(list(range(start, stop, step)))
