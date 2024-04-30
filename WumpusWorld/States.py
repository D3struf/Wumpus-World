import gif_pygame, pygame, sys, webbrowser, random
import numpy as np

from .Button import Button 

class Start:
    def __init__(self, screen, gameStateManager, title, title_size, title_font, background_path, position):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.background = gif_pygame.load(background_path)
        self.title = title_font.render(title, True, title_size)
        self.title_rect = self.title.get_rect(center=position)
        
        self.start_btn = Button(image_path=None, text="     START     ", text_size=42, bg_color="#292A2F", font_color="#A0E524", position=(512, 420))
        self.instruction_btn = Button(image_path=None, text=" INSTRUCTION ", text_size=36, bg_color="#292A2F", font_color="#24E5CA", position=(512, 500))
        self.quit_btn = Button(image_path=None, text="      QUIT      ", text_size=42, bg_color="#292A2F", font_color="#FF3131", position=(512, 580))
        
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
                    self.gameStateManager.set_state('play')
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
        
        self.next_btn = Button(image_path=None, text="  NEXT  ", text_size=42, bg_color="#292A2F", font_color="#A0E524", position=(512, 691))
        self.exit_btn = Button(image_path="./assets/icons8-cancel-48 (1).png", text=None, text_size=None, bg_color=None, font_color=None, position=(910, 114))

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
        
        self.back_btn = Button(image_path=None, text="  BACK  ", text_size=42, bg_color="#292A2F", font_color="#FF3131", position=(512, 691))
        
        self.exit_btn = Button(image_path="./assets/icons8-cancel-48 (1).png", text=None, text_size=None, bg_color=None, font_color=None, position=(910, 114))
        
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
    def __init__(self, screen, gameStateManager, cell_image_path, text_size):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.font = pygame.font.Font("./assets/fonts/Noot Regular.ttf", text_size)
        self.cell_image_path = cell_image_path
        self.cell_size = 190
        self.cell_image = pygame.image.load(self.cell_image_path).convert_alpha()
        self.worldMatrix = np.zeros((4, 4), dtype=int)
        self.setMobs()
        # Player Movement
        self.char_x_coords = 0
        self.char_y_coords = 570
        self.char_x = 0
        self.char_y = 3
        self.faceDirection = 'front'
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
        self.died = False
        self.armed = False
        self.treasure = False
        self.wumpusKilled = False

    def reset(self):
        self.worldMatrix = np.zeros((4, 4), dtype=int)
        self.setMobs()
        # Player Movement
        self.char_x_coords = 0
        self.char_y_coords = 570
        self.char_x = 0
        self.char_y = 3
        self.faceDirection = 'front'
        # Define boundaries
        self.boundary_left = 0
        self.boundary_right = 760
        self.boundary_upper = 0
        self.boundary_lower = 760
        # State
        self.died = False
        self.armed = False
        self.treasure = False
        self.wumpusKilled = False

    def load_images(self):
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

    def render_display(self):
        self.load_images()
        self.render_panel()
        
        # Render the grid with images
        for row in range(4):
            for col in range(4):
                x = col * self.cell_size
                y = row * self.cell_size
                self.screen.blit(self.cell_image, (x, y))
        
        self.change_char()
        self.spawn_mobs()

    def run(self):
        self.render_display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_btn.is_hovered:
                    pass
                if self.back_btn.is_hovered:
                    self.gameStateManager.set_state('start')
                    self.reset()
                if self.github_btn.is_hovered:
                    webbrowser.open("https://github.com/D3struf")
            if event.type == pygame.KEYDOWN:
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
                
                if event.key == pygame.K_SPACE:
                    self.reset()
                if event.key == pygame.K_RETURN:
                    if self.armed:
                        self.throw_dagger()
        
        pygame.display.update()

    def check_state(self):
        state = self.worldMatrix[self.char_y][self.char_x]
        if state == -50: 
            self.died = True
            print("game over caused by pit")
        elif state == -200: 
            self.died = True
            print("game over caused by wumpus")
        elif state == 10: 
            self.armed = True
            print("gained dagger")
            self.worldMatrix[self.char_y][self.char_x] = 0
        elif state == 100:
            self.treasure = True
            self.worldMatrix[self.char_y][self.char_x] = 0
            print("gained treasure")
        
        if self.treasure and state == 1:
            print("win")

    def render_panel(self):
        pygame.draw.rect(self.screen, "#292A2F", (760, 0, 264, 768))
        
        # Load Components
        self.start_btn = Button(image_path=None, text="   START   ", text_size=42, bg_color="#292A2F", font_color="#A0E524", position=(890, 400))
        self.back_btn = Button(image_path=None,  text="   BACK   ", text_size=42, bg_color="#292A2F", font_color="#FF3131", position=(890, 500))
        self.github_btn = Button(image_path="./assets/icons8-github-64.png",  text=None, text_size=None, bg_color=None, font_color=None, position=(800, 710))
        self.text_surface = self.font.render("@John Paul Monter", True, "#ffffff")
        self.text_rect = self.text_surface.get_rect(center=(920, 710))
        
        # Display
        self.start_btn.run(self.screen)
        self.back_btn.run(self.screen)
        self.github_btn.run(self.screen)
        self.screen.blit(self.text_surface, self.text_rect)

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

        # Loop for each mobs
        for mob_type in [(-200, 'wumpus'), (-50, 'pit'), (-50, 'pit'), (100, 'gold'), (10, 'dagger')]:
            mob_value, mob_name = mob_type
            x, y = 3, 0
            
            # Find a valid position that is not restricted
            while (x, y) in restricted_positions or self.worldMatrix[x][y] != 0:
                x = random.randint(0, 3)
                y = random.randint(0, 3)
            
            # Set the mob at the valid position
            self.worldMatrix[x][y] = mob_value
            print(f"{mob_name} placed at position ({x}, {y})")

        print(self.worldMatrix)

    def spawn_mobs(self):
        # Display
        for row in range(4):
            for col in range(4):
                x = col * self.cell_size
                y = row * self.cell_size
                if self.worldMatrix[row][col] == -200:
                    if self.wumpusKilled: self.screen.blit(self.wumpus_dead_image, (x, y))
                    else: self.screen.blit(self.wumpus_alive_image, (x, y))
                elif self.worldMatrix[row][col] == -50:
                    self.screen.blit(self.pit_image, (x, y))
                elif self.worldMatrix[row][col] == 100 and self.treasure == False:
                    self.screen.blit(self.gold_image, (x, y))
                elif self.worldMatrix[row][col] == 10 and self.armed == False:
                    self.screen.blit(self.Dagger_image, (x, y))

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
                    print(i, "|", self.char_y, ": ", self.worldMatrix[self.char_y][i])
                    if self.worldMatrix[self.char_y][i] == -200:
                        self.wumpusKilled = True
                        print('killed')
            elif self.faceDirection == 'left':
                self.dagger_x -= self.dagger_speed
                self.screen.blit(self.Dagger_image, (self.dagger_x, self.dagger_y))
                if self.dagger_x <= self.boundary_left:
                    break
                for i in range(self.char_x, -1, -1):
                    if self.worldMatrix[self.char_y][i] == -200:
                        self.wumpusKilled = True
                        print('killed')
            elif self.faceDirection == 'up':
                self.dagger_y -= self.dagger_speed
                self.screen.blit(self.Dagger_image, (self.dagger_x, self.dagger_y))
                if self.dagger_y <= self.boundary_upper:
                    break
                for i in range(self.char_y, -1, -1):
                    if self.worldMatrix[i][self.char_x] == -200:
                        self.wumpusKilled = True
                        print('killed')
            elif self.faceDirection == 'front':
                self.dagger_y += self.dagger_speed
                self.screen.blit(self.Dagger_image, (self.dagger_x, self.dagger_y))
                if self.dagger_y >= self.boundary_lower:
                    break
                for i in range(self.char_y, 4):
                    if self.worldMatrix[i][self.char_x] == -200:
                        self.wumpusKilled = True
                        print('killed')
        
        self.armed = False