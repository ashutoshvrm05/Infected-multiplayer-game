import pygame
import sys
from core.vfs import VirtualFileSystem


class VirusTUI:
    def __init__(self, x, y, width, height, vfs, node_map):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vfs = vfs
        self.node_map = node_map

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
    
        self.actions = ["[ Infect ]", "[ Replicate ]", "[ Cloak ]", "[ Back ]"]
        
        # State Tracking
        self.selected_row = 0
        self.selected_action = 0
        self.in_action_menu = False 

        self.files = []
        self.update_file_list()
        

    
    def update_file_list(self):
        """Fetches real data from the VFS and formats it for the TUI."""
        self.files.clear()
        
        if self.vfs.current_dir.name != "/root":
            self.files.append({"name": "..", "type": "DIR", "size": "- "})

        # Looping through the actual children in the current VFS directory
        for name, node in self.vfs.current_dir.children.items():
            if type(node).__name__ == "Directory":
                self.files.append({"name": name + "/", "type": "DIR", "size": "- "})
            else:
                size_str = f"{len(node.content) * 4} KB" if hasattr(node, 'content') else "UNK"
                self.files.append({"name": name, "type": "FILE", "size": size_str})
                
        # Safety check: if folder empties out, reset cursor
        if self.selected_row >= len(self.files):
            self.selected_row = max(0, len(self.files) - 1)

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
                # elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                #     # Switch focus to the bottom action menu
                #     self.in_action_menu = True
            
                elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                    # Check if they are trying to enter a directory!
                    if self.files and self.files[self.selected_row]["type"] == "DIR":
                        target = self.files[self.selected_row]["name"].replace("/", "")
                        self.vfs.cd(target)
                        self.update_file_list() # Refresh the screen!
                        self.selected_row = 0   # Reset cursor to top
                        self.node_map.center_camera_on(self.vfs.current_dir)
                    else:
                        # It's a file, so switch focus to the bottom action menu
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
        line_y = header_y + self.font.get_height() + 7
        list_y = line_y + 7
        menu_y = self.y + self.height - (self.height * 0.15) 
        help_y = self.y + self.height - (self.height * 0.05) 

        max_chars = self.width // self.char_width

        # Title
        surface.blit(self.title, (self.x + self.width//2 - self.title.get_width()//2, title_y))

        # List heading
        surface.blit(self.font.render("Name", True, self.text_color), (self.x, header_y))
        surface.blit(self.font.render("Type", True, self.text_color), (self.x + self.width//2 - 10, header_y))
        surface.blit(self.font.render("Size", True, self.text_color), (self.x + self.width - 40, header_y))

        # Line
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
                surface.blit(data_type, (self.x + self.width//2 - 10, current_y))
                surface.blit(size, (self.x + self.width - size.get_width(), current_y))
            else:
                name = self.font.render(name_str, True, self.text_color)
                data_type = self.font.render(file_data['type'], True, self.text_color)
                size = self.font.render(file_data['size'], True, self.text_color)
                surface.blit(name, (self.x, current_y))
                surface.blit(data_type, (self.x + self.width//2 - 10, current_y))
                surface.blit(size, (self.x + self.width - size.get_width(), current_y))
                
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


class NodeMap:
    def __init__(self, x, y, width, height, vfs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vfs = vfs
        
        self.font = pygame.font.SysFont('couriernew, consolas, monospace', 12, bold=True)
        self.line_color = (0, 100, 25) 
        self.node_color = (0, 255, 65) 
        self.bg_color = (10, 5, 15)
        
        # Camera & Panning State 
        self.camera_x = 0
        self.camera_y = 0
        self.is_dragging = False
        
        # Layout Generation
        self.node_positions = {}
        self.build_layout()
        
        # Start the game with the camera looking at the folder you spawn in
        self.center_camera_on(self.vfs.current_dir)

    def build_layout(self):
        """Recursively maps the entire VFS into fixed X, Y coordinates."""
        self.node_positions.clear()
        
        # A recursive function to place nodes
        def traverse(node, depth, current_x):
            if not hasattr(node, 'children') or len(node.children) == 0:
                self.node_positions[node] = (current_x, depth * 80)
                return current_x + 80 
            
            # If it has children, lay them out first
            start_x = current_x
            for child in node.children.values():
                current_x = traverse(child, depth + 1, current_x)
                
            # centering the parent above its children
            children_xs = [self.node_positions[c][0] for c in node.children.values()]
            my_x = sum(children_xs) / len(children_xs)
            self.node_positions[node] = (my_x, depth * 80)
            
            return current_x
            
        traverse(self.vfs.root, 0, 0)

    def center_camera_on(self, node):
        """Moves the camera so the target node is in the center of the map window."""
        if node in self.node_positions:
            nx, ny = self.node_positions[node]
            # Calculate the offset needed to put (nx, ny) in the center of our bounding box
            self.camera_x = (self.width // 2) - nx
            self.camera_y = (self.height // 2) - ny

    def handle_event(self, event):
        """Listens for mouse clicks and drags to pan the camera."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                # Check if they clicked inside the map window
                if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                    self.is_dragging = True
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                # event.rel contains how many pixels the mouse moved since the last frame
                self.camera_x += event.rel[0]
                self.camera_y += event.rel[1]

    def draw(self, surface):
        
        # rect region 
        clip_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        surface.set_clip(clip_rect)
        
        # Fill the map background
        pygame.draw.rect(surface, self.bg_color, clip_rect)

        # DRAW LINES 
        for node, (nx, ny) in self.node_positions.items():
            if hasattr(node, 'children'):
                for child in node.children.values():
                    if child in self.node_positions:
                        cx, cy = self.node_positions[child]
                        # Apply camera offset to raw coordinates
                        start_pos = (self.x + nx + self.camera_x, self.y + ny + self.camera_y)
                        end_pos = (self.x + cx + self.camera_x, self.y + cy + self.camera_y)
                        pygame.draw.line(surface, self.line_color, start_pos, end_pos, 2)

        # DRAW NODES
        for node, (nx, ny) in self.node_positions.items():
            screen_x = self.x + nx + self.camera_x
            screen_y = self.y + ny + self.camera_y
            
            # nodes that are currently scrolled off-screen
            if not (-50 < screen_x - self.x < self.width + 50 and -50 < screen_y - self.y < self.height + 50):
                continue

            is_dir = type(node).__name__ == "Directory"
            is_current = (node == self.vfs.current_dir)

            # Draw the node shape
            if is_current:
                # The current location 
                pygame.draw.circle(surface, self.bg_color, (screen_x, screen_y), 18) 
                pygame.draw.circle(surface, self.node_color, (screen_x, screen_y), 16, 3)
                pygame.draw.circle(surface, (255, 0, 60), (screen_x, screen_y), 6) 
            elif is_dir:
                pygame.draw.circle(surface, self.bg_color, (screen_x, screen_y), 8) 
                pygame.draw.circle(surface, self.node_color, (screen_x, screen_y), 8, 2)
            else:
                pygame.draw.circle(surface, self.node_color, (screen_x, screen_y), 5)
                
            # Draw the node name
            text_color = self.node_color if is_current else self.line_color
            text_surf = self.font.render(node.name[:10], True, text_color)
            surface.blit(text_surf, (screen_x - text_surf.get_width()//2, screen_y + 12))

        # REMOVE CLIPPING REGION
        surface.set_clip(None)
        
        # physical border around the map
        pygame.draw.rect(surface, self.node_color, clip_rect, 2)


def main():
    pygame.init()

    WIDTH = 1000
    HEIGHT = 600
    # Widen the screen to fit both UI elements
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Swarm Interface")
    clock = pygame.time.Clock()
    
    # the file system
    vfs = VirtualFileSystem()
    
    # Tactical Map (x=20, width=360)
    node_map = NodeMap(20, 20, 360, 560, vfs)
    
    # The TUI (x=400, width=580)
    tui = VirusTUI(400, 20, 580, 560, vfs, node_map)

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
            if event.type == pygame.QUIT: running = False
            tui.handle_event(event)
            node_map.handle_event(event)
            
        screen.fill((13, 2, 8))
        game_surface.fill((10, 5, 15))
        
        # Draw both tui and map
        node_map.draw(game_surface)
        tui.draw(game_surface)

        # CREATE THE GLOW EFFECT (BLOOM)
        shrunk = pygame.transform.smoothscale(game_surface, (WIDTH // 2, HEIGHT // 1))
        glow = pygame.transform.smoothscale(shrunk, (WIDTH, HEIGHT))

        # COMPOSITE EVERYTHING TO THE ACTUAL SCREEN
        screen.blit(game_surface, (0, 0))
        
        # Additive blend the blurred glow on top! 
        screen.blit(glow, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        
        # Step C: Slap the scanlines over the very top
        screen.blit(scanline_overlay, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()