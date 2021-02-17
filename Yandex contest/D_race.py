from abc import ABC, abstractmethod


class Transport(ABC):
    def __init__(self, number, type, speed):
        self.number = number
        self.type = type
        self.speed = speed

    def countDistance(self, time, cycle):
        return abs(cycle - time * self.speed) % cycle


class Carriage(Transport):
    def __init__(self, number, type, speed):
        super().__init__(number, type, speed)


class Auto(Transport):
    def __init__(self, number, type, speed, fuel):
        super().__init__(number, type, speed)
        if fuel == 98:
            self.speed = speed
        elif fuel == 95:
            self.speed = int(speed / 100 * 90)
        elif fuel == 92:
            self.speed = int(speed / 100 * 80)


class Moto(Transport):
    def __init__(self, number, type, speed, fuel):
        super().__init__(number, type, speed)
        if fuel == 98:
            self.speed = speed
        elif fuel == 95:
            self.speed = int(speed / 100 * 80)
        elif fuel == 92:
            self.speed = int(speed / 100 * 60)


if __name__ == "__main__":
    n, m, t = map(int, input().split())
    mass = []
    for i in range(n):
        a = list(map(int, input().split()))
        if a[1] == 1:
            mass.append(Auto(a[0], a[1], a[2], a[3]))
        elif a[1] == 2:
            mass.append(Moto(a[0], a[1], a[2], a[3]))
        else:
            mass.append(Carriage(a[0], a[1], a[2]))

    max1 = 0
    winner = 0
    for i, transport in enumerate(mass):
        if (transport.speed * t) % m > max1:
            max1 = (transport.speed * t) % m
            winner = i
        elif (transport.speed * t) % m == max1:
            if transport.number < mass[winner].number:
                max1 = (transport.speed * t) % m
                winner = i
    print(mass[winner].number)
