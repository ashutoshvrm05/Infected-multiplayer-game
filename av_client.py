import pygame
import sys
import random
from core.vfs import VirtualFileSystem

class SystemMonitor:
    def __init__(self, x, y, width, height):
        # coordinates of the System Minitor screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # font and text
        self.color = (0, 255, 65)
        self.bg_color = (10, 5, 15)
        self.font = pygame.font.SysFont('couriernew, consolas, monospace', 14, bold=True)
        self.title_font = pygame.font.SysFont('couriernew, consolas, monospace', 16, bold=True)
        
        # CPU
        self.cpu_history = [0.0] * 40
        self.cpu_target = 10.0
        self.cpu_current = 10.0
        
        # RAM
        self.ram_usage = 35.0 
        
        # Syslog Data
        self.logs = [
            "SYSTEM BOOT SUCCESS",
            "VFS MOUNTED AT /",
            "AWAITING CONNECTIONS...",
            "WARNING: FIREWALL OFFLINE"
        ]

    def add_log(self, message):
        self.logs.append(message)
        if len(self.logs) > 12:
            self.logs.pop(0)

    def update(self, curr_tick):
        # Fake CPU for testing
        if random.random() < 0.05:
            self.cpu_target = random.uniform(5, 85)
            
        self.cpu_current += (self.cpu_target - self.cpu_current) * 0.1
        self.cpu_history.append(self.cpu_current)
        self.cpu_history.pop(0)

    def draw(self, surface):
        # Layout metrics
        graph_h = int(self.height * 0.30)
        ram_h = int(self.height * 0.15)
        padding = 15
        
        # CPU SPARKLINE GRAPH 
        cpu_y = self.y
        pygame.draw.rect(surface, self.color, (self.x, cpu_y, self.width, graph_h), 5)
        
        title = self.title_font.render(f"CPU LOAD: {int(self.cpu_current)}%", True, self.color)
        surface.blit(title, (self.x + 5, cpu_y + 5))
        
        # solid area Sparkline
        bar_width = (self.width - 4) / len(self.cpu_history)
        for i, val in enumerate(self.cpu_history):
            bar_h = (val / 100.0) * (graph_h - 30) 
            bx = self.x + 2 + (i * bar_width)
            by = cpu_y + graph_h - bar_h - 2 
            pygame.draw.rect(surface, self.color, (bx, by, bar_width + 1, bar_h))

        # RAM PROGRESS BAR 
        ram_y = cpu_y + graph_h + padding
        pygame.draw.rect(surface, self.color, (self.x, ram_y, self.width, ram_h), 2)
        
        ram_title = self.title_font.render(f"RAM ALLOC: {int(self.ram_usage)}%", True, self.color)
        surface.blit(ram_title, (self.x + 5, ram_y + 5))
        
        # Chunky background bar
        bar_x = self.x + 10
        bar_y = ram_y + 35
        max_bar_w = self.width - 20
        pygame.draw.rect(surface, (50, 35, 0), (bar_x, bar_y, max_bar_w, 20)) 
        
        # Solid filled foreground bar
        inner_w = (self.ram_usage / 100.0) * max_bar_w
        pygame.draw.rect(surface, self.color, (bar_x, bar_y, inner_w, 20))

        # SYSLOG SECTION 
        syslog_y = ram_y + ram_h + padding
        syslog_h = self.height - (syslog_y - self.y)
        pygame.draw.rect(surface, self.color, (self.x, syslog_y, self.width, syslog_h), 2)
        
        log_title = self.title_font.render("--- SYSTEM LOG ---", True, self.bg_color, self.color)
        surface.blit(log_title, (self.x, syslog_y))
        
        text_y = syslog_y + 25
        for log in self.logs:
            log_surf = self.font.render(f"> {log}", True, self.color)
            surface.blit(log_surf, (self.x + 5, text_y))
            text_y += self.font.get_height() + 4

class Terminal:
    def __init__(self, x, y, width, monitor=None):
        # coordinates of the terminal screen
        self.x = x
        self.y = y
        self.width = width
        self.monitor = monitor 
        
        # font and text
        self.font = pygame.font.SysFont('couriernew, consolas, monospace', 20, bold=True)
        self.text_color = (0, 255, 65) 
        
        # size of a letter in px
        self.char_width = self.font.size("A")[0] 
        self.char_height = self.font.size("A")[1]
        
        # prompt is default text, input text is what the user inputs, lines is everything that is to be displayed
        self.vfs = VirtualFileSystem()
        self.prompt = ""
        self.update_prompt() 
        self.input_text = ""
        self.lines = []

        # history is the record of all input text
        self.history = []
        self.history_index = 0
        
        # cursor, cursor index is the number of letters before it
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
        self.blink_interval = 500 
        self.cursor_index = 0
    
    def update_prompt(self):
        self.prompt = f"admin@{self.vfs.get_path()}> "

    # runs when the user hits enter after some input text
    def execute_command(self, command_string):
        if not command_string:
            return

        parts = command_string.split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        if cmd == "clear":
            self.lines.clear()
            
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

    # handle all key press
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

    # updating blink of cursor
    def update(self):
        curr_time = pygame.time.get_ticks()
        if curr_time - self.cursor_timer >= self.blink_interval:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = curr_time

    # draw everything 
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
    
    # Widen the screen to 1000px to fit both UI elements comfortably
    WIDTH, HEIGHT = 1200, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Antivirus Command Center")
    clock = pygame.time.Clock()
    
    bg_color = (10, 5, 15)
    border_color = (0, 255, 65)
    border_padding = 20

    #  Monitor on the Left (Width: 320)
    monitor = SystemMonitor(x=border_padding, y=border_padding, width=320, height=HEIGHT - (border_padding*2))
    
    # Terminal on the Right
    term_x = border_padding + 320 + border_padding
    term_width = WIDTH - term_x - border_padding
    terminal = Terminal(x=term_x + 10, y=border_padding + 10, width=term_width - 20, monitor=monitor)

    # CRT Effect Scanlines 
    scanline_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    scanline_color = (0, 0, 0, 80) 
    for y in range(0, HEIGHT, 2): 
        pygame.draw.line(scanline_overlay, scanline_color, (0, y), (WIDTH, y), 1)

    # A temporary surface to draw our clean game onto before applying effects
    game_surface = pygame.Surface((WIDTH, HEIGHT))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            
            terminal.handle_event(event)

        # Updates
        terminal.update()
        monitor.update(pygame.time.get_ticks())

        # Drawing
        game_surface.fill(bg_color)
        
        # Draw Left Panel
        monitor.draw(game_surface)

        # Draw Right Panel (Terminal + Border)
        pygame.draw.rect(game_surface, border_color, 
                         pygame.Rect(term_x, border_padding, term_width, HEIGHT - (2*border_padding)), 
                         width=2) 
        terminal.draw(game_surface, HEIGHT - 4*border_padding)

        # GLOW EFFECT (BLOOM)
        shrunk = pygame.transform.smoothscale(game_surface, (WIDTH // 2, HEIGHT // 2))
        glow = pygame.transform.smoothscale(shrunk, (WIDTH, HEIGHT))

        # COMPOSITING
        screen.blit(game_surface, (0, 0))
        screen.blit(glow, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        screen.blit(scanline_overlay, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()