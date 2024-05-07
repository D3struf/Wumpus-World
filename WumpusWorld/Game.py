import pygame, sys, threading

from .States import Start, Instruction1, Instruction2, Play, Mode
from .GameStateManager import GameStateManager

# Variables
SCREENWIDTH, SCREENHEIGHT = 1024, 768
FPS = 60

class Game:
    def __init__(self, caption, icon_path):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("./assets/fonts/Noot Regular.ttf", 100)
        pygame.display.set_caption(caption)
        pygame.display.set_icon(pygame.image.load(icon_path).convert_alpha())
        
        self.gameStateManager = GameStateManager('start')
        self.start = Start(screen=self.screen, gameStateManager=self.gameStateManager, title="WUMPUS WORLD", title_size=72, title_font=self.font, background_path="./assets/Wumpus World.gif", position=(512, 200))
        self.instruction1 = Instruction1(screen=self.screen, gameStateManager=self.gameStateManager, background_path="./assets/Instruction1.gif")
        self.instruction2 = Instruction2(screen=self.screen, gameStateManager=self.gameStateManager, background_path="./assets/Instruction2.gif")
        self.chooseMode = Mode(screen=self.screen, gameStateManager=self.gameStateManager, background_path="./assets/Wumpus World.gif", text='CHOOSE MODE', text_font=self.font, text_size=72, position=(512, 200))
        self.play = Play(screen=self.screen, gameStateManager=self.gameStateManager, text_size=24)
        
        self.states = {
            'start': self.start,
            'instruction1': self.instruction1,
            'instruction2': self.instruction2,
            'mode': self.chooseMode,
            'play': self.play
        }

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.states[self.gameStateManager.get_state()].run()
            
            self.clock.tick(FPS)