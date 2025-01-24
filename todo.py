import os
import time


ALLOW_MULTILINE_TODOS = False


textfile_extensions = {
    ".txt", ".md", ".py", ".java",
    ".c", ".cpp", ".h", ".hpp", ".js",
    ".html", ".css", ".rb", ".php",
    ".ts", ".go", ".rs", ".swift",
    ".kt", ".sh", ".cs", ".lua",
    ".html", ".json", ".bash", ".bat",
    ".cmd", ".ps1", ".zsh", ".ini",
    ".cfg", ".conf", ".gradle", 
    ".gitignore", ".asm", ".s", ".erl",
    ".hs", ".lhs", ".ex", ".pl", 
    ".scala", ".sc", ".vb", ".log"
}

comments = {
    "//", "#"
}

# TODO: This is an example todo!
#       I hope this works!

def time_func(func):

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        total_time = end - start
        print(f"Time for {func.__name__}: {total_time}")
        return result

    return wrapper


def is_todo_file(file_path):
    filename, file_extension = os.path.splitext(file_path)

    if file_extension not in textfile_extensions:
        if os.path.basename(filename).lower() != "makefile":
            return False 

    with open(file_path, "r") as f:
        try:
            for line in f:
                if "TODO" in line:
                    return True
        except UnicodeDecodeError:
            return False

    return False


@time_func
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
        parsing_todo = False
        while line_full := file.readline():
            i += 1
            line = line_full.strip()
            index = line.find("TODO")
            if index != -1:
                box_char = bytes([192]).decode('cp437')
                line_char = bytes([196]).decode('cp437')

                parsing_todo = True

                print(f"    {box_char}{line_char} * {line[index:]} \x1b[93m(line {i})\x1b[39m")
            elif parsing_todo and ALLOW_MULTILINE_TODOS:
                comment = ""
                for c in comments:
                    if line.startswith(c):
                        comment = c
                        break
                
                if comment == "":
                    parsing_todo = False
                    continue
                
                line = line[len(comment):].lstrip()
                print(" " * 15 + line)


def main():
    files = gather_files()
    if len(files) == 0:
        return

    print("\x1b[94m* " + "-" * 76 + " *")
    for file in files:
        print_todo_file(file)
    print("\x1b[94m* " + "-" * 76 + " *\x1b[39m")

if __name__ == "__main__":
    main()
