from pathlib import Path

file_path = Path("sample.txt")

if file_path.exists():
    with open(file_path, "r", encoding="utf-8") as f:
        print("Using read():")
        print(f.read())

    with open(file_path, "r", encoding="utf-8") as f:
        print("Using readline():")
        print(f.readline().strip())
        print(f.readline().strip())

    with open(file_path, "r", encoding="utf-8") as f:
        print("Using readlines():")
        lines = f.readlines()
        for line in lines:
            print(line.strip())
else:
    print("File does not exist.")