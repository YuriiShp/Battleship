class Ship:

    def __init__(self):
        self.coordinates = None
        self.position = 0

    def rotate(self):
        for i in range(len(self.coordinates)):
            x, y = self.coordinates[i]
            if self.position == 0:
                x -= i
                y -= i
            else:
                x += i
                y += i
            self.coordinates[i] = (x,y)
        if self.position == 0:
            self.position = 1
        else:
            self.position = 0

    def locate(self, position):
        dx, dy = position
        result = []
        for (x,y) in self.coordinates:
            pos_x = x + dx
            pos_y = y + dy
            result.append((pos_x,pos_y))
        return result


class OneDecker(Ship):

    def __init__(self):
        super().__init__()
        self.coordinates = [(0,0)]
        self.name = 'one_decker'


class TwoDecker(Ship):

    def __init__(self):
        super().__init__()
        self.coordinates = [(0,0), (0,1)]
        self.name = 'two_decker'


class ThreeDecker(Ship):

    def __init__(self):
        super().__init__()
        self.coordinates = [(0,0), (0,1), (0,2)]
        self.name = 'three_decker'


class FourDecker(Ship):

    def __init__(self):
        super().__init__()
        self.coordinates = [(0,0), (0,1), (0,2), (0,3)]
        self.name = 'four_decker'

# ship = FourDecker()
# ship.rotate()
# print(ship.locate((5,0)))
# ship.rotate()
# print(ship.locate((5,0)))
