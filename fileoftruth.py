import pygame

pygame.init()

WIDTH, HEIGHT = 500, 500
WHITE = (255, 255, 255)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Barrel Opener')
    clock = pygame.time.Clock()
    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)
    amongusdot = pygame.image.load('amongusdot.png')

    def draw_amongusdot():
        screen.blit(amongusdot, (250,250))




    while True:
        clock.tick(30)
        screen.fill(WHITE)
        draw_amongusdot()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()

if __name__ == "__main__":
    main()
    
    