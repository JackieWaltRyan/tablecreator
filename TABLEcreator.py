import sys
from base64 import b64encode
from json import loads, dump, dumps
from os import walk, makedirs
from os.path import exists, join, abspath, dirname
from sys import exit

from bs4 import BeautifulSoup


def resource_path(file):
    return join(getattr(sys, "_MEIPASS", dirname(p=abspath(path=__file__))), file)


def load_fake():
    with open(file=resource_path(file="fake.json"),
              mode="r",
              encoding="UTF-8") as fake_json:
        return loads(s=fake_json.read())


SETTINGS = {"Consumable": False,
            "Decore": False,
            "DestroyedHouse": False,
            "EquestriaGirls": False,
            "ExpansionZone": False,
            "Inn": False,
            "MasterExpansionZone": False,
            "PartySceneDecore": False,
            "Path": False,
            "Pony": False,
            "Pony_House": False,
            "PonyPart": False,
            "PonySet": False,
            "ProfileAvatar": False,
            "ProfileAvatarFrame": False,
            "ProgressBooster": False,
            "QuestSpecialItem": False,
            "TapableContainer": False,
            "Theme": False,
            "Totem": False,
            "TravelersCafe": False}

CATEGORIES = {"Consumable": [["Name", "Unlocal"], ["Graphic", "Sprite"], load_fake()["all"]],
              "Decore": [["Name", "Unlocal"], ["Shop", "Icon"], load_fake()["decore"]],
              "DestroyedHouse": [["Name", "Unlocal"], ["Icon", "QuestIcon"], load_fake()["house"]],
              "EquestriaGirls": [["Name", "Unlocal"], ["Icons", "Icons_Avatar"], load_fake()["all"]],
              "ExpansionZone": [["ExpansionPopup", "Description"], ["ExpansionPopup", "Image"], load_fake()["all"]],
              "Inn": [["Name", "Unlocal"], ["Icon", "BookIcon"], load_fake()["all"]],
              "MasterExpansionZone": [["Unlock", "UnavailableText"], ["Unlock", "UnavailableImage"],
                                      load_fake()["all"]],
              "PartySceneDecore": [["Name", "Unlocal"], ["Shop", "Icon"], load_fake()["decore"]],
              "Path": [["Name", "Unlocal"], ["Shop", "Icon"], load_fake()["all"]],
              "Pony": [["Name", "Unlocal"], ["Shop", "Icon"], load_fake()["pony"]],
              "Pony_House": [["Name", "Unlocal"], ["Shop", "Icon"], load_fake()["house"]],
              "PonyPart": [["PonyPart", "ModelName"], ["PonyPart", "Icon"], load_fake()["all"]],
              "PonySet": [["PonySet", "Localization"], ["PonySet", "Icon"], load_fake()["all"]],
              "ProfileAvatar": [["Shop", "Label"], ["Settings", "PictureActive"], load_fake()["all"]],
              "ProfileAvatarFrame": [["Shop", "Label"], ["Shop", "Icon"], load_fake()["all"]],
              "ProgressBooster": [["Shop", "Label"], ["Shop", "Icon"], load_fake()["all"]],
              "QuestSpecialItem": [["QuestSpecialItem", "Name"], ["QuestSpecialItem", "Icon"], load_fake()["all"]],
              "TapableContainer": [["UI", "TaskName"], ["UI", "Icon"], load_fake()["all"]],
              "Theme": [["Appearance", "Name"], ["Appearance", "Image"], load_fake()["all"]],
              "Totem": [["Name", "Unlocal"], ["Production", "ShopIcon"], load_fake()["all"]],
              "TravelersCafe": [["Name", "Unlocal"], ["Shop", "Icon"], load_fake()["house"]]}

DESCRIPTION = {"Consumable": "Расходный материал",
               "Decore": "Декор",
               "DestroyedHouse": "Разрушенные дома",
               "EquestriaGirls": "Девочки из Эквестрии",
               "ExpansionZone": "",
               "Inn": "",
               "MasterExpansionZone": "",
               "PartySceneDecore": "Праздничная сцена",
               "Path": "Дорожки",
               "Pony": "Персонажи",
               "Pony_House": "Магазины и дома",
               "PonyPart": "Костюмы",
               "PonySet": "Наборы костюмов",
               "ProfileAvatar": "Аватары",
               "ProfileAvatarFrame": "Рамки аватаров",
               "ProgressBooster": "Бустеры",
               "QuestSpecialItem": "Предметы квестов",
               "TapableContainer": "",
               "Theme": "Темы",
               "Totem": "Тотемы",
               "TravelersCafe": "Отель \"Золотая подкова\""}

