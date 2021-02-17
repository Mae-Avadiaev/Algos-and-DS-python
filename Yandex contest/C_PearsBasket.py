class PearsBasket():
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return str(self.amount)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.amount})"

    def __floordiv__(self, other):
        resList = list()
        basketAmount = self.amount // other
        rem = self.amount % other
        for i in range(other):
            resList.append(PearsBasket(basketAmount))
        resList.append(PearsBasket(rem))
        return resList

    def __mod__(self, other):
        self.amount = self.amount % other
        return self.amount

    def __add__(self, other):
        return PearsBasket(self.amount + other.amount)

    def __sub__(self, other):
        if self.amount - other < 0:
            self.amount = 0
        else:
            self.amount = self.amount - other