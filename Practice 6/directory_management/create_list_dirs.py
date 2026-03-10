import os
from pathlib import Path

base_dir = Path("test_dir")
nested_dir = base_dir / "subdir1" / "subdir2"
nested_dir.mkdir(parents=True, exist_ok=True)

print("Nested directories created successfully.")

print("Current working directory:")
print(os.getcwd())

print("\nFiles and folders in current directory:")
for item in os.listdir():
    print(item)

print("\nSearching for .py files:")
for path in Path(".").rglob("*.py"):
    print(path)