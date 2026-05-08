import pygame
import sys

class Terminal:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        
        self.font = pygame.font.SysFont('couriernew', 20, bold=True)
        self.text_color = (0, 255, 65)  
        
        self.prompt = "> "
        self.input_text = ""
        self.lines = []
        
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
        self.blink_interval = 500 

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(f"Command entered: {self.input_text}")
                self.lines.append(self.input_text)
                self.input_text = "" 
                
            elif event.key == pygame.K_BACKSPACE:

                self.input_text = self.input_text[:-1]
                
            else:

                if event.unicode.isprintable():
                    self.input_text += event.unicode

    def update(self):

        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_timer >= self.blink_interval:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time

    def draw(self, surface):
        
        y = self.y
        for line in self.lines:
            full_text = self.prompt + line
            text_surface = self.font.render(full_text, True, self.text_color)
            surface.blit(text_surface, (self.x, y))
            y+=self.font.get_height()
        full_text = self.prompt + self.input_text
        text_surface = self.font.render(full_text, True, self.text_color)
        surface.blit(text_surface, (self.x, y))
        

        if self.cursor_visible:

            text_width = text_surface.get_width()
            cursor_x = self.x + text_width + 2 
            cursor_y = y
            

            cursor_rect = pygame.Rect(cursor_x, cursor_y, 10, self.font.get_height())
            pygame.draw.rect(surface, self.text_color, cursor_rect)



def main():
    pygame.init()
    

    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Infected")
    clock = pygame.time.Clock()
    

    bg_color = (13, 2, 8)     
    border_color = (0, 255, 65) 
    

    border_padding = 20

    terminal = Terminal(x=border_padding + 10, y=border_padding + 10, width=WIDTH - (border_padding*2))
    
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            

            terminal.handle_event(event)

        terminal.update()

        screen.fill(bg_color)

        pygame.draw.rect(screen, border_color, 
                         pygame.Rect(border_padding, border_padding, 
                                     WIDTH - (2*border_padding), HEIGHT - (2*border_padding)), 
                         width=2) 

        terminal.draw(screen)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()