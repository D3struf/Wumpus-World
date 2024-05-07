import pygame

class Button:
    def __init__(self, image_path, text, text_size, bg_color, font_color, hovered_size, image_size, position):
        self.image_path = image_path
        self.text = text
        self.bg_color = bg_color
        self.font_color = font_color
        self.outline_color = (0, 0, 0)
        self.position = position
        self.hovered_size = hovered_size
        self.image_size = image_size
        self.is_hovered = False
        if self.image_path is None:
            self.font = pygame.font.Font("./assets/fonts/Noot Regular.ttf", text_size)
            self.image = self.text
            self.text_surface = self.font.render(self.text, True, self.font_color)
            self.text_rect = self.text_surface.get_rect(center=self.position)
            self.rect = self.text_rect
        else:
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.rect = self.image.get_rect(center=self.position)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def run(self, screen):
        self.update()
        if self.image_path is None:
            if self.is_hovered:
                scaled_rect = self.rect.inflate(15, 15)
                pygame.draw.rect(screen, self.bg_color, scaled_rect, 0)
                pygame.draw.rect(screen, self.outline_color, scaled_rect, 5)
            else:
                pygame.draw.rect(screen, self.bg_color, self.rect, 0)
                pygame.draw.rect(screen, self.outline_color, self.rect, 5)
            if hasattr(self, 'text_surface'):
                screen.blit(self.text_surface, self.text_rect)
        else:
            if self.is_hovered:
                self.image = pygame.transform.scale(self.image, self.hovered_size)
            else:
                self.image = pygame.transform.scale(self.image, self.image_size)
            screen.blit(self.image, self.rect)
    
    