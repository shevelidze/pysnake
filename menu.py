from mode import Mode
import pygame, sys

class MenuMode(Mode):
    def __init__(self, mode_to_game):
        self.title_font = pygame.font.Font('courier.ttf', 100)
        self.normal_font = pygame.font.Font('courier.ttf', 50)
        self.menu_members = [
            ['start', None, mode_to_game],
            ['exit', None, sys.exit]
        ]

    def __blit_text_hor_center(self, display, font, text, pos_y, color=(0, 0, 0), background=None):
        text_img = font.render(text, True, color, background)
        text_img_rect = text_img.get_rect()
        text_img_rect.centerx = display.get_width() / 2
        text_img_rect.y = pos_y
        display.blit(text_img, text_img_rect)
        return text_img_rect

    def draw_frame(self, display):
        display.fill((255, 255, 255))
        title_pos_y = 100
        self.__blit_text_hor_center(display, self.title_font, 'Pysnake', title_pos_y)
        
        menu_members_pos_y = title_pos_y + self.title_font.get_linesize()

        mouse_pos = pygame.mouse.get_pos()

        for member in self.menu_members:
            color = (0, 0, 0)
            background = (255, 255, 255)
            if (
                mouse_pos[1] > menu_members_pos_y and mouse_pos[1] < menu_members_pos_y + self.normal_font.get_linesize() and
                member[1] and member[1].x < mouse_pos[0] and member[1].x + member[1].width > mouse_pos[0]
            ):  
                color, background = background, color
                if pygame.mouse.get_pressed(3)[0]:
                    member[2]()
            
            member[1] = self.__blit_text_hor_center(display, self.normal_font, member[0], menu_members_pos_y, color, background)

            menu_members_pos_y += self.normal_font.get_linesize()

            