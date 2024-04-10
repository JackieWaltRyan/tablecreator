import sys
from base64 import b64encode
from json import loads, dump, dumps
from os import walk, makedirs
from os.path import exists, join, abspath, dirname
from sys import exit
from traceback import format_exc

from bs4 import BeautifulSoup

from parsers import FUNCTIONS, DESCRIPTIONS

SETTINGS = {"Categories": {},
            "Lite": False}

FOLDERS = [["000_and_mlpextra_common"],
           ["000_and_mlpextra_pvr_common", "000_and_mlpextra_astc_pvr_common"],
           ["000_and_mlpextra_veryhigh", "000_and_mlpextra_astc_veryhigh"],
           ["000_and_mlpextra2_pvr_common", "000_and_mlpextra2_astc_pvr_common"],
           ["000_and_mlpextra2_veryhigh", "000_and_mlpextra2_astc_veryhigh"],
           ["000_and_mlpextragui_veryhigh/gui", "000_and_mlpextragui_astc_veryhigh/gui"],
           ["000_and_startup_common"],
           ["001_and_mlpdata_veryhigh", "001_and_mlpdata_astc_veryhigh"]]


def resource_path(file):
    try:
        return join(getattr(sys,
                            "_MEIPASS",
                            dirname(p=abspath(path=__file__))),
                    file)
    except Exception:
        print(format_exc())


def load_fake():
    try:
        with open(file=resource_path(file="fake.json"),
                  mode="r",
                  encoding="UTF-8") as fake_json:
            return loads(s=fake_json.read())
    except Exception:
        print(format_exc())


def create_file_settings(data=None):
    try:
        print("0: Создание файла TABLEcreator.json.\n")

        with open(file="TABLEcreator.json",
                  mode="w") as settings_json:
            dump(obj=(data or SETTINGS),
                 fp=settings_json,
                 indent=4)

        return data or SETTINGS
    except Exception:
        print("[ERROR] Во время создания файла настроек TABLEcreator.json возникла ошибка. "
              "Возможно нет прав на создания файлов.\n")

        return data or SETTINGS


def load_file_settings():
    try:
        functions = sorted(FUNCTIONS,
                           key=lambda x: x.lower())

        for cat in functions:
            SETTINGS["Categories"].update({cat: True})

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

                        data = create_file_settings(data=data)

                    if len(data["Categories"]) < len(SETTINGS["Categories"]):
                        print("[INFO] В файле настроек TABLEcreator.json отсутствуют некоторые параметры. "
                              "Эти параметры будут добавлены в файл со стандартными значениями.\n")

                        for item in SETTINGS["Categories"]:
                            if item not in data["Categories"]:
                                data["Categories"].update({item: SETTINGS["Categories"][item]})

                        data = create_file_settings(data=data)

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

                    if (len(data) == 2) and data[0].strip():
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

                    if (len(data) == 2) and data[0].strip():
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


def find_image_files():
    try:
        image_list, trigger = {}, True

        for folder in FOLDERS:
            if exists(path=folder[0]):
                print(f"4: Обработка папки {folder[0]}.\n")

                try:
                    for (root, dirs, files) in walk(top=folder[0]):
                        for file in files:
                            if file.endswith(".png"):
                                folder = root.replace("\\",
                                                      "/")

                                image_list.update({file.replace(".png",
                                                                ""): f"{folder}/{file}"})
                except Exception:
                    print(f"[ERROR] Во время обработки файлов в папке {folder[0]} возникла ошибка. "
                          f"Возможно файлы в папке повреждены или нет прав на чтение файлов.\n")

                    trigger = False
            elif (len(folder) == 2) and exists(path=folder[1]):
                print(f"4: Обработка папки {folder[1]}.\n")

                try:
                    for (root, dirs, files) in walk(top=folder[1]):
                        for file in files:
                            if file.endswith(".png"):
                                folder = root.replace("\\",
                                                      "/")

                                image_list.update({file.replace(".png",
                                                                ""): f"{folder}/{file}"})
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
        folders = ", ".join([(", ".join(x) if (len(x) == 2) else x[0]) for x in FOLDERS])

        print(f"[ERROR] Во время обработки PNG файлов в папках {folders} возникла ошибка. "
              f"Возможно файлы в папках повреждены или нет прав на чтение файлов.\n")

        return None


