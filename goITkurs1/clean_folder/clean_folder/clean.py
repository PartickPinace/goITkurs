import os
import shutil
import re
import sys


def main():
    if len(sys.argv) > 1:
        organize_files(sys.argv[1])
    else:
        print("Proszę podać ścieżkę do folderu.")

def normalize(name):
    transliteration = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z'}
    name = ''.join(transliteration.get(c, c) for c in name)
    return re.sub(r'\W+', '_', name)

def organize_files(directory):
    file_categories = {
        'images': ['jpeg', 'png', 'jpg', 'svg'],
        'videos': ['avi', 'mp4', 'mov', 'mkv'],
        'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
        'music': ['mp3', 'ogg', 'wav', 'amr'],
        'archives': ['zip', 'gz', 'tar'],
        'unknown': []
    }

    for category in file_categories.keys():
        os.makedirs(os.path.join(directory, category), exist_ok=True)

    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            ext = filename.lower().split('.')[-1]
            new_filename = normalize(filename)
            for category, extensions in file_categories.items():
                if ext in extensions:
                    shutil.move(os.path.join(directory, filename), os.path.join(directory, category, new_filename))
                    break
            else:
                if ext != new_filename.split('.')[-1]:
                    shutil.move(os.path.join(directory, filename), os.path.join(directory, 'unknown', new_filename))
    for foldername in os.listdir(directory):
        subfolder = os.path.join(directory, foldername)
        if os.path.isdir(subfolder) and foldername not in file_categories:
            organize_files(subfolder)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        organize_files(sys.argv[1])
    else:
        print("Proszę podać ścieżkę do folderu.")
