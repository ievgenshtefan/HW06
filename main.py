import shutil
import sys
import scan
import normalize
from pathlib import Path
from files_generator import file_generator


#функція обробки файлів
def handle_file(path, root_folder, dest):
    #вказуємо папку куди буде зберігатись
    target_folder = root_folder/dest
    target_folder.mkdir(exist_ok=True)
    #нормалізовуємо імена файлів
    path.replace(target_folder/normalize.normalize(path.name))

#функція обробки архівів
def handle_archive(path, root_folder, dest):
    
    target_folder = root_folder/dest
    target_folder.mkdir(exist_ok=True)

    new_name = path.name.removesuffix(path.suffix)
    archive_folder = target_folder/new_name
    try:
        shutil.unpack_archive(path, target_folder/f'{normalize.normalize(new_name)}')
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()

#функція видалення пустих папок
def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

#
def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass

def main(folder_path):
    scan.scan(folder_path)

    for file in scan.pictures:
        handle_file(file, folder_path, "PICTURES")

    for file in scan.videos:
        handle_file(file, folder_path, "VIDEOS")

    for file in scan.musics:
        handle_file(file, folder_path, "MUSICS")

    for file in scan.documents:
        handle_file(file, folder_path, "DOCUMENTS")
    
    for file in scan.others:
        handle_file(file, folder_path, "OTHERS")

    for file in scan.archives:
        handle_archive(file, folder_path, "ARCHIVE")

    get_folder_objects(folder_path)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    file_generator(arg)
    main(arg.resolve())