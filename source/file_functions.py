import os

# Function to return all the files in the given path
def getPaths(path):
    PATHS = os.listdir(path)
    return PATHS

# Function to rename a file/folder
def rename(old_name, new_name):
    os.rename(old_name, new_name)


PATH = 'D:\images\Walpapers'
files = getPaths(PATH)
count = 0

for file in files:
    extension = file.split(".")
    count += 1
    new_name = "wallpaper-" + str(count) + "." + extension[len(extension)-1]
    old_path = os.path.join(PATH, file)
    new_path = os.path.join(PATH, new_name)
    rename(old_path, new_path)
