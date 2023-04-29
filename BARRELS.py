import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WHITE = (255, 255, 255)

path = os.path.dirname(os.path.abspath(__file__))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Barrel Opener')
    clock = pygame.time.Clock()
    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)
    blackkits = pygame.image.load(path + '/images/blackkits.png')
    barrel = pygame.image.load(path + '/images/barrel.png') 
    barrel = pygame.transform.scale(barrel, (412,412))

    def draw_blackkits():
        screen.blit(blackkits, (0,0))
    
    def draw_barrel():
        screen.blit(barrel, (0,270))

    while True:
        clock.tick(30)
        screen.fill(WHITE)
       
        draw_blackkits()
        draw_barrel()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
        
          
if __name__ == "__main__":
    
    main()
    
    