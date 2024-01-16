import sys
from sort import organize_files

if __name__ == "__main__":
    if len(sys.argv) > 1:
        organize_files(sys.argv[1])
    else:
        print("Proszę podać ścieżkę do folderu.")
