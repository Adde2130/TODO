import os

binary_extensions = (".exe", ".bin", ".dll", ".png", ".jpg")

# TODO: This is an example todo!

def is_todo_file(file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension in binary_extensions:
        return False 

    with open(file_path, "rb") as f:
        read_size = max(os.path.getsize(file_path), 512)
        chunk = f.read(read_size)

        if b'\0' in chunk: # Infers that the file is not text
            return False 

        f.seek(0)
        try:
            content = f.read().decode("utf-8")
        except UnicodeDecodeError:
            return False
        if not "TODO:" in content:
            return False 


    return True 


def gather_files():
    todo_files = []
    cwd = os.getcwd()
    for root, dirs, files in os.walk(cwd):
        for file in files:
            full_path = os.path.join(root, file)
            if not is_todo_file(full_path):
                continue

            rel_path = os.path.relpath(full_path, cwd)
            todo_files.append(rel_path)

    return todo_files

def print_todo_file(file_path):
    print(f"\x1b[96m{file_path}\x1b[39m")
    with open(file_path, "r") as file:
        i = 0
        while line_full := file.readline():
            i += 1
            line = line_full.strip()
            index = line.find("TODO")
            if index != -1:
                box_char = bytes([192]).decode('cp437')
                line_char = bytes([196]).decode('cp437')


                print(f"    {box_char}{line_char} * {line[index:]} \x1b[93m(line {i})\x1b[39m")


def main():
    files = gather_files()
    print("\x1b[94m* " + "-" * 76 + " *")
    for file in files:
        print_todo_file(file)
    print("\x1b[94m* " + "-" * 76 + " *\x1b[39m")

if __name__ == "__main__":
    main()