FOLDERS = [["000_and_mlpextra_common"],
           ["000_and_mlpextra_pvr_common", "000_and_mlpextra_astc_pvr_common"],
           ["000_and_mlpextra_veryhigh", "000_and_mlpextra_astc_veryhigh"],
           ["000_and_mlpextra2_pvr_common", "000_and_mlpextra2_astc_pvr_common"],
           ["000_and_mlpextra2_veryhigh", "000_and_mlpextra2_astc_veryhigh"],
           ["000_and_mlpextragui_veryhigh/gui", "000_and_mlpextragui_astc_veryhigh/gui"],
           ["000_and_startup_common"],
           ["001_and_mlpdata_veryhigh", "001_and_mlpdata_astc_veryhigh"]]


def create_file_settings(data=None):
    try:
        print("0: Создание файла TABLEcreator.json.\n")
        
        with open(file="TABLEcreator.json",
                  mode="w") as settings_json:
            dump(obj=data or SETTINGS,
                 fp=settings_json,
                 indent=4)
        
        return data or SETTINGS
    except Exception:
        print("[ERROR] Во время создания файла настроек TABLEcreator.json возникла ошибка. "
              "Возможно нет прав на создания файлов.\n")
        
        return data or SETTINGS


def create_file_html(data):
    try:
        splash, trigger, index_html, i = "", True, {}, 1
        
        try:
            with open(file="000_and_startup_common/mlp_splash.png",
                      mode="rb") as mlp_splash_png:
                splash = b64encode(s=mlp_splash_png.read()).decode(encoding="UTF-8",
                                                                   errors="ignore")
        except Exception:
            print("[ERROR] Во время обработки файла 000_and_startup_common/mlp_splash.png возникла ошибка. "
                  "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
            
            trigger = False
        
        if not exists(path="TABLEcreator"):
            print(f"6: Создание папки TABLEcreator.\n")
            
            try:
                makedirs(name="TABLEcreator")
            except Exception:
                print(f"[ERROR] Во время создания папки TABLEcreator возникла ошибка. "
                      f"Возможно нет прав на создания папок.\n")
                
                trigger = False
        
        for cat in data:
            print(f"6: Создание файла TABLEcreator/{cat}.html.\n")
            
            try:
                with open(file=resource_path(file="template_files.html"),
                          mode="r",
                          encoding="UTF-8") as template_files_html:
                    html = template_files_html.read() % (dumps(obj=data[cat],
                                                               indent=4,
                                                               ensure_ascii=False), cat, cat, splash, "%")
                    
                    with open(file=f"TABLEcreator/{cat}.html",
                              mode="w",
                              encoding="UTF-8") as output_html:
                        output_html.write(html)
                    
                    index_html.update({i: {"img": data[cat][1]["img"],
                                           "page": f"{cat}.html",
                                           "desc": DESCRIPTION[cat],
                                           "size": f"{str(len(html) / 1024 / 1024)[:4]} МБ"}})
                
                i += 1
            except Exception:
                print(f"[WARNING] Во время создания файла TABLEcreator/{cat}.html возникла ошибка. "
                      f"Возможно нет прав на создания файлов. "
                      f"Файл пропущен.\n")
                
                trigger = False
        
        try:
            print("7: Создание файла TABLEcreator/index.html.\n")
            
            with open(file=resource_path(file="template_index.html"),
                      mode="r",
                      encoding="UTF-8") as template_index_html:
                with open(file="TABLEcreator/index.html",
                          mode="w",
                          encoding="UTF-8") as output_index_html:
                    output_index_html.write(template_index_html.read() % (dumps(obj=index_html,
                                                                                indent=4,
                                                                                ensure_ascii=False), splash, "%"))
        except Exception:
            print("[WARNING] Во время создания файла TABLEcreator/index.html возникла ошибка. "
                  "Возможно нет прав на создания файлов. "
                  "Файл пропущен.\n")
            
            trigger = False
        
        return trigger
    except Exception:
        print(f"[ERROR] Во время создания HTML файлов возникла ошибка. "
              f"Возможно нет прав на создания файлов.\n")
        
        return False


def load_file_settings():
    try:
        if exists(path="TABLEcreator.json"):
            print("1: Обработка файла TABLEcreator.json.\n")
            
            with open(file="TABLEcreator.json",
                      mode="r",
                      encoding="UTF-8") as settings_json:
                try:
                    data = loads(s=settings_json.read())
                    
                    if len(data) < len(SETTINGS):
                        print("[INFO] В файле настроек TABLEcreator.json отсутствуют некоторые параметры. "
                              "Эти параметры будут добавлены в файл со стандартными значениями.\n")
                        
                        for item in SETTINGS:
                            if item not in data:
                                data.update({item: SETTINGS[item]})
                        
                        return create_file_settings(data=data)
                    else:
                        return data
                except Exception:
                    print("[INFO] Не удалось прочитать файл настроек TABLEcreator.json. "
                          "Возможно данные в файле повреждены. "
                          "Будет создан новый файл со стандартными настройками.\n")
                    
                    return create_file_settings()
        else:
            print("[INFO] Файл настроек TABLEcreator.json не обнаружен. "
                  "Будет создан новый файл со стандартными настройками.\n")
            
            return create_file_settings()
    except Exception:
        print("[ERROR] Во время обработки файла настроек TABLEcreator.json возникла ошибка. "
              "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
        
        return SETTINGS


def load_russian_strings():
    current_file = ""
    
    try:
        if exists(path="000_and_startup_common/russian.txt"):
            current_file, russian_list = "russian.txt", {}
            
            print(f"2: Обработка файла 000_and_startup_common/{current_file}.\n")
            
            with open(file=f"000_and_startup_common/{current_file}",
                      mode="r",
                      encoding="UTF-8") as russian_file:
                for line in russian_file.readlines():
                    data = line.split("=")
                    
                    if len(data) == 2 and data[0] != "":
                        russian_list.update({data[0].strip(): data[1].strip()})
                
                return russian_list
        elif exists(path="000_and_startup_common/russian.json"):
            current_file = "russian.json"
            
            print(f"2: Обработка файла 000_and_startup_common/{current_file}.\n")
            
            with open(file=f"000_and_startup_common/{current_file}",
                      mode="r",
                      encoding="UTF-8") as russian_file:
                data = loads(s=russian_file.read())
                
                return data
        else:
            print("[ERROR] Отсутствует папка 000_and_startup_common или в ней нет файла russian.txt или russian.json. "
                  "Разархивируйте архив 000_and_startup_common.ark используя программу ARKdumper. "
                  "В настройках программы ARKdumper обязательно установите Convert = 1.\n")
            
            return None
    except Exception:
        print(f"[ERROR] Во время обработки файла 000_and_startup_common/{current_file} возникла ошибка. "
              f"Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
        
        return None


def load_english_strings():
    current_file = ""
    
    try:
        if exists(path="000_and_startup_common/english.txt"):
            current_file, english_list = "english.txt", {}
            
            print(f"3: Обработка файла 000_and_startup_common/{current_file}.\n")
            
            with open(file=f"000_and_startup_common/{current_file}",
                      mode="r",
                      encoding="UTF-8") as english_file:
                for line in english_file.readlines():
                    data = line.split("=")
                    
                    if len(data) == 2 and data[0] != "":
                        english_list.update({data[0].strip(): data[1].strip()})
                
                return english_list
        elif exists(path="000_and_startup_common/english.json"):
            current_file = "english.json"
            
            print(f"3: Обработка файла 000_and_startup_common/{current_file}.\n")
            
            with open(file=f"000_and_startup_common/{current_file}",
                      mode="r",
                      encoding="UTF-8") as english_file:
                data = loads(s=english_file.read())
                
                return data
        else:
            print("[ERROR] Отсутствует папка 000_and_startup_common или в ней нет файла english.txt или english.json. "
                  "Разархивируйте архив 000_and_startup_common.ark используя программу ARKdumper. "
                  "В настройках программы ARKdumper обязательно установите Convert = 1.\n")
            
            return None
    except Exception:
        print(f"[ERROR] Во время обработки файла 000_and_startup_common/{current_file} возникла ошибка. "
              f"Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
        
        return None


def load_image_folders():
    try:
        image_list, trigger = {}, True
        
        for folder in FOLDERS:
            if exists(path=folder[0]):
                print(f"4: Обработка папки {folder[0]}.\n")
                
                try:
                    for root, dirs, files in walk(top=folder[0]):
                        for file in files:
                            if file.endswith(".png"):
                                folder = root.replace("\\", "/")
                                
                                image_list.update({file: f"{folder}/{file}"})
                except Exception:
                    print(f"[ERROR] Во время обработки файлов в папке {folder[0]} возникла ошибка. "
                          f"Возможно файлы в папке повреждены или нет прав на чтение файлов.\n")
                    
                    trigger = False
            elif len(folder) == 2 and exists(path=folder[1]):
                print(f"4: Обработка папки {folder[1]}.\n")
                
                try:
                    for root, dirs, files in walk(top=folder[1]):
                        for file in files:
                            if file.endswith(".png"):
                                folder = root.replace("\\", "/")
                                
                                image_list.update({file: f"{folder}/{file}"})
                except Exception:
                    print(f"[ERROR] Во время обработки файлов в папке {folder[1]} возникла ошибка. "
                          f"Возможно файлы в папке повреждены или нет прав на чтение файлов.\n")
                    
                    trigger = False
            else:
                if len(folder) == 1:
                    print(f"[ERROR] Отсутствует папка {folder[0]} или в ней нет файлов. "
                          f"Разархивируйте архив {folder[0]}.ark используя программу ARKdumper. "
                          f"В настройках программы ARKdumper обязательно установите Convert = 1 и Split = 1.\n")
                else:
                    print(f"[ERROR] Отсутствуют папки {folder[0]} и {folder[1]} или в них нет файлов. "
                          f"Для работы программы нужна хотябы одна их них. "
                          f"Разархивируйте архив {folder[0]}.ark или {folder[1]}.ark используя программу ARKdumper. "
                          f"В настройках программы ARKdumper обязательно установите Convert = 1 и Split = 1.\n")
                
                trigger = False
        if trigger:
            return image_list
        else:
            return None
    except Exception:
        folders = ", ".join([", ".join(x) if len(x) == 2 else x[0] for x in FOLDERS])
        
        print(f"[ERROR] Во время обработки PNG файлов в папках {folders} возникла ошибка. "
              f"Возможно файлы в папках повреждены или нет прав на чтение файлов.\n")
        
        return None


def parse_gameobjectdata(settings, russian, english, images):
    try:
        all_data, trigger = {}, True
        
        if not exists(path="000_and_mlpextra_common/gameobjectdata.xml"):
            print("[ERROR] Отсутствует папка 000_and_mlpextra_common или в ней нет файла gameobjectdata.xml. "
                  "Разархивируйте архив 000_and_mlpextra_common.ark используя программу ARKdumper.\n")
            
            trigger = False
        
        if True not in settings.values():
            print("[ERROR] В файле настроек TABLEcreator.json не включен ни один параметр. "
                  "Для работы программы нужно включить хотя бы один.\n")
            
            trigger = False
        
        if trigger and russian is not None and english is not None and images is not None:
            print("5: Обработка файла 000_and_mlpextra_common/gameobjectdata.xml.")
            
            with open(file="000_and_mlpextra_common/gameobjectdata.xml",
                      mode="r",
                      encoding="UTF-8") as gameobjectdata_xml:
                soup = BeautifulSoup(markup=gameobjectdata_xml.read(),
                                     features="xml").find_all(name="GameObjects",
                                                              limit=1)[0]
                
                for cat in settings:
                    if settings[cat] and cat in CATEGORIES:
                        print(f"    Поиск всех {cat}...")
                        
                        try:
                            data, i = {}, 1
                            
                            for item in soup.find_all(name="Category",
                                                      attrs={"ID": cat},
                                                      limit=1)[0]:
                                if len(item) > 1:
                                    res_id, res_rus, res_eng, res_img = "", "", "", CATEGORIES[cat][2]
                                    
                                    try:
                                        res_id = item["ID"]
                                    except Exception:
                                        pass
                                    
                                    try:
                                        res_rus = russian[item.find_all(name=CATEGORIES[cat][0][0],
                                                                        limit=1)[0][CATEGORIES[cat][0][1]]]
                                    except Exception:
                                        pass
                                    
                                    try:
                                        res_eng = english[item.find_all(name=CATEGORIES[cat][0][0],
                                                                        limit=1)[0][CATEGORIES[cat][0][1]]]
                                    except Exception:
                                        pass
                                    
                                    try:
                                        image = item.find_all(name=CATEGORIES[cat][1][0],
                                                              limit=1)[0][CATEGORIES[cat][1][1]].replace("gui/", "")
                                        
                                        with open(file=images[image],
                                                  mode="rb") as image_file:
                                            res_img = b64encode(s=image_file.read()).decode(encoding="UTF-8",
                                                                                            errors="ignore")
                                    except Exception:
                                        pass
                                    
                                    if res_rus != "" or res_eng != "" or res_img != CATEGORIES[cat][2]:
                                        data.update({i: {"img": res_img,
                                                         "rus": res_rus,
                                                         "eng": res_eng,
                                                         "id": res_id}})
                                        
                                        i += 1
                            
                            all_data.update({cat: data})
                        except Exception:
                            print("")
                            
                            print(f"[WARNING] Во время обработки категории {cat} возникла ошибка. "
                                  f"Возможно данные в файле повреждены или нет прав на чтение файлов. "
                                  f"Категория пропущена.\n")
                            
                            trigger = False
                
                if len(all_data) > 0:
                    print("")
                    
                    trigger = create_file_html(data=all_data) if trigger else False
                
                return trigger
        else:
            return False
    except Exception:
        print("")
        
        print("[ERROR] Во время обработки файла 000_and_mlpextra_common/gameobjectdata.xml возникла ошибка. "
              "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
        
        return False


if __name__ == "__main__":
    try:
        if parse_gameobjectdata(settings=load_file_settings(),
                                russian=load_russian_strings(),
                                english=load_english_strings(),
                                images=load_image_folders()):
            exit()
        else:
            raise Exception
    except Exception:
        input()
        exit()
