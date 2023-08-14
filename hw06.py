import sys
import re
import shutil
from pathlib import Path
from files_generator import file_generator

images = list()
video = list()
documents = list()
audio = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    "JPEG": images,
    "PNG" : images,
    "JPG" : images,
    "SVG" : images,
    "AVI" : video,
    "MP4" : video,
    "MOV" : video,
    "MKV" : video,
    "TXT" : documents,
    "DOC" : documents,
    "DOCX": documents,
    "PDF" : documents,
    "XLSX": documents,
    "PPTX": documents,
    "MP3" : audio,
    "OGG" : audio,
    "WAV" : audio,
    "AMR" : audio,
    "ZIP" : archives,
    "GZ"  : archives,
    "TAR" : archives
}


UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

#функція нормалізації імен
def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"

#функція отримання розширень файлів
def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


#функція сканування папок
def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            #ігноруємо вказані папки при скануванні
            if item.name not in ("IMAGES", "VIDEO", "AUDIO", "DOCUMENTS", "ARCHIVES"): 
                folders.append(item)
                #скануємо далі, починаючи з папки, яку вже перевірили
                scan(item)
            continue
        
        #якщо елемент не є папка, значить він файл
        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        #якщо файл не має росширення ми додаємо його в папку Others
        if not extension:
            others.append(new_name)
        #якщо росширення є, але воно невідоме -> в окремий список
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


#функція обробки файлів
def handle_file(path, root_folder, dest):
    
    target_folder = root_folder/dest
    target_folder.mkdir(exist_ok=True)
    
    path.replace(target_folder/normalize(path.name))


#функція обробки архівів
def handle_archive(path, root_folder, dest):
    
    target_folder = root_folder/dest
    target_folder.mkdir(exist_ok=True)

    new_name = path.name.removesuffix(path.suffix)
    archive_folder = target_folder/new_name
    try:
        shutil.unpack_archive(path, target_folder/f'{normalize(new_name)}')
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
    scan(folder_path)

    for file in images:
        handle_file(file, folder_path, "IMAGES")
    for file in video:
        handle_file(file, folder_path, "VIDEO")
    for file in audio:
        handle_file(file, folder_path, "AUDIO")
    for file in documents:
        handle_file(file, folder_path, "DOCUMENTS")
    for file in others:
        handle_file(file, folder_path, "OTHERS")
    for file in archives:
        handle_archive(file, folder_path, "ARCHIVES")

    get_folder_objects(folder_path)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    file_generator(arg)
    main(arg.resolve())