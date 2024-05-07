import gif_pygame, pygame, sys, webbrowser, random
import numpy as np

from .Button import Button
from .Agent import Agent

# Global
playerMode = False

class Start:
    def __init__(self, screen, gameStateManager, title, title_size, title_font, background_path, position):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.background = gif_pygame.load(background_path)
        self.title = title_font.render(title, True, title_size)
        self.title_rect = self.title.get_rect(center=position)
        
        self.start_btn = Button(image_path=None, text="     START     ", text_size=42, bg_color="#292A2F", font_color="#A0E524", position=(512, 420), hovered_size=(0, 0), image_size=(0, 0))
        self.instruction_btn = Button(image_path=None, text=" INSTRUCTION ", text_size=36, bg_color="#292A2F", font_color="#24E5CA", position=(512, 500), hovered_size=(0, 0), image_size=(0, 0))
        self.quit_btn = Button(image_path=None, text="      QUIT      ", text_size=42, bg_color="#292A2F", font_color="#FF3131", position=(512, 580), hovered_size=(0, 0), image_size=(0, 0))
        
    def run(self):
        self.background.render(self.screen, (512-self.background.get_width()*0.5, 384-self.background.get_height()*0.5))
        self.screen.blit(self.title, self.title_rect)
        
        self.start_btn.run(self.screen)
        self.instruction_btn.run(self.screen)
        self.quit_btn.run(self.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_btn.is_hovered:
                    self.gameStateManager.set_state('mode')
                if self.instruction_btn.is_hovered:
                    self.gameStateManager.set_state('instruction1')
                if self.quit_btn.is_hovered:
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()

class Instruction1:
    def __init__(self, screen, gameStateManager, background_path):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.instruction = gif_pygame.load(background_path)
        
        self.next_btn = Button(image_path=None, text="  NEXT  ", text_size=42, bg_color="#292A2F", font_color="#A0E524", position=(512, 691), hovered_size=(0, 0), image_size=(0, 0))
        self.exit_btn = Button(image_path="./assets/icons8-cancel-48 (1).png", text=None, text_size=None, bg_color=None, font_color=None, position=(910, 114), hovered_size=(56, 56), image_size=(48, 48))

    def run(self):
        self.instruction.render(self.screen, (512-self.instruction.get_width()*0.5, 384-self.instruction.get_height()*0.5))
        
        self.next_btn.run(self.screen)
        self.exit_btn.run(self.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.next_btn.is_hovered:
                    self.gameStateManager.set_state('instruction2')
                if self.exit_btn.is_hovered:
                    self.gameStateManager.set_state('start')
        
        pygame.display.update()

class Instruction2:
    def __init__(self, screen, gameStateManager, background_path):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.instruction = gif_pygame.load(background_path)
        
        self.back_btn = Button(image_path=None, text="  BACK  ", text_size=42, bg_color="#292A2F", font_color="#FF3131", position=(512, 691), hovered_size=(0, 0), image_size=(0, 0))
        
        self.exit_btn = Button(image_path="./assets/icons8-cancel-48 (1).png", text=None, text_size=None, bg_color=None, font_color=None, position=(910, 114), hovered_size=(56, 56), image_size=(48, 48))
        
    def run(self):
        self.instruction.render(self.screen, (512-self.instruction.get_width()*0.5, 384-self.instruction.get_height()*0.5))

        self.back_btn.run(self.screen)
        self.exit_btn.run(self.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_btn.is_hovered:
                    self.gameStateManager.set_state('instruction1')
                if self.exit_btn.is_hovered:
                    self.gameStateManager.set_state('start')
                    
        pygame.display.update()

class Play:
    def __init__(self, screen, gameStateManager, text_size):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.text_size = text_size
        self.font = pygame.font.Font("./assets/fonts/Noot Regular.ttf", self.text_size)
        self.cell_size = 190
        # Player Movement
        self.char_x_coords = 0
        self.char_y_coords = 570
        self.char_x = 0
        self.char_y = 3
        self.faceDirection = 'front'
        self.visited = [(3, 0), (2, 0), (3, 1)]
        # Define boundaries
        self.boundary_left = 0
        self.boundary_right = 760
        self.boundary_upper = 0
        self.boundary_lower = 760
        # Dagger
        self.dagger_speed = 100
        self.dagger_x = 0
        self.dagger_y = 190
        # State
        self.died_wumpus = False
        self.died_pit = False
        self.died = False
        self.armed = False
        self.treasure = False
        self.win = False
        # Agent
        self.agent = False
        path = True
        while path:
            self.worldMatrix = np.zeros((4, 4), dtype=int)
            self.setMobs()
            self.path_by_gold = Agent(self.worldMatrix).get_path_directions()
            if self.path_by_gold is not None:
                path = False

    def play_music(self, music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
    
    def set_font(self, font_size):
        self.text_size = font_size
        self.font = pygame.font.Font("./assets/fonts/Noot Regular.ttf", font_size)
    
    def reset(self):
        # Player Movement
        self.char_x_coords = 0
        self.char_y_coords = 570
        self.char_x = 0
        self.char_y = 3
        self.faceDirection = 'front'
        self.visited = [(3, 0), (2, 0), (3, 1)]
        # Define boundaries
        self.boundary_left = 0
        self.boundary_right = 760
        self.boundary_upper = 0
        self.boundary_lower = 760
        # State
        self.died_wumpus = False
        self.died_pit = False
        self.died = False
        self.armed = False
        self.treasure = False
        self.win = False
        # Agent
        self.agent = False
        path = True
        while path:
            self.worldMatrix = np.zeros((4, 4), dtype=int)
            self.setMobs()
            self.path_by_gold = Agent(self.worldMatrix).get_path_directions()
            if self.path_by_gold is not None:
                path = False

    def load_images(self):
        self.cell_image = pygame.image.load("./assets/wall.png").convert_alpha()
        self.wall_cover_image = pygame.image.load("./assets/wall_cover.png").convert_alpha()
        self.wumpus_alive_image = pygame.image.load("./assets/Wumpus-Alive.png").convert_alpha()
        self.wumpus_dead_image = pygame.image.load("./assets/Wumpus-Dead.png").convert_alpha()
        self.pit_image = pygame.image.load("./assets/Pit.png").convert_alpha()
        self.gold_image = pygame.image.load("./assets/Gold.png").convert_alpha()
        self.Dagger_image = pygame.image.load("./assets/Dagger.png").convert_alpha()
        self.Dagger_gif = gif_pygame.load("./assets/Dagger-twirl.gif")
        self.char_back_image =  pygame.image.load("./assets/Char-Back.png").convert_alpha()
        self.char_front_image = pygame.image.load("./assets/Char-Front.png").convert_alpha()
        self.char_left_image = pygame.image.load("./assets/Char-Left.png").convert_alpha()
        self.char_right_image = pygame.image.load("./assets/Char-Right.png").convert_alpha()
        self.roar = pygame.mixer.Sound("./assets/sounds/roar.wav")
        self.falling = pygame.mixer.Sound("./assets/sounds/falling.mp3")
        self.slain = pygame.mixer.Sound("./assets/sounds/hero-hurt.mp3")

    def render_display(self):
        self.load_images()
        self.render_panel()
        
        # Render the grid with images
        for row in range(4):
            for col in range(4):
                x = col * self.cell_size
                y = row * self.cell_size
                self.screen.blit(self.cell_image, (x, y))
        
        self.spawn_mobs()
        self.change_char()
        pygame.draw.rect(self.screen, "#292A2F", (0, 760, 1024, 8))
        
        self.cell_cover()
        
        if self.died:
            self.agent = False
            pygame.draw.rect(self.screen, "#FF3131", (0, 0, 760, 768))
            self.set_font(font_size=100)
            game_over = self.font.render("Game Over", True, "#000000")
            game_over_rect = game_over.get_rect(center=(380, 384))
            self.screen.blit(game_over, game_over_rect)
            if self.died_pit:
                self.set_font(font_size=30)
                killedbypit = self.font.render("You fell in the Pit of Darkness.", True, "#000000")
                killedbypit_rect = killedbypit.get_rect(center=(380, 450))
                self.screen.blit(killedbypit, killedbypit_rect)
            if self.died_wumpus:
                self.set_font(font_size=30)
                killedbywumpus = self.font.render("You have been Slain by Wumpus.", True, "#000000")
                killedbywumpus_rect = killedbywumpus.get_rect(center=(380, 450))
                self.screen.blit(killedbywumpus, killedbywumpus_rect)
        if self.win:
            self.agent = False
            pygame.draw.rect(self.screen, "#A0E524", (0, 0, 760, 768))
            # self.confetti = gif_pygame.load("./assets/confetti.gif")
            # self.confetti.render(self.screen, (380-self.confetti.get_width()*0.5, 384-self.confetti.get_height()*0.5))
            self.set_font(font_size=100)
            win = self.font.render("Congratulations", True, "#000000")
            win_rect = win.get_rect(center=(380, 384))
            self.screen.blit(win, win_rect)

    def run(self):
        global playerMode
        self.render_display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_btn.is_hovered:
                    if playerMode:
                        self.reset()
                    else:
                        self.agent = True
                if self.back_btn.is_hovered:
                    self.gameStateManager.set_state('start')
                    self.reset()
                if self.github_btn.is_hovered:
                    webbrowser.open("https://github.com/D3struf")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset()
                    # If Player Moves
                if playerMode:
                    if event.key == pygame.K_LEFT:
                        if self.char_x_coords > self.boundary_left and self.faceDirection == 'left':
                            # If already double-clicked, move left
                            self.char_x_coords -= self.cell_size
                            self.char_x -= 1
                            self.check_state()
                        self.faceDirection = 'left'
                    if event.key == pygame.K_RIGHT:
                        if self.char_x_coords < self.boundary_right - self.cell_size and self.faceDirection == 'right':
                            self.char_x_coords += self.cell_size
                            self.char_x += 1
                            self.check_state()
                        self.faceDirection = 'right'
                    if event.key == pygame.K_UP:
                        if self.char_y_coords > self.boundary_upper and self.faceDirection == 'up':
                            self.char_y_coords -= self.cell_size
                            self.char_y -= 1
                            self.check_state()
                        self.faceDirection = 'up'
                    if event.key == pygame.K_DOWN:
                        if self.char_y_coords < self.boundary_lower - self.cell_size and self.faceDirection == 'front':
                            self.char_y_coords += self.cell_size
                            self.char_y += 1
                            self.check_state()
                        self.faceDirection = 'front'
                    if event.key == pygame.K_RETURN:
                            if self.armed:
                                self.play_music("./assets/sounds/dagger-throw.mp3")
                                self.throw_dagger()

        # If Start Button is Pressed Agent will start
        if self.agent:
            if len(self.path_by_gold) > 0:
                move = self.path_by_gold.pop(0)  # Get the next move from the list
                if move == 'left':
                    if self.faceDirection != 'left':
                        self.faceDirection = 'left'
                        self.change_char()
                    if self.char_x_coords > self.boundary_left and self.faceDirection == 'left':
                        self.char_x_coords -= self.cell_size
                        self.char_x -= 1
                        self.check_state()
                    self.faceDirection = 'left'
                elif move == 'right':
                    if self.faceDirection != 'right':
                        self.faceDirection = 'right'
                        self.change_char()
                    if self.char_x_coords < self.boundary_right - self.cell_size and self.faceDirection == 'right':
                        self.char_x_coords += self.cell_size
                        self.char_x += 1
                        self.check_state()
                    self.faceDirection = 'right'
                elif move == 'up':
                    if self.faceDirection != 'up':
                        self.faceDirection = 'up'
                        self.change_char()
                    if self.char_y_coords > self.boundary_upper and self.faceDirection == 'up':
                        self.char_y_coords -= self.cell_size
                        self.char_y -= 1
                        self.check_state()
                    self.faceDirection = 'up'
                elif move == 'front':
                    if self.faceDirection != 'front':
                        self.faceDirection = 'front'
                        self.change_char()
                    if self.char_y_coords < self.boundary_lower - self.cell_size and self.faceDirection == 'front':
                        self.char_y_coords += self.cell_size
                        self.char_y += 1
                        self.check_state()
                    self.faceDirection = 'front'
                elif move == 'shoot':
                    self.armed = True
                    if self.armed:
                        self.play_music("./assets/sounds/dagger-throw.mp3")
                        self.throw_dagger()
                pygame.time.delay(100)
        
        pygame.display.update()

    def check_state(self):
        state = self.worldMatrix[self.char_y][self.char_x]
        if state == -50: 
            self.died = True
            self.died_pit = True
            self.falling.play()
            # print("game over caused by pit")
        elif state == -200: 
            self.died = True
            self.died_wumpus = True
            self.slain.play()
            # print("game over caused by wumpus")
        elif state == 10: 
            self.armed = True
            self.play_music("./assets/sounds/draw-sword.mp3")
            # print("gained dagger")
            self.worldMatrix[self.char_y][self.char_x] = 0
        elif state == 100:
            self.treasure = True
            self.play_music("./assets/sounds/gold-glitter.wav")
            self.worldMatrix[self.char_y][self.char_x] = 0
            # print("gained treasure")
        
        if self.treasure and state == 1:
            self.win = True
            self.play_music("./assets/sounds/win.wav")
            # print("win")

    def render_panel(self):
        pygame.draw.rect(self.screen, "#292A2F", (760, 0, 264, 768))
        
        # Load Components
        self.set_font(font_size=24)
        if playerMode:
            self.start_btn = Button(image_path=None, text="  RESTART  ", text_size=42, bg_color="#292A2F", font_color="#A0E524", position=(890, 400), hovered_size=(0, 0), image_size=(0, 0))
        else:
            self.start_btn = Button(image_path=None, text="  START  ", text_size=42, bg_color="#292A2F", font_color="#A0E524", position=(890, 400), hovered_size=(0, 0), image_size=(0, 0))
        self.back_btn = Button(image_path=None,  text="   BACK   ", text_size=42, bg_color="#292A2F", font_color="#FF3131", position=(890, 500), hovered_size=(0, 0), image_size=(0, 0))
        self.github_btn = Button(image_path="./assets/icons8-github-64.png",  text=None, text_size=None, bg_color=None, font_color=None, position=(800, 710), hovered_size=(56, 56), image_size=(48, 48))
        text_surface = self.font.render("@John Paul Monter", True, "#ffffff")
        text_rect = text_surface.get_rect(center=(920, 710))
        
        self.set_font(font_size=36)
        if self.treasure:
            tresure_obtain = self.font.render("Treasure", True, "#A0E524")
            tresure_obtain_rect = tresure_obtain.get_rect(topleft=(780, 150))
        else: 
            tresure_obtain = self.font.render("Treasure", True, "#FF3131")
            tresure_obtain_rect = tresure_obtain.get_rect(topleft=(780, 150))
        if self.win and not self.died_wumpus:
            wumpus_killed = self.font.render("Killed Wumpus", True, "#A0E524")
            wumpus_killed_rect = wumpus_killed.get_rect(topleft=(780, 200))
        else:
            wumpus_killed = self.font.render("Killed Wumpus", True, "#FF3131")
            wumpus_killed_rect = wumpus_killed.get_rect(topleft=(780, 200))
        if self.armed:
            dagger_obtain = self.font.render("Dagger", True, "#A0E524")
            dagger_obtain_rect = dagger_obtain.get_rect(topleft=(780, 250))
        else: 
            dagger_obtain = self.font.render("Dagger", True, "#FF3131")
            dagger_obtain_rect = dagger_obtain.get_rect(topleft=(780, 250))
        
        # Display
        self.start_btn.run(self.screen)
        self.back_btn.run(self.screen)
        self.github_btn.run(self.screen)
        self.screen.blit(text_surface, text_rect)
        self.screen.blit(tresure_obtain, tresure_obtain_rect)
        self.screen.blit(wumpus_killed, wumpus_killed_rect)
        self.screen.blit(dagger_obtain, dagger_obtain_rect)

    def cell_cover(self):        
        if (self.char_y, self.char_x) not in self.visited:
            self.visited.append((self.char_y, self.char_x))
        
        # Render the grid with images
        for row in range(4):
            for col in range(4):
                x = col * self.cell_size
                y = row * self.cell_size
                if (row, col) not in self.visited:
                    self.screen.blit(self.wall_cover_image, (x, y))

    def change_char(self):
        if self.faceDirection == 'front':
            self.screen.blit(self.char_front_image, (self.char_x_coords, self.char_y_coords))
        elif self.faceDirection == 'left':
            self.screen.blit(self.char_left_image, (self.char_x_coords, self.char_y_coords))
        elif self.faceDirection == 'right':
            self.screen.blit(self.char_right_image, (self.char_x_coords, self.char_y_coords))
        elif self.faceDirection == 'up':
            self.screen.blit(self.char_back_image, (self.char_x_coords, self.char_y_coords))
    
    def setMobs(self):
        self.worldMatrix[3][0] = 1  # Initial position of the character
        
        # Restricted positions
        restricted_positions = [(3, 0), (2, 0), (3, 1)]
        
        # Loop for each mob type
        mob_types = [(100, 'dagger'), (-200, 'wumpus'), (-50, 'pit'), (-50, 'pit'), (10, 'dagger')]
        for mob_value, mob_name in mob_types:
            x, y = 3, 0
            
            # Find a valid position that is not restricted
            while (x, y) in restricted_positions or self.worldMatrix[x][y] != 0:
                x = random.randint(0, 3)
                y = random.randint(0, 3)
            
            # Set the mob at the valid position
            self.worldMatrix[x][y] = mob_value
            # print(f"{mob_name} placed at position ({x}, {y})")
            
        # print(self.worldMatrix)

    def spawn_mobs(self):
        self.set_font(font_size=32)
        breeze = self.font.render("BREEZE", True, "#38b6ff")
        stench = self.font.render("STENCH", True, "#993b00")
        
        # Display
        for row in range(4):
            for col in range(4):
                x = col * self.cell_size
                y = row * self.cell_size
                if self.worldMatrix[row][col] == 100 and self.treasure == False:
                    self.screen.blit(self.gold_image, (x, y))
                elif self.worldMatrix[row][col] == 10 and self.armed == False:
                    self.screen.blit(self.Dagger_image, (x + 50, y - 50))
                elif self.worldMatrix[row][col] == -200:
                    if self.win: self.screen.blit(self.wumpus_dead_image, (x, y))
                    else: self.screen.blit(self.wumpus_alive_image, (x, y))
                elif self.worldMatrix[row][col] == -50:
                    self.screen.blit(self.pit_image, (x, y))

                # Display stench
                if self.worldMatrix[row][col] == -200:
                    if row > 0 and (self.worldMatrix[row - 1][col] == 0 or self.worldMatrix[row - 1][col] == 10):
                        self.screen.blit(stench, (x, y - self.cell_size // 2))
                    if row < 3 and (self.worldMatrix[row + 1][col] == 0 or self.worldMatrix[row + 1][col] == 10):
                        self.screen.blit(stench, (x, y + self.cell_size + 85))
                    if col > 0 and (self.worldMatrix[row][col - 1] == 0 or self.worldMatrix[row][col - 1] == 10):
                        self.screen.blit(stench, (x - self.cell_size, y + 100))
                    if col < 3 and (self.worldMatrix[row][col + 1] == 0 or self.worldMatrix[row][col + 1] == 10):
                        self.screen.blit(stench, (x + self.cell_size, y + 100))
                
                # Display breeze
                if self.worldMatrix[row][col] == -50:
                    if row > 0 and (self.worldMatrix[row - 1][col] == 0 or self.worldMatrix[row - 1][col] == 10):
                        self.screen.blit(breeze, (x, y - self.cell_size))
                    if row < 3 and (self.worldMatrix[row + 1][col] == 0 or self.worldMatrix[row + 1][col] == 10):
                        self.screen.blit(breeze, (x, y + self.cell_size))
                    if col > 0 and (self.worldMatrix[row][col - 1] == 0 or self.worldMatrix[row][col - 1] == 10):
                        self.screen.blit(breeze, (x - self.cell_size, y))
                    if col < 3 and (self.worldMatrix[row][col + 1] == 0 or self.worldMatrix[row][col + 1] == 10):
                        self.screen.blit(breeze, (x + self.cell_size, y))

    def throw_dagger(self):
        self.dagger_x = self.char_x_coords
        self.dagger_y = self.char_y_coords
        
        while True:
            if self.faceDirection == 'right':
                self.dagger_x += self.dagger_speed
                self.screen.blit(self.Dagger_image, (self.dagger_x, self.dagger_y))
                if self.dagger_x >= self.boundary_right - (self.cell_size // 2) - 100:
                    break
                for i in range(self.char_x, 4):
                    # print(i, "|", self.char_y, ": ", self.worldMatrix[self.char_y][i])
                    if self.worldMatrix[self.char_y][i] == -200:
                        self.win = True
                        # print('killed')
            elif self.faceDirection == 'left':
                self.dagger_x -= self.dagger_speed
                self.screen.blit(self.Dagger_image, (self.dagger_x, self.dagger_y))
                if self.dagger_x <= self.boundary_left:
                    break
                for i in range(self.char_x, -1, -1):
                    if self.worldMatrix[self.char_y][i] == -200:
                        self.win = True
                        # print('killed')
            elif self.faceDirection == 'up':
                self.dagger_y -= self.dagger_speed
                self.screen.blit(self.Dagger_image, (self.dagger_x, self.dagger_y))
                if self.dagger_y <= self.boundary_upper:
                    break
                for i in range(self.char_y, -1, -1):
                    if self.worldMatrix[i][self.char_x] == -200:
                        self.win = True
                        # print('killed')
            elif self.faceDirection == 'front':
                self.dagger_y += self.dagger_speed
                self.screen.blit(self.Dagger_image, (self.dagger_x, self.dagger_y))
                if self.dagger_y >= self.boundary_lower:
                    break
                for i in range(self.char_y, 4):
                    if self.worldMatrix[i][self.char_x] == -200:
                        self.win = True
                        # print('killed')
        
        self.armed = False

        if self.win:
            self.roar.play()

class Mode:
    def __init__(self, screen, gameStateManager, background_path, text, text_font, text_size, position):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.background = gif_pygame.load(background_path)
        self.text_input = text_font.render(text, True, text_size)
        self.text_rect = self.text_input.get_rect(center=position)
        
        self.set_font(font_size=15)
        self.ai_btn = Button(image_path='./assets/Agent.png', text=None, text_size=42, bg_color="#292A2F", font_color="#A0E524", position=(341, 384), hovered_size=(250, 250), image_size=(190, 190))
        self.ai_text = text_font.render('Agent', True, "#A0E524")
        self.ai_rect = self.ai_text.get_rect(center=(341, 580))
        self.player_btn = Button(image_path='./assets/Icon.png', text=None, text_size=42, bg_color="#292A2F", font_color="#A0E524", position=(682, 384),hovered_size=(250, 250), image_size=(190, 190))
        self.player_text = text_font.render('Player', True, "#A0E524")
        self.player_rect = self.player_text.get_rect(center=(682, 580))
    
    def set_font(self, font_size):
        self.text_size = font_size
        self.font = pygame.font.Font("./assets/fonts/Noot Regular.ttf", font_size)
    
    def run(self):
        global playerMode
        self.background.render(self.screen, (512-self.background.get_width()*0.5, 384-self.background.get_height()*0.5))
        self.screen.blit(self.text_input, self.text_rect)
        
        self.ai_btn.run(self.screen)
        self.screen.blit(self.ai_text, self.ai_rect)
        self.player_btn.run(self.screen)
        self.screen.blit(self.player_text, self.player_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ai_btn.is_hovered:
                    playerMode = False
                    self.gameStateManager.set_state('play')
                if self.player_btn.is_hovered:
                    playerMode = True
                    self.gameStateManager.set_state('play')
        
        pygame.display.update()

