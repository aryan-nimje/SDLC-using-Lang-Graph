from pathlib import Path
import os

FOLDER_PATH = "workspace"

file = "artifaclan.md"

full_path = os.path.join(FOLDER_PATH, file)

print(full_path)

folder = "workspace"
print(os.listdir(folder))