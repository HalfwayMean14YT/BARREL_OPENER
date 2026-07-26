import pygame
import pygame_gui
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 1000
WHITE = (255, 255, 255)
RED = (255, 0, 0)

path = os.path.dirname(os.path.abspath(__file__))

manager = pygame_gui.UIManager((WIDTH, HEIGHT), path + '/themeing.json', True)

def main():
    def read_unlocked():
        unlocked_path = os.path.exists(path + '/user-spec/unlocked')
        if not unlocked_path:
            return False
        try:
            f = open(path + '/user-spec/unlocked')
            content = f.read().strip()
            f.close()
            return content == "1"
        except:
            return False
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    current_screen = "lvl1"
    max_level = 0
    if read_unlocked():
        max_level = 1
    pygame.display.set_caption('Barrel Opener')
    clock = pygame.time.Clock()
    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)
    blackkits = pygame.image.load(path + '/images/blackkits.png')
    barrel = pygame.image.load(path + '/images/barrel.png') 
    barrel = pygame.transform.scale(barrel, (312,312))
    scrap = pygame.image.load(path + '/images/scrap.png')
    scrap = pygame.transform.scale(scrap, (225,225))

                                                                                                   # Load the barrel break sound effect
    barrel_break_sound = pygame.mixer.Sound(path + '/sounds/barrel_break.wav')
    barrel_break_sound.set_volume(0.4)  # tweak to taste
     # Load and start the lobby music
    pygame.mixer.music.load(path + '/sounds/lobby_music.mp3')
    pygame.mixer.music.set_volume(0.5)   # 0.0 = silent, 1.0 = full volume
    pygame.mixer.music.play(-1)          # -1 means loop forever

    def draw_blackkits():
        screen.blit(blackkits, (0,0))
    
    def draw_barrel():
        screen.blit(barrel, (0,520))
        
    def draw_scrap():
        screen.blit(scrap, (400, 675))
    
    def draw_big_scrap():
        screen.blit(pygame.transform.scale(scrap, (240,240)), (390, 667))

    def draw_scrap_amount(amount):
        text_pos_x, text_pos_y, = 451, 15
        font = pygame.font.Font(None,50)
        text = font.render(f'{amount} scrap', True, WHITE)
        screen.blit(text, (420 , 690))

    scrap_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 675), (255, 255)),
                                            text='',
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(object_id='#scrap_button'))
    unlock_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((800, 50), (200, 50)),
                                            text=("Unlock Level 2 (2500 scrap)" if max_level == 0 else "Unlocked!"),
                                            manager=manager)
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((800, 100), (200, 50)),
                                            text='Back',
                                            manager=manager)
    
    def scrap_reader():
        global scrap_amount
        
        scrap_amount_path = os.path.exists(path + '/user-spec/scrap')
        if scrap_amount_path == True:
            print('Loaded scrap file')
        else:
            print('Scrap file not found. Attempting to create it...')
            try:
                dir_to_make = "/user-spec"
                os.mkdir(path + dir_to_make)
                print('Made user-spec folder')
                m = open(path + '/user-spec/scrap', 'x')
                m.close()
                print('Made scrap file')
            except:
                print('There was an error creating the file.')
               
        
        try:
            scrap_amount_file = open(path + '/user-spec/scrap')
            scrap_amount_stat = os.stat(path + '/user-spec/scrap')
            if scrap_amount_stat.st_size == 0:
                f = open(path + '/user-spec/scrap', 'w')
                f.write("0")
                f.close()
            
            scrap_amount_string = scrap_amount_file.read()
            scrap_amount = int(scrap_amount_string)
        finally:
            scrap_amount_file.close()
            
    def write_scrap(scrap_number):
        try:
            scrap_amount_file = open(path + '/user-spec/scrap', 'w')
            scrap_str = str(scrap_number)
            scrap_amount_file.write(scrap_str)
        finally:
            scrap_amount_file.close()
    

    def write_unlocked(is_unlocked):
        try:
            f = open(path + '/user-spec/unlocked', 'w')
            f.write("1" if is_unlocked else "0")
            f.close()
        except:
            print("Error writing to unlocked file.")
        
            
    scrap_reader()
    

    while True:
        global scrap_amount
        time_delta = clock.tick(60)/1000
        screen.fill(WHITE)
        if current_screen == "lvl1":
            draw_blackkits()
            draw_scrap()
            draw_barrel()
            draw_scrap_amount(str(scrap_amount))
        if current_screen == "lvl2":
            screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == scrap_button:
                    barrel_break_sound.play()
                    draw_big_scrap()
                    scrap_amount += 1
                    print(f'user now has {scrap_amount} scrap')
                    write_scrap(scrap_amount)

                if event.ui_element == unlock_button:
                    if max_level == 1:
                        unlock_button.set_text("Unlocked!")
                        current_screen = "lvl2"
                    else: 
                        if scrap_amount >= 2500:
                            scrap_amount -= 2500
                            write_scrap(scrap_amount)
                            current_screen = "lvl2"
                            print('Unlocked lvl2!')
                            write_unlocked(True)
                            max_level = 1
                            unlock_button.set_text("Unlocked!")
                        else:
                            unlock_message = "Not enough scrap!"
                            unlock_message_timer = 120   # roughly 2 seconds at 60 FPS
                if event.ui_element == back_button:
                    current_screen = "lvl1"
                    print('Returned to lvl1')
                    
                
            manager.process_events(event)
       
        
        
        
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()
        
          
if __name__ == "__main__":
    
    main()
    
    