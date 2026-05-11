import pygame
import sys
from vfs import VirtualFileSystem  

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
        
        self.vfs = VirtualFileSystem()
        self.prompt = ""
        self.update_prompt() 
        self.input_text = ""
        self.lines = []

        self.history = []
        self.history_index = 0
        
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
        self.blink_interval = 500 
        
        self.cursor_index = 0
    
    def update_prompt(self):
        self.prompt = f"admin@{self.vfs.get_path()}> "

    def execute_command(self, command_string):
        if not command_string:
            return

        parts = command_string.split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        if cmd == "clear":
            self.lines.clear()
            print(self.cmds)
            
        elif cmd == "ls":
            items = self.vfs.ls()
            if items:
                msg = ""
                c = 1
                for item in items:
                    if c%2==0:
                        msg += item
                        c += 1
                        self.lines.append(msg)
                        msg = ""
                    else:
                        msg += item
                        msg += (15-len(item))*" "
                        c += 1
                if c%2 == 0:
                    self.lines.append(msg)
                
        elif cmd == "cd":
            if not args:
                return 
            
            target = args[0]
            error = self.vfs.cd(target)
            
            if error:
                self.lines.append(error)
            else:
                self.update_prompt()
                
        else:
            self.lines.append(f"Command not found: {cmd}")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                self.input_text = self.input_text.strip()
                
                if self.input_text:
                    self.history.append(self.input_text)
                    self.history_index = len(self.history)

                    self.lines.append(self.prompt + self.input_text)
                    self.execute_command(self.input_text)
                else:
                    self.lines.append(self.prompt)
                    
                self.input_text = "" 
                self.cursor_index = 0
                
            elif event.key == pygame.K_LEFT:
                self.cursor_index = max(0, self.cursor_index - 1)
                self.cursor_visible = True
                self.cursor_timer = pygame.time.get_ticks()

            elif event.key == pygame.K_RIGHT:
                self.cursor_index = min(len(self.input_text), self.cursor_index + 1)
                self.cursor_visible = True
                self.cursor_timer = pygame.time.get_ticks()
                
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_index > 0:
                    self.input_text = self.input_text[:self.cursor_index - 1] + self.input_text[self.cursor_index:]
                    self.cursor_index -= 1

            elif event.key == pygame.K_UP:
                if self.history and self.history_index > 0:
                    self.history_index -= 1
                    self.input_text = self.history[self.history_index]
                    self.cursor_index = len(self.input_text) 
                    
                    self.cursor_visible = True
                    self.cursor_timer = pygame.time.get_ticks()

            elif event.key == pygame.K_DOWN:
                if self.history:
                    if self.history_index < len(self.history) - 1:
                        self.history_index += 1
                        self.input_text = self.history[self.history_index]
                        self.cursor_index = len(self.input_text)
                    elif self.history_index == len(self.history) - 1:
                        self.history_index += 1
                        self.input_text = ""
                        self.cursor_index = 0

                    self.cursor_visible = True
                    self.cursor_timer = pygame.time.get_ticks()
                
            else:
                if event.unicode.isprintable():
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

        for line in visible_lines:
            text_surface = self.font.render(line, True, self.text_color)
            surface.blit(text_surface, (self.x, y))
            y += line_height
        
        full_text = self.prompt + self.input_text[:self.cursor_index] + " " + self.input_text[self.cursor_index+1:]
        text_surface = self.font.render(full_text, True, self.text_color)

        surface.blit(text_surface, (self.x, y))
        
        total_chars_behind_cursor = len(self.prompt) + self.cursor_index
        cursor_x = self.x + (total_chars_behind_cursor * self.char_width)
        cursor_y = self.y + len(visible_lines)*self.char_height

        if self.cursor_visible:
           
            cursor_rect = pygame.Rect(cursor_x, cursor_y, self.char_width, self.char_height)
            
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