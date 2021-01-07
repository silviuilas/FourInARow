import pygame


class slider:
    def render(self):
        bigfont = pygame.font.SysFont('monospace', 60)
        self.nr_text_render = bigfont.render(str(self.nr), True, (255, 255, 255))
        self.nr_text_size = bigfont.size(str(self.nr))
        pygame.draw.rect(self.screen, (255, 255, 255), self.button_left)
        pygame.draw.rect(self.screen, (255, 255, 255), self.button_right)
        aux = self.font.size(self.text)

        self.screen.blit(self.text_render, (self.x + 50 + (75 - aux[0] / 2), self.y))
        self.screen.blit(self.nr_text_render, (
            (self.x + 50) + (self.text_size[0] / 2 - self.nr_text_size[0] / 2), self.y + self.text_size[1]))

    def __init__(self, screen, text, font, x, y, nr, min, max):
        self.screen = screen
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.text_render = font.render(text, True, (255, 255, 255))
        aux = font.size(text)
        self.text_size = (150, aux[1])
        self.nr = nr
        self.min = min
        self.max = max
        bigfont = pygame.font.SysFont('monospace', 60)

        self.button_left = pygame.Rect(x, y, 50, 100)
        self.button_right = pygame.Rect(x + 50 + self.text_size[0], y, 50, 100)

        self.render()

    def check_collide(self, coords):
        if self.button_left.collidepoint(coords):
            return 1
        if self.button_right.collidepoint(coords):
            return 2
        return 0

    def press_button(self, coords):
        if self.check_collide(coords) == 1:
            if self.nr > self.min:
                self.nr -= 1
                self.render()
        elif self.check_collide(coords) == 2:
            if self.nr < self.max:
                self.nr += 1
                self.render()
        else:
            return


def main_menu():
    pygame.init()
    res = (720, 720)
    screen = pygame.display.set_mode(res)
    color = (255, 255, 255)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    width = screen.get_width()
    height = screen.get_height()

    smallfont = pygame.font.SysFont('Corbel', 35)

    text_rows = smallfont.render('Rows', True, color)
    text_columns = smallfont.render('Columns', True, color)

    rows_slider = slider(screen, "Rows", smallfont, width / 2 - 124, 75, 5, 3, 10)
    columns_slider = slider(screen, "Columns", smallfont, width / 2 - 124, 200, 7, 5, 10)
    players_slider = slider(screen, "Players", smallfont, width / 2 - 124, 325, 2, 1, 4)
    start = False
    next = False
    while not start:
        screen.fill((140, 235, 52))
        click = False
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    click = True
        mouse = pygame.mouse.get_pos()
        if not next:
            columns_slider.render()
            rows_slider.render()
            players_slider.render()

            next_button = pygame.Rect(width / 2 - 75, 450, 150, 75)
            pygame.draw.rect(screen, (255, 255, 255), next_button)
            text_render = smallfont.render("Next", True, (0, 0, 0))
            screen.blit(text_render, (width / 2 - 75 + 40, 470))

            if click == True:
                columns_slider.press_button(mouse)
                rows_slider.press_button(mouse)
                players_slider.press_button(mouse)
                if next_button.collidepoint(mouse):
                    next = True
                    ai_slider = slider(screen, "AI", smallfont, width / 2 - 124, 200, 0, 0, players_slider.nr)
            # updates the frames of the game
        else:
            ai_slider.render()
            prev_button = pygame.Rect(width / 2 - 75, 325, 150, 75)
            pygame.draw.rect(screen, (255, 255, 255), prev_button)
            text_render = smallfont.render("Prev", True, (0, 0, 0))
            screen.blit(text_render, (width / 2 - 75 + 40, 345))

            start_button = pygame.Rect(width / 2 - 75, 450, 150, 75)
            pygame.draw.rect(screen, (255, 255, 255), start_button)
            text_render = smallfont.render("Start", True, (0, 0, 0))
            screen.blit(text_render, (width / 2 - 75 + 40, 470))
            if click == True:
                ai_slider.press_button(mouse)
                if prev_button.collidepoint(mouse):
                    next = False
                if start_button.collidepoint(mouse):
                    start = True


        pygame.display.update()

    return (rows_slider.nr, columns_slider.nr, players_slider.nr, ai_slider.nr)
