from pathlib import Path
import shutil

source_dir = Path("source_files")
target_dir = Path("target_files")

source_dir.mkdir(exist_ok=True)
target_dir.mkdir(exist_ok=True)

# Create a sample file in source_dir
sample_file = source_dir / "example.txt"
with open(sample_file, "w", encoding="utf-8") as f:
    f.write("This file will be copied and moved.\n")

# Copy file
copied_file = target_dir / "example_copy.txt"
shutil.copy(sample_file, copied_file)
print(f"Copied {sample_file} to {copied_file}")

# Move file
moved_file = target_dir / "example_moved.txt"
shutil.move(str(sample_file), str(moved_file))
print(f"Moved {sample_file} to {moved_file}")