import os

# Function to return all the files in the given path
def getPaths(path):
    PATHS = os.listdir(path)
    return PATHS

# Function to rename a file/folder
def rename(old_name, new_name):
    os.rename(old_name, new_name)


PATH = r'D:\dsa\3-lifecycle\2-research-study\1-project\0-sign-language-translator\1-code\hand-gesture-recognition-mediapipe\assets\videos'
folders = getPaths(PATH)

for folder in folders:
    path = os.path.join(PATH, folder)
    sub_folders = getPaths(path)
    print(sub_folders)