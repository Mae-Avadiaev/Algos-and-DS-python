from abc import ABC, abstractmethod


class AbstractCat(ABC):
    def __init__(self):
        self.weight = 0
        self.reserve = 0

    def __str__(self):
        return f"{self.__class__.__name__} ({self.weight})"

    def eat(self, amount):
        p_weight = (amount + self.reserve) // 10
        new_reserve = (amount + self.reserve) % 10
        while self.weight < 100 and p_weight > 0:
            self.weight += 1
            p_weight -= 1
        self.reserve = new_reserve + (p_weight * 10)


class Kitten(AbstractCat):
    def __init__(self, weight):
        super().__init__()
        self.weight = weight

    def meow(self):
        return "meow..."

    def sleep(self):
        return "Snore" * (self.weight // 5)


class Cat(Kitten):
    def __init__(self, weight, name):
        super().__init__(weight)
        self.name = name

    def meow(self):
        return "MEOW..."

    def get_name(self):
        return self.name

    def catch_mice(self):
        return "Got it!"