def parse_mapzones():
    try:
        mapzones_list = {}

        if exists(path="000_and_startup_common/mapzones.xml"):
            print("5: Обработка файла 000_and_startup_common/mapzones.xml.\n")

            with open(file="000_and_startup_common/mapzones.xml",
                      mode="r",
                      encoding="UTF-8") as mapzones_xml:
                soup = BeautifulSoup(markup=mapzones_xml.read(),
                                     features="xml").find_all(name="World",
                                                              limit=1)[0]

                for item in soup.find_all(name="MapZone"):
                    mapzones_list.update({item["ID"]: item.find_all(name="UI",
                                                                    limit=1)[0].find_all(name="flash",
                                                                                         limit=1)[0]["zoneNameString"]})

                return mapzones_list
        else:
            print("[ERROR] Отсутствует папка 000_and_startup_common или в ней нет файла mapzones.xml. "
                  "Разархивируйте архив 000_and_startup_common.ark используя программу ARKdumper. "
                  "В настройках программы ARKdumper обязательно установите Convert = 1.\n")

            return None
    except Exception:
        print("[ERROR] Во время обработки файла 000_and_startup_common/mapzones.xml возникла ошибка. "
              "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")

        return None


def parse_shopdata():
    try:
        shopdata_list = {}

        if exists(path="000_and_startup_common/shopdata.xml"):
            print("6: Обработка файла 000_and_startup_common/shopdata.xml.\n")

            with open(file="000_and_startup_common/shopdata.xml",
                      mode="r",
                      encoding="UTF-8") as shopdata_xml:
                soup = BeautifulSoup(markup=shopdata_xml.read(),
                                     features="xml").find_all(name="ShopItemData",
                                                              limit=1)[0]

                for sic in soup.find_all(name="ShopItemCategory"):
                    for item in sic.find_all(name="ShopItem"):
                        unlockvalue, currencytype, cost, mapzone = None, None, None, None

                        try:
                            unlockvalue = item["UnlockValue"]
                        except Exception:
                            pass

                        try:
                            currencytype = item["CurrencyType"]
                        except Exception:
                            pass

                        try:
                            cost = item["Cost"]
                        except Exception:
                            pass

                        try:
                            if item["MapZone"] != "-1":
                                mapzone = item["MapZone"].replace(" ",
                                                                  "").split(",")
                        except Exception:
                            pass

                        shopdata_list.update({item["ID"]: {"UnlockValue": unlockvalue,
                                                           "CurrencyType": currencytype,
                                                           "Cost": cost,
                                                           "MapZone": mapzone}})

                return shopdata_list
        else:
            print("[ERROR] Отсутствует папка 000_and_startup_common или в ней нет файла shopdata.xml. "
                  "Разархивируйте архив 000_and_startup_common.ark используя программу ARKdumper. "
                  "В настройках программы ARKdumper обязательно установите Convert = 1.\n")

            return None
    except Exception:
        print("[ERROR] Во время обработки файла 000_and_startup_common/shopdata.xml возникла ошибка. "
              "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")

        return None


def create_files_html(data):
    try:
        splash, trigger, index_html, i = "", True, {}, 1

        try:
            with open(file="000_and_startup_common/mlp_splash.png",
                      mode="rb") as mlp_splash_png:
                splash = b64encode(s=mlp_splash_png.read()).decode(encoding="UTF-8",
                                                                   errors="ignore")
        except Exception:
            print("[WARNING] Во время обработки файла 000_and_startup_common/mlp_splash.png возникла ошибка. "
                  "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")

            trigger = False

        if not exists(path="TABLEcreator"):
            print(f"8: Создание папки TABLEcreator.\n")

            try:
                makedirs(name="TABLEcreator")
            except Exception:
                print(f"[ERROR] Во время создания папки TABLEcreator возникла ошибка. "
                      f"Возможно нет прав на создания папок.\n")

                trigger = False

        for cat in data:
            print(f"9: Создание файла TABLEcreator/{cat}.html.\n")

            try:
                with open(file=resource_path(file="template/template.html"),
                          mode="r",
                          encoding="UTF-8") as template_file_html:
                    html = template_file_html.read()

                    with open(file=resource_path(file="template/template.css"),
                              mode="r",
                              encoding="UTF-8") as template_file_css:
                        css = template_file_css.read()

                        with open(file=resource_path(file="template/template.js"),
                                  mode="r",
                                  encoding="UTF-8") as template_file_js:
                            js = template_file_js.read()

                            html = html.replace("{{ data }}",
                                                dumps(obj=data[cat],
                                                      indent=4,
                                                      ensure_ascii=False))
                            html = html.replace("{{ cat }}",
                                                f"Список {cat}")
                            html = html.replace("{{ icon }}",
                                                data[cat][1]["Изображение"][0])
                            html = html.replace("{{ style }}",
                                                css)
                            html = html.replace("{{ script }}",
                                                js)
                            html = html.replace("{{ splash }}",
                                                splash)

                            with open(file=f"TABLEcreator/{cat}.html",
                                      mode="w",
                                      encoding="UTF-8") as output_html:
                                output_html.write(html)

                            index_html.update({i: {"Изображение": data[cat][1]["Изображение"],
                                                   "Страница": f"{cat}.html",
                                                   "Описание": DESCRIPTIONS[cat],
                                                   "Размер": f"{int(len(html) / 1024 / 1024)} МБ"}})

                i += 1
            except Exception:
                print(f"[WARNING] Во время создания файла TABLEcreator/{cat}.html возникла ошибка. "
                      f"Возможно нет прав на создания файлов. "
                      f"Файл пропущен.\n")

                trigger = False

        try:
            print("10: Создание файла TABLEcreator/index.html.\n")

            with open(file=resource_path(file="template/template.html"),
                      mode="r",
                      encoding="UTF-8") as template_file_html:
                html = template_file_html.read()

                with open(file=resource_path(file="template/template.css"),
                          mode="r",
                          encoding="UTF-8") as template_file_css:
                    css = template_file_css.read()

                    with open(file=resource_path(file="template/template.js"),
                              mode="r",
                              encoding="UTF-8") as template_file_js:
                        js = template_file_js.read()

                        html = html.replace("{{ data }}",
                                            dumps(obj=index_html,
                                                  indent=4,
                                                  ensure_ascii=False))
                        html = html.replace("{{ cat }}",
                                            "Список всех таблиц")
                        html = html.replace("{{ icon }}",
                                            index_html[1]["Изображение"][0])
                        html = html.replace("{{ style }}",
                                            css)
                        html = html.replace("{{ script }}",
                                            js)
                        html = html.replace("{{ splash }}",
                                            splash)

                        with open(file="TABLEcreator/index.html",
                                  mode="w",
                                  encoding="UTF-8") as output_index_html:
                            output_index_html.write(html)
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


