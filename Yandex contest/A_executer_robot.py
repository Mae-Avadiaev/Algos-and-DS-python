class Robot():
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.way = list()
        self.init_point()

    def init_point(self):
        self.way = list()
        self.way.append((self.x, self.y))

    def move(self, commands):
        a = list(commands)
        self.init_point()
        for command in a:
            if command == 'N':
                self.y += 1
                self.way.append((self.x, self.y))
            if command == 'S':
                self.y -= 1
                self.way.append((self.x, self.y))
            if command == 'W':
                self.x -= 1
                self.way.append((self.x, self.y))
            if command == 'E':
                self.x += 1
                self.way.append((self.x, self.y))
        return self.way[-1]

    def path(self):
        return self.way
