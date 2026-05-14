import pygame
import sys

class VirusTUI:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Retro color palette
        self.bg_color = (13, 2, 8)
        self.text_color = (0, 255, 65)
        self.highlight_bg = (0, 255, 65)
        self.highlight_fg = (13, 2, 8)
        
        self.font = pygame.font.Font('assets/fonts/Minecraftia-Regular.ttf', 14)
        self.title_font = pygame.font.Font('assets/fonts/Minecraftia-Regular.ttf', 18)

        self.font = pygame.font.SysFont('couriernew, consolas, monospace', 18, bold=True)
        self.title_font = pygame.font.SysFont('couriernew, consolas, monospace', 20, bold=True)

        self.title = self.title_font.render("Swarm Interface v1.0", True, self.text_color)

        self.char_width = self.font.size("A")[0]
        self.char_height = self.font.size("A")[1]
    
        
        # Dummy Data (will add it from vfs.py later)
        self.files = [
            {"name": "system32/", "type": "Directory", "size": "4.2 GB"},
            {"name": "kernel.dll", "type": "File", "size": "1.2 MB"},
            {"name": "user_data/", "type": "Directory", "size": "800 MB"},
            {"name": "config.sys", "type": "File", "size": "12 KB"}
        ]
        
        self.actions = ["[ Infect ]", "[ Replicate ]", "[ Cloak ]", "[ Back ]"]
        
        # State Tracking
        self.selected_row = 0
        self.selected_action = 0
        self.in_action_menu = False 

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            # inside file list
            if not self.in_action_menu:
                if event.key == pygame.K_UP:
                    # self.selected_row = max(0, self.selected_row - 1)
                    if self.selected_row <= 0:
                        self.selected_row = len(self.files) - 1
                    else:
                        self.selected_row -= 1
                elif event.key == pygame.K_DOWN:
                    # self.selected_row = min(len(self.files) - 1, self.selected_row + 1)
                    if self.selected_row >= len(self.files) - 1:
                        self.selected_row = 0
                    else:
                        self.selected_row += 1
                elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                    # Switch focus to the bottom action menu
                    self.in_action_menu = True
                    
                    
                    
            # inside bottom menu
            else:
                if event.key == pygame.K_LEFT:
                    self.selected_action = max(0, self.selected_action - 1)
                elif event.key == pygame.K_RIGHT:
                    self.selected_action = min(len(self.actions) - 1, self.selected_action + 1)
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_UP:
                    # Cancel action, go back to file list
                    self.in_action_menu = False
                elif event.key == pygame.K_RETURN:
                    # Execute the action!
                    action = self.actions[self.selected_action]
                    target = self.files[self.selected_row]['name']
                    print(f"Executing {action} on {target}")
                    self.in_action_menu = False # Reset focus

    def draw(self, surface):
        title_y = self.y + (self.height * 0.02)  
        header_y = self.y + (self.height * 0.12)  
        list_y = self.y + (self.height * 0.20)    
        menu_y = self.y + self.height - (self.height * 0.15) 
        help_y = self.y + self.height - (self.height * 0.05) 

        max_chars = self.width // self.char_width

        surface.blit(self.title, (self.x + self.width//2 - self.title.get_width()//2, title_y))

        surface.blit(self.font.render("Name", True, self.text_color), (self.x, header_y))
        surface.blit(self.font.render("Type", True, self.text_color), (self.width//2 - 10, header_y))
        surface.blit(self.font.render("Size", True, self.text_color), (self.width - 26, header_y))

        line_y = header_y + self.font.get_height() + 5
        pygame.draw.line(surface, self.text_color, (self.x, line_y), (self.x + self.width, line_y))

        # File List
        current_y = list_y
        for i, file_data in enumerate(self.files):
            
            name_str = file_data['name']
            if len(name_str)>15:
                name_str = name_str[:16] + "..."
            
            
            if i == self.selected_row and not self.in_action_menu:
                rect = pygame.Rect(self.x, current_y, self.width, self.char_height)
                pygame.draw.rect(surface, self.highlight_bg, rect)

                name = self.font.render(name_str, True, self.highlight_fg)
                data_type = self.font.render(file_data['type'], True, self.highlight_fg)
                size = self.font.render(file_data['size'], True, self.highlight_fg)
                surface.blit(name, (self.x, current_y))
                surface.blit(data_type, (self.width//2 - 10, current_y))
                surface.blit(size, (self.width - size.get_width() + 18, current_y))
            else:
                name = self.font.render(name_str, True, self.text_color)
                data_type = self.font.render(file_data['type'], True, self.text_color)
                size = self.font.render(file_data['size'], True, self.text_color)
                surface.blit(name, (self.x, current_y))
                surface.blit(data_type, (self.width//2 - 10, current_y))
                surface.blit(size, (self.width - size.get_width() + 18, current_y))
                
            # Row spacing
            current_y += self.char_height + 5 

        # width of all the action
        total_text_width = sum([self.font.size(act)[0] for act in self.actions])
        
        # buttons
        available_empty_space = self.width - total_text_width
        dynamic_padding = available_empty_space // (len(self.actions) + 1)
        
        current_action_x = self.x + dynamic_padding
        for i, action in enumerate(self.actions):
            if i == self.selected_action and self.in_action_menu:
                act_surf = self.font.render(action, True, self.highlight_fg, self.highlight_bg)
            else:
                act_surf = self.font.render(action, True, self.text_color)
                
            surface.blit(act_surf, (current_action_x, menu_y))

            current_action_x += act_surf.get_width() + dynamic_padding

        # Help Text
        help_text = "[ARROWS] Navigate   [ENTER] Select   [ESC] Cancel"
        help_surf = self.font.render(help_text, True, (100, 100, 100))
        surface.blit(help_surf, (self.x + self.width//2 - help_surf.get_width()//2, help_y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    tui = VirusTUI(20, 20, 560, 360)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            tui.handle_event(event)
            
        screen.fill((13, 2, 8))
        tui.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()