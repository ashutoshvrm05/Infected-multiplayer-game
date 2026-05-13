import pygame
import sys

class VirusTUI:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.font = pygame.font.Font('assets/fonts/VT323-Regular.ttf', 24)
        self.title_font = pygame.font.Font('assets/fonts/VT323-Regular.ttf', 24)
        self.font = pygame.font.SysFont('couriernew, consolas, monospace', 18, bold=True)
        self.title_font = pygame.font.SysFont('couriernew, consolas, monospace', 20, bold=True)
        
        # Retro color palette
        self.bg_color = (13, 2, 8)
        self.text_color = (0, 255, 65)     
        self.highlight_bg = (0, 255, 65)   
        self.highlight_fg = (13, 2, 8)     
        
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
            # file list
            if not self.in_action_menu:
                if event.key == pygame.K_UP:
                    self.selected_row = max(0, self.selected_row - 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_row = min(len(self.files) - 1, self.selected_row + 1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                    # Switch focus to the bottom action menu
                    self.in_action_menu = True
                    
                    
            # bottom menu
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
        y_offset = self.y
        
        # Top 
        title = self.title_font.render("Swarm Interface v1.0", True, self.text_color)
        surface.blit(title, (self.x + self.width//2 - title.get_width()//2, y_offset))
        y_offset += 40
        
        # Table Headers
        headers = f"{'Name'.ljust(20)} {'Type'.ljust(15)} {'Size'.rjust(10)}"
        header_surf = self.font.render(headers, True, self.text_color)
        surface.blit(header_surf, (self.x, y_offset))
        y_offset += 5
        
        # Header underline
        pygame.draw.line(surface, self.text_color, (self.x, y_offset + 20), (self.x + self.width, y_offset + 20))
        y_offset += 30
        
        # File List
        for i, file_data in enumerate(self.files):
            row_text = f"{file_data['name'].ljust(20)} {file_data['type'].ljust(15)} {file_data['size'].rjust(10)}"
            
            if i == self.selected_row and not self.in_action_menu:

                rect = pygame.Rect(self.x, y_offset, self.width, self.font.get_height())
                pygame.draw.rect(surface, self.highlight_bg, rect)
                # inverted text
                text_surf = self.font.render(row_text, True, self.highlight_fg)
            else:
                text_surf = self.font.render(row_text, True, self.text_color)
                
            surface.blit(text_surf, (self.x, y_offset))
            y_offset += self.font.get_height() + 5
            
        # Bottom Action Menu
        menu_y = self.y + self.height - 60
        
        current_x = self.x + 20
        for i, action in enumerate(self.actions):
            if i == self.selected_action and self.in_action_menu:
                # Highlight active menu option
                act_surf = self.font.render(action, True, self.highlight_fg, self.highlight_bg)
            else:
                act_surf = self.font.render(action, True, self.text_color)
                
            surface.blit(act_surf, (current_x, menu_y))
            current_x += act_surf.get_width() + 20 # Spacing between buttons
            
        help_text = "[ARROWS] Navigate   [ENTER] Select   [ESC] Cancel"
        help_surf = self.font.render(help_text, True, (100, 100, 100)) # Dim grey
        surface.blit(help_surf, (self.x + self.width//2 - help_surf.get_width()//2, menu_y + 30))


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