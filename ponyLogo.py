import os
import shutil

# Source file path (current location of the file)
source = 'C:\Users\kebki\DubHacks 24\DubHacks24\templates\PonyLogo.png'

# Destination directory (where the file should be moved)
destination_folder = 'static/uploads/'

# Ensure the destination directory exists
os.makedirs(destination_folder, exist_ok=True)

# Define the full destination path for the file
destination = os.path.join(destination_folder, 'PonyLogo.png')

# Move the file
shutil.move(source, destination)

# Confirm the file has been moved
if os.path.exists(destination):
    print(f"File successfully moved to {destination}")
else:
    print("File move failed.")
