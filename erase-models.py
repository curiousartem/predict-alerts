import os
import time
import getpass

# Ask for user confirmation


confirmation = ""
for i in range(5, 0, -1):
    print("\033[2J\033[H", end="")  # Clear console
    print(f"\033[91mAre you sure you want to delete all models? (yes/no): \033[0m({i})", end="\r")
    time.sleep(1)
    if i == 1:
        print("\033[2J\033[H", end="")  # Clear console

confirmation = input('\033[91mAre you sure you want to delete all models? (yes/no): \033[0m')

if confirmation.lower() == "yes":
    # Delete all models in the directory
    models_dir = "models/"
    for file_name in os.listdir(models_dir):
        file_path = os.path.join(models_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("All models have been deleted.")
else:
    print("Deletion canceled.")
