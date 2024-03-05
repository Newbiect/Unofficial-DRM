import os

class MemoryFileSystem:
    def __init__(self):
        self.memory_file_system = {}

    def get_file_name(self, path):
        return os.path.basename(path)

    def file_exists(self, file_name):
        return file_name in self.memory_file_system

    def get_file_size(self, file_name):
        if file_name in self.memory_file_system:
            return len(self.memory_file_system[file_name])
        else:
            print(f"Failed to get size for {file_name}")
            return -1

    def list_files(self):
        return list(self.memory_file_system.keys())

    def read(self, path):
        file_name = self.get_file_name(path)
        if file_name in self.memory_file_system:
            return self.memory_file_system[file_name]
        else:
            print(f"Failed to read from {path}")
            return ""

    def write(self, path, content):
        file_name = self.get_file_name(path)
        self.memory_file_system[file_name] = content
        return len(content)

    def remove_file(self, file_name):
        if file_name in self.memory_file_system:
            del self.memory_file_system[file_name]
            return True
        else:
            print(f"Cannot find file to remove: {file_name}")
            return False

    def remove_all_files(self):
        self.memory_file_system.clear()
        return len(self.memory_file_system) == 0