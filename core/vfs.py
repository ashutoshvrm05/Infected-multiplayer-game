
# both files and folders are nodes 
class Node:
    """Base class for both files and directories."""
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

# files class
class File(Node):
    def __init__(self, name, content="", parent=None):
        super().__init__(name, parent)
        self.content = content
        self.is_infected = False  

# folder class
class Directory(Node):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.children = {}  

    def add_child(self, node):
        self.children[node.name] = node
        node.parent = self

class VirtualFileSystem:
    def __init__(self):
        self.root = Directory("/root")
        self.current_dir = self.root
        self._build_default_system()

    def _build_default_system(self):
        
        # making virtual file system
        sys_dir = Directory("sys")
        users_dir = Directory("users")
        home_dir = Directory("ashutosh")
        downloads_dir = Directory("downloads")
        pictures_dir = Directory("pictures")
        documents_dir = Directory("documents")
        videos_dir = Directory("videos")
        phone_recovery_dir = Directory("phone recovery")
        dcmi_dir = Directory("DCMI")
        whatsapp_dir = Directory("whatsapp")
        camera_dir = Directory("camera")
        screenshot_dir = Directory("screenshot")

        pic1 = File("pic1.jpeg")
        pic2 = File("pic2.jpeg")
        pic3 = File("pic3.jpeg")

        
        self.root.add_child(sys_dir)
        self.root.add_child(users_dir)
        users_dir.add_child(home_dir)
        home_dir.add_child(downloads_dir)
        home_dir.add_child(pictures_dir)
        home_dir.add_child(documents_dir)
        home_dir.add_child(videos_dir)
        home_dir.add_child(phone_recovery_dir)
        phone_recovery_dir.add_child(whatsapp_dir)
        phone_recovery_dir.add_child(dcmi_dir)
        dcmi_dir.add_child(screenshot_dir)
        dcmi_dir.add_child(camera_dir)

        videos_dir.add_child(pic1)
        videos_dir.add_child(pic2)
        videos_dir.add_child(pic3)
        
        sys_dir.add_child(File("kernel.dll", "CRITICAL SYSTEM FILE"))

        self.current_dir = home_dir

    def get_path(self):
        """Builds the string representation of the current path (e.g., /users/ashutosh)"""
        if self.current_dir.name == "/":
            return "/"
            
        parts = []
        curr = self.current_dir
        while curr.name != "/root":
            parts.append(curr.name)
            curr = curr.parent
            
        return "/" + "/".join(reversed(parts))

    def ls(self):
        """Returns a list of items in the current directory."""
        if not self.current_dir.children:
            return []
        
        items = []
        for name, node in self.current_dir.children.items():
            if isinstance(node, Directory):
                items.append(name + "/") 
            else:
                items.append(name)
        return items

    def cd(self, target_name):
        """Changes the current directory. Returns an error message if it fails."""
        if target_name == "..":
            if self.current_dir.parent is not None:
                self.current_dir = self.current_dir.parent
            return None 
            
        if target_name == "/":
            self.current_dir = self.root
            return None

        if target_name in self.current_dir.children:
            node = self.current_dir.children[target_name]
            if isinstance(node, Directory):
                self.current_dir = node
                return None
            else:
                return f"cd: not a directory: {target_name}"
        else:
            return f"cd: no such file or directory: {target_name}"