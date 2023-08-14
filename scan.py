import sys
from pathlib import Path

pictures = list()
videos = list()
documents = list()
musics = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    "JPEG": pictures,
    "PNG" : pictures,
    "JPG" : pictures,
    "SVG" : pictures,
    "AVI" : videos,
    "MP4" : videos,
    "MOV" : videos,
    "MKV" : videos,
    "TXT" : documents,
    "DOC" : documents,
    "DOCX": documents,
    "PDF" : documents,
    "XLSX": documents,
    "PPTX": documents,
    "MP3" : musics,
    "OGG" : musics,
    "WAV" : musics,
    "AMR" : musics,
    "ZIP" : archives,
    "GZ"  : archives,
    "TAR" : archives
}


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        #чи є елемент сканованої папки сам папкою?
        if item.is_dir():
            #умова того, що не буде сканування у папках, які приготовлені для перенесення в них мотлоху
            if item.name not in ("PICTURES", "VIDEOS", "MUSICS", "DOCUMENTS", "OTHERS", "ARCHIVE"): 
                folders.append(item)
                #більш глибоке сканування, починаючи з папки, яку вже перевірили
                scan(item)
            continue
        
        #якщо елемент не є папка, значить він файл
        extension = get_extensions(file_name=item.name)
        #повний шлях до файлу
        new_name = folder/item.name
        #якщо файл не має росширення ми додаємо його в папку Others
        if not extension:
            others.append(new_name)
        #якщо росширення є, але воно не в списку відомих,
        #тоді додаєм невідомі росширення у окремий список
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


# if __name__ == '__main__':
#     path = sys.argv[1]
#     print(f"Start in {path}")

#     arg = Path(path)
#     scan(arg)

#     print(f"Pictures: {pictures}\n")
#     print(f"Video files: {videos}\n")
#     print(f"Documents: {documents}\n")
#     print(f"Music files: {musics}\n")
#     print(f"Archives: {archives}\n")
#     print(f"Unknown files: {others}\n")
#     print(f"All extensions: {extensions}\n")
#     print(f"Unknown extensions: {unknown}\n")