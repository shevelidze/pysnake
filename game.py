from mode import Mode
import pygame
import time
from random import randrange


class GameMode(Mode):
    def __init__(self, mode_to_menu):
        self.snake_move_duration = 1 / 30
        self.section_size = 10
        self.start_snake_length = 20
        self.apples_count = 5
        self.snake_length = self.start_snake_length
        self.score_font = pygame.font.Font('courier.ttf', 25)
        self.__clear_field()
        self.mode_to_menu = mode_to_menu

    def __clear_field(self):
        self.snake_sections = []
        self.apples = []
        self.move_mod = [1, 0]
        self.last_move_time = None

    def __get_sign(self, number):
        if number == 0: return 0
        return number / abs(number)

    def draw_frame(self, display):
        display.fill((255, 255, 255))
        field_hor_space = display.get_width() % self.section_size
        field_width = display.get_width() - field_hor_space
        field_ver_space = display.get_height() % self.section_size
        field_height = display.get_height() - field_hor_space
        field_rect = pygame.Rect(field_hor_space / 2, field_ver_space / 2, field_width, field_height)
        field_cols = display.get_width() // self.section_size
        field_rows = display.get_height() // self.section_size

        if len(self.snake_sections) == 0:
            tail_pos = [field_cols // 2  - self.start_snake_length // 2, field_rows // 2]
            self.snake_sections.append((tail_pos, [tail_pos[0] + self.start_snake_length - 1, tail_pos[1]]))
            self.last_move_time = time.time()

        while len(self.apples) < self.apples_count:
            new_apple = [randrange(0, field_cols), randrange(0, field_rows)]
            while new_apple in self.apples:
                new_apple = [randrange(0, field_cols), randrange(0, field_rows)]
            
            self.apples.append(new_apple)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_w] and self.prev_move_mode != [0, 1]:
            self.move_mod = [0, -1]
        elif keys_pressed[pygame.K_s] and self.prev_move_mode != [0, -1]:
            self.move_mod = [0, 1]
        elif keys_pressed[pygame.K_a] and self.prev_move_mode != [1, 0]:
            self.move_mod = [-1, 0]
        elif keys_pressed[pygame.K_d] and self.prev_move_mode != [-1, 0]:
            self.move_mod = [1, 0]

        if time.time() - self.last_move_time > self.snake_move_duration:
            self.last_move_time = time.time()
            head_section = self.snake_sections[-1]
            self.prev_move_mode = [
                self.__get_sign(head_section[1][0] - head_section[0][0]),
                self.__get_sign(head_section[1][1] - head_section[0][1])
            ]
            if self.prev_move_mode != self.move_mod:
                self.snake_sections.append([head_section[1].copy(), head_section[1].copy()])
                head_section = self.snake_sections[-1]

            head_section[1][0] += self.move_mod[0]
            head_section[1][1] += self.move_mod[1]

            if head_section[1][0] < 0 or head_section[1][0] >= field_cols:
                head_section[1][0] -= self.move_mod[0]
                self.snake_sections.append([[abs(field_cols- abs(head_section[1][0])) -1, head_section[1][1]]] * 2)
                head_section = self.snake_sections[-1]
            elif head_section[1][1] < 0 or head_section[1][1] >= field_rows:
                head_section[1][1] -= self.move_mod[1]
                self.snake_sections.append([[head_section[1][0], abs(field_rows- abs(head_section[1][1])) -1]] * 2)
                head_section = self.snake_sections[-1]

            for snake_section in self.snake_sections[:-2]:
                if (
                    (
                        abs(head_section[1][0] - snake_section[0][0]) + abs(head_section[1][0] - snake_section[1][0]) == abs(snake_section[0][0] - snake_section[1][0]) and
                        head_section[1][1] == snake_section[0][1]
                    ) or
                    (
                        abs(head_section[1][1] - snake_section[0][1]) + abs(head_section[1][1] - snake_section[1][1]) == abs(snake_section[0][1] - snake_section[1][1]) and
                        head_section[1][0] == snake_section[0][0]
                    )
                ):
                    self.mode_to_menu()
                    self.__clear_field()
                    return
        
            if self.snake_sections[-1][1] in self.apples: 
                self.apples.remove(self.snake_sections[-1][1])
                self.snake_length += 1
            else:
                tail_section = self.snake_sections[0]
                tail_section[0][0] += self.__get_sign(tail_section[1][0] - tail_section[0][0])
                tail_section[0][1] += self.__get_sign(tail_section[1][1] - tail_section[0][1])
                if tail_section[0] == tail_section[1]:
                    del self.snake_sections[0]


        for apple in self.apples:
            apple_rect = pygame.Rect(
                field_rect.left + self.section_size * apple[0],
                field_rect.top + self.section_size * apple[1],
                self.section_size, self.section_size
            )
            pygame.draw.rect(display, (255, 0, 0), apple_rect)

        for snake_section in self.snake_sections:
            section_left = min(snake_section[0][0], snake_section[1][0]) * self.section_size
            section_top = min(snake_section[0][1], snake_section[1][1]) * self.section_size
            section_width = max(snake_section[0][0], snake_section[1][0]) - min(snake_section[0][0], snake_section[1][0]) + 1
            section_height = max(snake_section[0][1], snake_section[1][1]) - min(snake_section[0][1], snake_section[1][1]) + 1
            snake_section_rect = pygame.Rect(
                field_rect.left + section_left,
                field_rect.top + section_top,
                section_width * self.section_size,
                section_height * self.section_size,
            )
            pygame.draw.rect(display, (0, 0, 0), snake_section_rect)

        score_surf = self.score_font.render('Score: %i' % (self.snake_length - self.start_snake_length), True, (0, 0, 0))
        display.blit(score_surf, (field_rect.x, field_rect.y))
        
