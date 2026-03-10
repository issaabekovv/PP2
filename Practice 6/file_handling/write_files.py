from pathlib import Path

file_path = Path("sample.txt")

with open(file_path, "w", encoding="utf-8") as f:
    f.write("Python File Handling Practice\n")
    f.write("Line 1: Hello world!\n")
    f.write("Line 2: This is Practice 6.\n")

print("File created and data written successfully.")