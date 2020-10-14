from ships import *
from pynput import keyboard
from time import sleep
import random


class Game:

    def __init__(self):
        self.player = None
        self.player_ships = {'one_decker': [],
                             'two_decker': [],
                             'three_decker': [],
                             'four_decker': []}
        self.player_turns = {'hit': [], 'miss': []}
        self.comptr_ships = {'one_decker': [],
                             'two_decker': [],
                             'three_decker': [],
                             'four_decker': []}
        self.comptr_turns = {'hit': [], 'miss': []}
        self.comptr_logic_var = {'hit': [], 'miss': []}
        self.forbiden_zone = set()
        self.set_interrupt = False
        self.set_figure = None
        self.set_position = (4,4)
        self.set_key_block = False
        self.cond_win = False
        self.winner = None

    def start_game(self, player_name):
        print('WELCOME TO BATTLESHIP')
        input('press any key to begin')

        # player sets ships on the field
        self.player_set(player_name)
        sleep(0.5)
        # computer sets ships on the field
        self.comptr_set()
        # # gameplay
        self.display()
        while not self.cond_win:
            # player's turns
            while True:
                result = self.players_turn()
                if result == 'miss' or self.cond_win:
                    break
            # computer's turns
            while True:
                result = self.comptrs_turn()
                sleep(1)
                if result == 'miss' or self.cond_win:
                    break
        print(f'{self.winner} wins\'s')

    def player_set(self, player_name):
        self.forbiden_zone = set()
        self.player = player_name
        listener = keyboard.Listener(on_press=self.key_press)
        listener.start()
        counter = 0
        while True:
            self.set_interrupt = False
            self.set_position = (4,4)
            if counter < 1:
                self.set_figure = FourDecker()
            elif counter >= 1 and counter < 3:
                self.set_figure = ThreeDecker()
            elif counter >= 3 and counter < 6:
                self.set_figure = TwoDecker()
            elif counter >= 6 and counter < 10:
                self.set_figure = OneDecker()
            else:
                print('player ready!')
                self.set_key_block = True
                break
            counter += 1
            self.display(set_field=True)
            while True:
                if self.set_interrupt:
                    break

    def key_press(self, key):
        if not self.set_key_block:
            if key == keyboard.Key.left:
                self.move_left()
            elif key == keyboard.Key.right:
                self.move_right()
            elif key == keyboard.Key.up:
                self.move_up()
            elif key == keyboard.Key.down:
                self.move_down()
            elif key == keyboard.Key.space:
                self.rotate()
            elif key == keyboard.KeyCode.from_char('s'):
                if self.place():
                    self.set_interrupt = True
            self.display(set_field=True)

    def move_up(self):
        x, y = self.set_position
        new_position = (x-1, y)
        figure_coordinates = self.set_figure.locate(new_position)
        # check border collision
        collide = False
        for (x, y) in figure_coordinates:
            if x < 0:
                collide = True
                break
        if not collide:
            self.set_position = new_position

    def move_down(self):
        x, y = self.set_position
        new_position = (x+1, y)
        figure_coordinates = self.set_figure.locate(new_position)
        # check border collision
        collide = False
        for (x, y) in figure_coordinates:
            if x > 9:
                collide = True
                break
        if not collide:
            self.set_position = new_position

    def move_left(self):
        x, y = self.set_position
        new_position = (x, y-1)
        figure_coordinates = self.set_figure.locate(new_position)
        # check border collision
        collide = False
        for (x, y) in figure_coordinates:
            if y < 0:
                collide = True
                break
        if not collide:
            self.set_position = new_position

    def move_right(self):
        x, y = self.set_position
        new_position = (x, y+1)
        figure_coordinates = self.set_figure.locate(new_position)
        # check border collision
        collide = False
        for (x, y) in figure_coordinates:
            if y > 9:
                collide = True
                break
        if not collide:
            self.set_position = new_position

    def rotate(self):
        self.set_figure.rotate()
        figure_coordinates = self.set_figure.locate(self.set_position)
        # check border collision
        dx = 0
        dy = 0
        for (x, y) in figure_coordinates:
            if x < 0:
                dx = -x
            if x > 9:
                dx = 9-x
            if y < 0:
                dy = -y
            if y > 9:
                dy = 9-y
        x, y = self.set_position
        self.set_position = (x+dx, y+dy)

    def place(self, computer=False):
        # check interferance
        figure_coordinates = self.set_figure.locate(self.set_position)
        for nodes in figure_coordinates:
            if nodes in self.forbiden_zone:
                return False
        for (x,y) in figure_coordinates:
            forbiden_nodes = {(x-1,y-1),(x-1,y),(x-1,y+1),
                              (x,y-1),(x,y),(x,y+1),
                              (x+1,y-1),(x+1,y),(x+1,y+1)}
            self.forbiden_zone = self.forbiden_zone.union(forbiden_nodes)
        if computer==False:
            self.player_ships[self.set_figure.name].append(figure_coordinates)
        else:
            self.comptr_ships[self.set_figure.name].append(figure_coordinates)
        return True

    def comptr_set(self):
        self.forbiden_zone = set()
        counter = 0
        while True:
            if counter < 1:
                self.set_figure = FourDecker()
            elif counter >= 1 and counter < 3:
                self.set_figure = ThreeDecker()
            elif counter >= 3 and counter < 6:
                self.set_figure = TwoDecker()
            elif counter >= 6 and counter < 10:
                self.set_figure = OneDecker()
            else:
                print('computer ready!')
                break
            counter += 1
            self.generate_figure()

    def generate_figure(self):
        while True:
            if random.choice([0,1]) == 1:
                self.set_figure.rotate()
            x = random.choice(list(range(10)))
            y = random.choice(list(range(10)))
            self.set_position = (x,y)
            figure_coordinates = self.set_figure.locate(self.set_position)
            # check border collision
            collide = False
            for (x, y) in figure_coordinates:
                if x > 9 or x < 0 or y > 9 or y < 0:
                    collide = True
            if collide:
                continue
            if self.place(computer=True):
                break

    def display(self, set_field=False):
        player_field = [[0 for i in range(10)] for j in range(10)]
        comptr_field = [[0 for i in range(10)] for j in range(10)]

        for ships in self.player_ships.values():
            for ship in ships:
                for (x, y) in ship:
                    player_field[x][y] = 1
        if set_field == True:
            for (x, y) in self.set_figure.locate(self.set_position):
                player_field[x][y] = 1
            # printing
            r = 1
            print('player'.center(22,'_'))
            print('  A B C D E F G H I J ')
            for row in player_field:
                if r == 10:
                    r = 0
                print(f'{r}|', end='')
                for index, col in enumerate(row):
                    char = '_'
                    print_end = ''
                    if col == 1:
                        char = '#'
                    if index == 9:
                        print_end = '\n'
                    print(f'{char}|', end=print_end)
                r += 1
        else:
            # add misses and hits to plaer's field
            for key, turns in self.comptr_turns.items():
                for (x, y) in turns:
                    player_field[x][y] = 2 if key=='hit' else 3
            # add enemy field
            for key, turns in self.player_turns.items():
                for (x, y) in turns:
                    comptr_field[x][y] = 2 if key=='hit' else 3
            # printing
            r = 1
            print('player'.center(22,'_')+'    '+'computer'.center(22,'_'))
            print('  A B C D E F G H I J '+'    '+'  A B C D E F G H I J ')
            for row in range(10):
                if r == 10:
                    r = 0
                print(f'{r}|', end='')
                for index, col in enumerate(player_field[row]):
                    char = '_'
                    print_end = ''
                    if col == 1:
                        char = '#'
                    elif col == 2:
                        char = 'X'
                    elif col == 3:
                        char = '*'
                    if index == 9:
                        print_end = '    '
                    print(f'{char}|', end=print_end)
                print(f'{r}|', end='')
                for index, col in enumerate(comptr_field[row]):
                    char = '_'
                    print_end = ''
                    if col == 2:
                        char = 'X'
                    elif col == 3:
                        char = '*'
                    if index == 9:
                        print_end = '\n'
                    print(f'{char}|', end=print_end)
                r += 1

    def players_turn(self):
        result = 'miss'
        print(f'{self.player}, now it is your turn. Enter the coordinates!')
        while True:
            coordinates = input('Coordinates (1a - 0j): ')
            if not coordinates or len(coordinates) > 2:
                print('wrong input!, try again')
                continue
            x = coordinates[0]
            y = coordinates[1]
            x_axis = ['1','2','3','4','5','6','7','8','9','0']
            y_axis = ['a','b','c','d','e','f','g','h','i','j']
            if (x not in x_axis) or (y not in y_axis):
                print('wrong input!, try again')
                continue
            true_x = x_axis.index(x)
            true_y = y_axis.index(y)
            shot = (true_x,true_y)
            if shot in self.player_turns['hit'] or shot in self.player_turns['miss']:
                print('can not choose this one!, try again')
                continue
            else:
                break
        key_to_pop = None
        for type, ships in self.comptr_ships.items():
            for ship in ships:
                for node in ship:
                    if shot == node:
                        result = 'hit'
                        ship.remove(node)
                        break
                    else:
                        result = 'miss'
                if not ship:
                    result = 'destroyed'
                    ship_type = type
                    ships.remove(ship)
                if result != 'miss':
                    break
            if not ships:
                key_to_pop = type
            if result != 'miss':
                break
        if key_to_pop:
            self.comptr_ships.pop(key_to_pop)
        if result == 'miss':
            self.player_turns['miss'].append(shot)
            print('you miss! computer\'s turn')
        if result == 'hit':
            self.player_turns['hit'].append(shot)
            print('you hit! it is your turn')
        if result == 'destroyed':
            self.player_turns['hit'].append(shot)
            print(f'{ship_type} destroyed! nice job! it is your turn')
        if not self.comptr_ships:
            self.cond_win = True
            self.winner = self.player
        self.display()
        return result

    def comptrs_turn(self):
        result = 'miss'
        # logic block begin
        if not self.comptr_logic_var['hit']:
            while True:
                x = random.choice(list(range(10)))
                y = random.choice(list(range(10)))
                shot = (x,y)
                if shot not in self.comptr_turns['hit'] and shot not in self.comptr_turns['miss']:
                    break
        else:
            possible_shots = list()
            if len(self.comptr_logic_var['hit']) == 1:
                hit = self.comptr_logic_var['hit'][0]
                x, y = hit
                possible_shots = [(x,y-1),(x+1,y),(x,y+1),(x-1,y)]
            else:
                hits = self.comptr_logic_var['hit']
                orients = None
                x_s = []
                y_s = []
                for hit in hits:
                    x, y = hit
                    x_s.append(x)
                    y_s.append(y)
                if len(set(x_s)) == 1:
                    orients = 'horizontal'
                    x = x_s[0]
                    y1 = min(y_s)
                    y2 = max(y_s)
                    possible_shots = [(x,y1-1),(x,y2+1)]
                elif len(set(y_s)) == 1:
                    orients = 'vertical'
                    y = y_s[0]
                    x1 = min(x_s)
                    x2 = max(x_s)
                    possible_shots = [(x1-1,y),(x2+1,y)]
            while True:
                shot = possible_shots.pop()
                x, y = shot
                if x < 0 or x > 9 or y < 0 or y > 9:
                    continue
                if shot in self.comptr_logic_var['miss']:
                    continue
                else:
                    break
        # logic block end

        x, y = shot
        x_axis = ['1','2','3','4','5','6','7','8','9','0']
        y_axis = ['a','b','c','d','e','f','g','h','i','j']
        choice = f'{x_axis[x]}{y_axis[y]}'
        print(f'computer choose: {choice}')

        key_to_pop = None
        for type, ships in self.player_ships.items():
            for ship in ships:
                for node in ship:
                    if shot == node:
                        result = 'hit'
                        ship.remove(node)
                        break
                    else:
                        result = 'miss'
                if not ship:
                    result = 'destroyed'
                    ship_type = type
                    ships.remove(ship)
                if result != 'miss':
                    break
            if not ships:
                key_to_pop = type
            if result != 'miss':
                break

        if key_to_pop:
            self.player_ships.pop(key_to_pop)
        if result == 'miss':
            self.comptr_turns['miss'].append(shot)
            self.comptr_logic_var['miss'].append(shot)
            print('computer miss! now it is your turn')
        if result == 'hit':
            self.comptr_turns['hit'].append(shot)
            self.comptr_logic_var['hit'].append(shot)
            print('computer hit! computer\'s turn')
        if result == 'destroyed':
            self.comptr_turns['hit'].append(shot)
            self.comptr_logic_var['hit'] = []
            self.comptr_logic_var['miss'] = []
            print(f'{ship_type} destroyed! computer\'s turn')
        if not self.player_ships:
            self.cond_win = True
            self.winner = 'Computer'
        self.display()
        return result
