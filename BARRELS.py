import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WHITE = (255, 255, 255)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Barrel Opener')
    clock = pygame.time.Clock()
    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)
    blackkits = pygame.image.load('blackkits.png')
    

    

    
    
    
    def draw_blackkits():
        screen.blit(blackkits, (0,0))


    while True:
        clock.tick(30)
        screen.fill(WHITE)
       

        draw_blackkits()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
        
        

    
      
if __name__ == "__main__":
    
    main()
    
    