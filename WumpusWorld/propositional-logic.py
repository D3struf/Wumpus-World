import random
import numpy as np

worldMatrix = np.zeros((4, 4), dtype=int)

def setMobs(worldMatrix):
    worldMatrix[3][0] = 1  # Initial position of the character
    
    # Restricted positions
    restricted_positions = [(3, 0), (2, 0), (3, 1)]

    # Loop for each mobs
    for mob_type in [(-200, 'wumpus'), (-50, 'pit'), (-50, 'pit'), (100, 'gold'), (10, 'dagger')]:
        mob_value, mob_name = mob_type
        x, y = 3, 0
        
        # Find a valid position that is not restricted
        while (x, y) in restricted_positions or worldMatrix[x][y] != 0:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
        
        # Set the mob at the valid position
        worldMatrix[x][y] = mob_value
        print(f"{mob_name} placed at position ({x}, {y})")

    print(worldMatrix)

setMobs(worldMatrix)

# Constants
S = 0
B = 1
P = 2
W = 3
V = 4
G = 5

class Agent:
    def __init__(self, worldMatrix):
        self.world = worldMatrix
        self.char_pos = (3, 0)
        self.path = []
        self.knowledge = np.zeros((self.world.shape[0], self.world.shape[1], 6), dtype=object)
        self.temp_world = self.duplicateWorld()
        self.armed = False
        self.is_wumpus = False
        
        for i in range(self.knowledge.shape[0]):
            for j in range(self.knowledge.shape[1]):
                for k in range(self.knowledge.shape[2]):
                    self.knowledge[i][j][k] = ''
    
    def print_knowledge(self):
        for i in range(self.knowledge.shape[0]):
            for j in range(self.knowledge.shape[1]):
                print(f"({i}, {j}): ", end=" ")
                for k in range(self.knowledge.shape[2]):
                    print(f"{self.knowledge[i][j][k]}, ", end=" ")
                print()
    
    def get_loc(self):
        return self.char_pos

    def perceives(self):
        pos = self.get_loc()
        if pos[0] >= 0 and pos[0] < self.temp_world.shape[0] and pos[1] >= 0 and pos[1] < self.temp_world.shape[1]:
            # Check if the position is within the bounds of temp_world
            senses = self.temp_world[pos[0], pos[1]].split(',')
        else:
            senses = []  # Return empty list if the position is out of bounds
        return senses

    def adjacent_positions(self):
        rows, cols = self.world.shape[0], self.world.shape[1]
        # print("World size: ", rows, ",", cols)
        
        adj_locs = []
        for row in [self.char_pos[0] - 1, self.char_pos[0] + 1]:
            if row >= 0 and row < rows:
                adj_locs.append((row, self.char_pos[1]))
                # print(row, self.char_pos[1])
        for col in [self.char_pos[1] - 1, self.char_pos[1] + 1]:
            if col >= 0 and col < cols:
                adj_locs.append((self.char_pos[0], col))
                # print(self.char_pos[0], col)
        return adj_locs

    def learn(self):
        pos_actuators = self.perceives()
        # print(pos_actuators)
        
        self.knowledge[self.char_pos[0], self.char_pos[1]][S] = ("S" if "S" in pos_actuators else "~S")
        self.knowledge[self.char_pos[0], self.char_pos[1]][B] = ("B" if "B" in pos_actuators else "~B")
        self.knowledge[self.char_pos[0], self.char_pos[1]][P] = ("P" if "P" in pos_actuators else "~P")
        self.knowledge[self.char_pos[0], self.char_pos[1]][W] = ("W" if "W" in pos_actuators else "~W")
        self.knowledge[self.char_pos[0], self.char_pos[1]][V] = "V"
        self.knowledge[self.char_pos[0], self.char_pos[1]][G] = ("G" if "G" in pos_actuators else "~G")
        # print(self.knowledge[self.char_pos[0], self.char_pos[1]])

        # Check for Wumpus and Pits
        for locations in self.adjacent_positions():
            if 'S' in pos_actuators:
                # Check if the adjacent positions has W?
                if 'W?' in self.knowledge[locations][W]:
                    if 'V' not in self.knowledge[locations][V]:
                        self.knowledge[locations][W] = 'W'
                        self.is_wumpus = True
                # chances of Wumpus in the adjacent positions
                elif '~W' not in self.knowledge[locations][W]: 
                    # If it has, set the knowledge of adjacent positions [W] to W?
                    self.knowledge[locations][W] = "W?"
            else:
                # If not, set the knowledge of adjacent positions [W] to ~W
                self.knowledge[locations][W] = "~W"
                # print(locations, self.knowledge[locations])
                # print("theres a wumpus adjacent to this position")
            if 'B' in pos_actuators:
                # Check if the adjacent positions has P? 
                if 'P?' in self.knowledge[locations][P]:
                    if 'V' not in self.knowledge[locations][V]:
                        self.knowledge[locations][P] = 'P'
                # chances of Pit in the adjacent positions
                elif '~P' not in self.knowledge[locations][P]: 
                    # If it has, set the knowledge of adjacent positions [P] to P?
                    self.knowledge[locations][P] = "P?"
            else:
                # If not, set the knowledge of adjacent positions [P] to ~P
                self.knowledge[locations][P] = "~P"
                # print(locations, self.knowledge[locations])
                # print("theres a pit adjacent to this position")

    def move(self, next_move):
        self.char_pos = next_move

    def get_path_gold(self):
        path = []
        
        while True:
            current_pos = self.get_loc()
            print("Current position: ", current_pos)
            
            self.learn()
            self.print_knowledge()
            
            elements = self.perceives()
            print("Elements ", elements)
            if 'G' in elements:
                path.append(current_pos)
                reverse_path = path[::-1]
                return path + reverse_path[1:]

            path.append(current_pos)
            next_xy = None
            
            for location in self.adjacent_positions():
                print('Locations: ', location)
                if 'W?' != self.knowledge[location][W] and 'P?' != self.knowledge[location][P] and 'V' not in self.knowledge[location][V]:
                    next_xy = [location[0], location[1]]
                    break 
            
            print('Next: ', next_xy)
            if next_xy is not None:
                self.move(next_xy)
            else:
                if len(path) > 1:
                    path.pop()
                    prev_pos = path.pop()
                    self.move(prev_pos)
                else:
                    break
    
    def get_path_kill(self):
        path = []
        
        while True:
            current_pos = self.get_loc()
            print("Current position: ", current_pos)
            
            self.learn()
            self.print_knowledge()
            elements = self.perceives()
            
            if 'D' in elements:
                self.armed = True
                
            path.append(current_pos)
            next_xy = None
            
            for location in self.adjacent_positions():
                print('Locations: ', location)
                if self.is_wumpus:
                    if self.armed:
                        path.append(location)
                        return path
                if 'W?' != self.knowledge[location][W] and 'P?' != self.knowledge[location][P] and 'V' != self.knowledge[location][V]:
                    next_xy = [location[0], location[1]]
                    break
            
            print('Wumpus ', self.is_wumpus)
            
            print('Next: ', next_xy)
            if next_xy is not None:
                self.move(next_xy)
            else:
                if len(path) > 1:
                    path.pop()
                    prev_pos = path.pop()
                    self.move(prev_pos)

    # To create a basis for the agent to learn
    def duplicateWorld(self):
        matrixwithsenses = np.empty((4, 4), dtype=object)
        matrixwithsenses.fill('')
        
        def setSensors(temp_world, x, y, sensor):
            if sensor == 'S':
                if x + 1 < 4:
                    temp_world[x + 1][y] += ',S' if temp_world[x + 1][y] else 'S'
                if x - 1 >= 0:
                    temp_world[x - 1][y] += ',S' if temp_world[x - 1][y] else 'S'
                if y + 1 < 4:
                    temp_world[x][y + 1] += ',S' if temp_world[x][y + 1] else 'S'
                if y - 1 >= 0:
                    temp_world[x][y - 1] += ',S' if temp_world[x][y - 1] else 'S'
            else:
                if x + 1 < 4:
                    temp_world[x + 1][y] += ',B' if temp_world[x + 1][y] else 'B'
                if x - 1 >= 0:
                    temp_world[x - 1][y] += ',B' if temp_world[x - 1][y] else 'B'
                if y + 1 < 4:
                    temp_world[x][y + 1] += ',B' if temp_world[x][y + 1] else 'B'
                if y - 1 >= 0:
                    temp_world[x][y - 1] += ',B' if temp_world[x][y - 1] else 'B'
        
        # Change from numeric to char
        for x in range(4):
            for y in range(4):
                if self.world[x][y] == -200:
                    matrixwithsenses[x][y] = 'W'
                elif self.world[x][y] == -50:
                    matrixwithsenses[x][y] = 'P'
                elif self.world[x][y] == 100:
                    matrixwithsenses[x][y] = 'G'
                elif self.world[x][y] == 10:
                    matrixwithsenses[x][y] = 'D'
        
        # Create stench and breeze
        for x in range(4):
            for y in range(4):
                if 'W' in matrixwithsenses[x][y]:
                    setSensors(matrixwithsenses, x, y, 'S')
                elif 'P' in matrixwithsenses[x][y]:
                    setSensors(matrixwithsenses, x, y, 'B')
        
        print(matrixwithsenses)
        return matrixwithsenses

worldwithsenses = Agent(worldMatrix)
# worldwithsenses.duplicateWorld()
# worldwithsenses.print_knowledge()

# worldwithsenses.learn()
path = worldwithsenses.get_path_kill()
print(path)
# lists = worldwithsenses.perceives()
# print(lists)