def parse_gameobjectdata(settings, russian, english, images, mapzones, shopdata, fake):
    try:
        trigger, all_data = True, {}

        if not exists(path="000_and_mlpextra_common/gameobjectdata.xml"):
            print("[ERROR] Отсутствует папка 000_and_mlpextra_common или в ней нет файла gameobjectdata.xml. "
                  "Разархивируйте архив 000_and_mlpextra_common.ark используя программу ARKdumper.\n")

            trigger = False

        if True not in settings["Categories"].values():
            print("[ERROR] В файле настроек TABLEcreator.json не включен ни один параметр. "
                  "Для работы программы нужно включить хотя бы один.\n")

            trigger = False

        if trigger and russian and english and images and mapzones and shopdata:
            print("7: Обработка файла 000_and_mlpextra_common/gameobjectdata.xml.\n")

            with open(file="000_and_mlpextra_common/gameobjectdata.xml",
                      mode="r",
                      encoding="UTF-8") as gameobjectdata_xml:
                soup = BeautifulSoup(markup=gameobjectdata_xml.read(),
                                     features="xml").find_all(name="GameObjects",
                                                              limit=1)[0]

                for cat in settings["Categories"]:
                    if settings["Categories"][cat] and (cat in SETTINGS["Categories"]):
                        print(f"    Поиск всех {cat}...")

                        try:
                            data, i, ii, items = {}, 1, 1, soup.find_all(name="Category",
                                                                         attrs={"ID": cat},
                                                                         limit=1)[0]

                            for item in items:
                                print(f"\r        Обработано {ii} из {len(items)}.",
                                      end="")

                                if len(item) > 1:
                                    res = FUNCTIONS[cat](item=item,
                                                         russian=russian,
                                                         english=english,
                                                         images=images,
                                                         mapzones=mapzones,
                                                         shopdata=shopdata,
                                                         fake=fake,
                                                         lite=settings["Lite"])

                                    if res:
                                        res.update({"ID": item["ID"]})

                                        data.update({i: res})

                                        i += 1

                                ii += 1

                            all_data.update({cat: data})

                            print("")
                        except Exception:
                            print(f"[WARNING] Во время обработки категории {cat} возникла ошибка. "
                                  f"Возможно данные в файле повреждены или нет прав на чтение файлов. "
                                  f"Категория пропущена.\n")

                            trigger = False

                        print("")

                if len(all_data) > 0:
                    trigger = (create_files_html(data=all_data) if trigger else False)

                return trigger
        else:
            return False
    except Exception:
        print("[ERROR] Во время обработки файла 000_and_mlpextra_common/gameobjectdata.xml возникла ошибка. "
              "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")

        return False


if __name__ == "__main__":
    try:
        if parse_gameobjectdata(settings=load_file_settings(),
                                russian=load_russian_strings(),
                                english=load_english_strings(),
                                images=find_image_files(),
                                mapzones=parse_mapzones(),
                                shopdata=parse_shopdata(),
                                fake=load_fake()):
            exit()
        else:
            raise Exception
    except Exception:
        input()
        exit()
