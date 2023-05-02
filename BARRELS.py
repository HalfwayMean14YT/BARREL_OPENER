import pygame
import pygame_gui
import os

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WHITE = (255, 255, 255)
RED = (255, 0, 0)

path = os.path.dirname(os.path.abspath(__file__))

manager = pygame_gui.UIManager((WIDTH, HEIGHT), path + '/themeing.json', True)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Barrel Opener')
    clock = pygame.time.Clock()
    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)
    blackkits = pygame.image.load(path + '/images/blackkits.png')
    barrel = pygame.image.load(path + '/images/barrel.png') 
    barrel = pygame.transform.scale(barrel, (412,412))
    scrap = pygame.image.load(path + '/images/scrap.png')
    scrap = pygame.transform.scale(scrap, (225,225))

    def draw_blackkits():
        screen.blit(blackkits, (0,0))
    
    def draw_barrel():
        screen.blit(barrel, (0,270))
        
    def draw_scrap():
        screen.blit(scrap, (400, 675))

    def draw_scrap_amount(amount):
        background_counter = pygame.image.load(path + '/images/background_counter.png')
        background_counter = pygame.transform.scale(background_counter, (400, 45))
        text_pos_x, text_pos_y, = 451, 15
        font = pygame.font.Font(None,50)
        text = font.render(f'You have {amount} scrap.', True, RED)
        screen.blit(background_counter, (text_pos_x - 50, text_pos_y - 5))
        screen.blit(text, (451, 15))

    scrap_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 675), (255, 255)),
                                            text='',
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(object_id='#scrap_button'))
    scrap_amount = 0
    

    while True:
        time_delta = clock.tick(60)/1000
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == scrap_button:
                    scrap_amount += 1
                    print(f'user now has {scrap_amount} scrap')
                
            manager.process_events(event)
       
        draw_blackkits()
        draw_barrel()
        draw_scrap()
        draw_scrap_amount(str(scrap_amount))
        
        
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()
        
          
if __name__ == "__main__":
    
    main()
    
    