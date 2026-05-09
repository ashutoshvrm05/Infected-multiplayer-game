import pygame
import sys

import pygame

class Terminal:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        
        self.font = pygame.font.SysFont('couriernew, consolas, monospace', 20, bold=True)
        self.text_color = (0, 255, 65)  
        
        
        self.char_width = self.font.size("A")[0] 
        self.char_height = self.font.size("A")[1]
        
        self.prompt = "> "
        self.input_text = ""
        self.lines = []
        
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
        self.blink_interval = 500 
        
        self.cursor_index = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                self.input_text = self.input_text.strip()
                
                print(f"Command entered: {self.input_text}")
                
                
                if self.input_text:
                    self.lines.append(self.prompt + self.input_text)
                else:
                    self.lines.append(self.prompt)
                    
                if self.input_text == "clear":
                    self.lines.clear()
                    
                self.input_text = "" 
                self.cursor_index = 0  # Reset cursor to start on new line
                
            # --- NEW: Arrow Key Logic ---
            elif event.key == pygame.K_LEFT:
                # Move left, but don't go below 0
                self.cursor_index = max(0, self.cursor_index - 1)
                self.cursor_visible = True
                self.cursor_timer = pygame.time.get_ticks()

            elif event.key == pygame.K_RIGHT:
                # Move right, but don't go past the length of the string
                self.cursor_index = min(len(self.input_text), self.cursor_index + 1)
                self.cursor_visible = True
                self.cursor_timer = pygame.time.get_ticks()
            # -----------------------------
                
            elif event.key == pygame.K_BACKSPACE:
                # Only delete if the cursor is past index 0
                if self.cursor_index > 0:
                    # Slice the string to remove the char just behind the cursor
                    self.input_text = self.input_text[:self.cursor_index - 1] + self.input_text[self.cursor_index:]
                    self.cursor_index -= 1
                
            else:
                if event.unicode.isprintable():
                    # Insert the new letter exactly at the cursor index
                    self.input_text = self.input_text[:self.cursor_index] + event.unicode + self.input_text[self.cursor_index:]
                    self.cursor_index += 1

    def update(self):
        curr_time = pygame.time.get_ticks()
        if curr_time - self.cursor_timer >= self.blink_interval:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = curr_time



    def draw(self, surface, terminal_height):
        
        y = self.y
        line_height = self.char_height
        
        max_lines = (terminal_height // line_height) - 1 
        visible_lines = self.lines[-max_lines:] if len(self.lines) > max_lines else self.lines

        # Draw the past history
        for line in visible_lines:
            # We already attached self.prompt when appending to self.lines
            text_surface = self.font.render(line, True, self.text_color)
            surface.blit(text_surface, (self.x, y))
            y += line_height
        
        # Draw the active input
        full_text = self.prompt + self.input_text[:self.cursor_index] + " " + self.input_text[self.cursor_index+1:]
        text_surface = self.font.render(full_text, True, self.text_color)

        surface.blit(text_surface, (self.x, y))
        
        # --- NEW: Grid-Based Cursor Drawing ---
         # The X position is: Base X + ((Length of prompt + Cursor Index) * Width of one character)
        total_chars_behind_cursor = len(self.prompt) + self.cursor_index
        cursor_x = self.x + (total_chars_behind_cursor * self.char_width)
        cursor_y = self.y + len(visible_lines)*self.char_height

        if self.cursor_visible:
           
            # Use char_width for the width of the rectangle so it perfectly covers one letter space
            cursor_rect = pygame.Rect(cursor_x, cursor_y, self.char_width, self.char_height)
            
            # Optional: If you want an underline cursor instead of a block, change char_height to 2 
            # and change cursor_y to (y + self.char_height - 2)
            pygame.draw.rect(surface, self.text_color, cursor_rect)

            if(len(self.input_text)>self.cursor_index):
                char_under_cursor = self.input_text[self.cursor_index]
                s = self.font.render(char_under_cursor, True, (0,0,0))
                surface.blit(s, (cursor_x, y))
        
        else:
            if(len(self.input_text)>self.cursor_index):
                char_under_cursor = self.input_text[self.cursor_index]
                s = self.font.render(char_under_cursor, True, self.text_color)
                surface.blit(s, (cursor_x, y))


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

        terminal.draw(screen, HEIGHT-4*border_padding)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()