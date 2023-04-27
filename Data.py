
"""
line 1:     indices
line 2:     names
line 3+:    type x y w h
"""
from os import read


def replace_line(line, text):
    with open("Levels.txt", 'r+') as f:
        lines = f.readlines()
        
    lines[line] = text + "\n"
    with open("Levels.txt", 'w') as f:
        f.write("".join(lines))

def append_line(line, text):
    with open("Levels.txt", 'r+') as f:
        lines = f.readlines()
        
    lines[line] = lines[line][:-1] + text + "\n"
    with open("Levels.txt", 'w') as f:
        f.write("".join(lines))
        
def append_EOF(string):
    with open("Levels.txt", 'a') as f:
        f.write(string)

def read_index() -> list:
    with open("Levels.txt", 'r+') as f:
        return f.readline(0).strip().split(" ")

def read_names() -> list:
    with open("Levels.txt", 'r') as f:
        return list(zip(f.readline(0).strip().split(), f.readline(1).strip().split()))

class Levels:

    def __init__(self) -> None:
        self.levels = read_names()
    
    def new_level(self, name, objects):
        if len(objects) < 4:
            return False
        indices = read_index()
        append_line(0, " " + str(indices[-1] + len(objects)))
        append_line(1, " " + name)
        for obj in objects:
            line = "%s %d %d %d %d\n" %(obj.t, obj.x, obj.y, obj.w, obj.h)
            append_EOF(line)