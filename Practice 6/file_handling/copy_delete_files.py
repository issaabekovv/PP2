from pathlib import Path
import shutil
import os

file_path = Path("sample.txt")
backup_path = Path("sample_backup.txt")

if file_path.exists():
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("Line 3: This line was appended.\n")
        f.write("Line 4: Appending is successful.\n")

    print("New lines appended successfully.")

    with open(file_path, "r", encoding="utf-8") as f:
        print("\nUpdated file content:")
        print(f.read())

    shutil.copy(file_path, backup_path)
    print(f"Backup created: {backup_path}")

    if backup_path.exists():
        os.remove(backup_path)
        print(f"Deleted file: {backup_path}")
else:
    print("Original file does not exist.")