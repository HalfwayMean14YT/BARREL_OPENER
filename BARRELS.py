import pygame
import pygame_gui
import os
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 1000
WHITE = (255, 255, 255)
RED = (255, 0, 0)

path = os.path.dirname(os.path.abspath(__file__))

manager = pygame_gui.UIManager((WIDTH, HEIGHT), path + '/themeing.json', True)

def main():
    global scrap_amount
    global current_screen
    global unlock_message
    global unlock_message_timer
    global screen2_unlocked
    global active_skins

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Barrel Opener')
    clock = pygame.time.Clock()
    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)
    blackkits = pygame.image.load(path + '/images/blackkits.png')
    barrel = pygame.image.load(path + '/images/barrel.png')
    barrel = pygame.transform.scale(barrel, (312, 312))
    scrap = pygame.image.load(path + '/images/scrap.png')
    scrap = pygame.transform.scale(scrap, (225, 225))

    barrel_break_sound = pygame.mixer.Sound(path + '/sounds/barrel_break.mp3')
    barrel_break_sound.set_volume(0.4)

    pygame.mixer.music.load(path + '/sounds/lobby_music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    SKINS = [
        {"name": "Cloth", "image": "cloth.png", "price": 3, "weight": 100},
    ]

    for skin in SKINS:
        img = pygame.image.load(path + '/images/skins/' + skin["image"])
        img = pygame.transform.scale(img, (150, 150))
        skin["surface"] = img

    def pick_random_skin():
        weights = [skin["weight"] for skin in SKINS]
        chosen = random.choices(SKINS, weights=weights, k=1)
        return chosen[0]

    def draw_blackkits():
        screen.blit(blackkits, (0, 0))

    def draw_barrel():
        screen.blit(barrel, (0, 520))

    def draw_scrap():
        screen.blit(scrap, (400, 675))

    def draw_big_scrap():
        screen.blit(pygame.transform.scale(scrap, (240, 240)), (390, 667))

    def draw_scrap_amount(amount):
        font = pygame.font.Font(None, 50)
        text = font.render(f'{amount} scrap', True, RED)
        screen.blit(text, (451, 15))

    scrap_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 675), (255, 255)),
                                            text='',
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(object_id='#scrap_button'))

    barrel_rect = pygame.Rect(0, 520, 312, 312)

    unlock_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (200, 50)),
                                            text='Unlock (2500 scrap)',
                                            manager=manager)

    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (150, 50)),
                                            text='Back',
                                            manager=manager)

    def scrap_reader():
        global scrap_amount
        scrap_amount_path = os.path.exists(path + '/user-spec/scrap')
        if scrap_amount_path:
            print('Loaded scrap file')
        else:
            print('Scrap file not found. Attempting to create it...')
            try:
                os.mkdir(path + "/user-spec")
                print('Made user-spec folder')
            except FileExistsError:
                pass
            except Exception as e:
                print(f'Error creating user-spec folder: {e}')
            try:
                open(path + '/user-spec/scrap', 'x').close()
                print('Made scrap file')
            except Exception as e:
                print(f'Error creating scrap file: {e}')

        scrap_amount_file = None
        try:
            scrap_amount_stat = os.stat(path + '/user-spec/scrap')
            if scrap_amount_stat.st_size == 0:
                with open(path + '/user-spec/scrap', 'w') as f:
                    f.write("0")

            scrap_amount_file = open(path + '/user-spec/scrap')
            scrap_amount = int(scrap_amount_file.read())
        finally:
            if scrap_amount_file:
                scrap_amount_file.close()

    def write_scrap(scrap_number):
        try:
            scrap_amount_file = open(path + '/user-spec/scrap', 'w')
            scrap_amount_file.write(str(scrap_number))
        finally:
            scrap_amount_file.close()

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

    def write_unlocked(is_unlocked):
        try:
            f = open(path + '/user-spec/unlocked', 'w')
            f.write("1" if is_unlocked else "0")
            f.close()
        except:
            print('There was an error saving unlocked status.')

    scrap_reader()

    current_screen = "main"
    unlock_message = ""
    unlock_message_timer = 0
    screen2_unlocked = read_unlocked()

    active_skins = []

    if screen2_unlocked:
        unlock_button.set_text('Enter Lvl 2 (Unlocked)')

    while True:
        time_delta = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "main" and barrel_rect.collidepoint(event.pos):
                    if scrap_amount >= 50:
                        scrap_amount -= 50
                        write_scrap(scrap_amount)
                        barrel_break_sound.play()
                        new_skin = pick_random_skin()
                        active_skins.append({"skin": new_skin, "alpha": 255, "delay": 90})
                        print(f'You got: {new_skin["name"]} (worth {new_skin["price"]} scrap)!')
                    else:
                        unlock_message = "Not enough scrap!"
                        unlock_message_timer = 120

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == scrap_button:
                    draw_big_scrap()
                    scrap_amount += 1
                    print(f'user now has {scrap_amount} scrap')
                    write_scrap(scrap_amount)

                if event.ui_element == unlock_button:
                    if screen2_unlocked:
                        current_screen = "screen2"
                    elif scrap_amount >= 2500:
                        scrap_amount -= 2500
                        write_scrap(scrap_amount)
                        screen2_unlocked = True
                        write_unlocked(True)
                        unlock_button.set_text('Enter Lvl 2 (Unlocked)')
                        current_screen = "screen2"
                        print('Unlocked screen 2!')
                    else:
                        unlock_message = "Not enough scrap!"
                        unlock_message_timer = 120

                if event.ui_element == back_button:
                    current_screen = "main"

            manager.process_events(event)

        if current_screen == "main":
            screen.fill(WHITE)
            draw_blackkits()
            draw_scrap()
            unlock_button.show()
            back_button.hide()
        elif current_screen == "screen2":
            screen.fill((0, 0, 0))
            unlock_button.hide()
            back_button.show()

        if unlock_message_timer > 0:
            unlock_message_timer -= 1
            if current_screen == "main":
                message_font = pygame.font.Font(None, 40)
                message_text = message_font.render(unlock_message, True, RED)
                screen.blit(message_text, (50, 110))
        else:
            unlock_message = ""

        if current_screen == "main":
            draw_barrel()
            draw_scrap_amount(str(scrap_amount))

            still_active = []
            for entry in active_skins:
                if entry["delay"] > 0:
                    entry["delay"] -= 1
                else:
                    entry["alpha"] -= 3
                    if entry["alpha"] < 0:
                        entry["alpha"] = 0

                skin = entry["skin"]
                skin_surface = skin["surface"].copy()
                skin_surface.set_alpha(entry["alpha"])
                skin_rect = skin_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(skin_surface, skin_rect)

                price_font = pygame.font.Font(None, 30)
                price_text = price_font.render(f'Worth: {skin["price"]} scrap', True, WHITE)
                price_text.set_alpha(entry["alpha"])
                price_rect = price_text.get_rect(center=(WIDTH // 2, skin_rect.bottom + 0))
                screen.blit(price_text, price_rect)

                if entry["alpha"] <= 0:
                    scrap_amount += skin["price"]
                    write_scrap(scrap_amount)
                    print(f'{skin["name"]} turned back into {skin["price"]} scrap!')
                else:
                    still_active.append(entry)

            active_skins = still_active

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()