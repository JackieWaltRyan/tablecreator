import sys
from base64 import b64encode
from os.path import join, abspath, dirname

DATA = {}


def resource_path(file):
    try:
        return join(getattr(sys,
                            "_MEIPASS",
                            dirname(p=abspath(path=__file__))),
                    file)
    except Exception:
        return file


def seconds_to_time(s):
    try:
        sec = int(float(s))

        seconds = (sec % 60)
        minutes = (int(sec / 60) % 60)
        hours = int(sec / 3600)

        minutes_string = str(minutes).zfill(2)
        seconds_string = str(seconds).zfill(2)

        return f"{hours}:{minutes_string}:{seconds_string}" if (hours > 0) else f"{minutes_string}:{seconds_string}"
    except Exception:
        return "--:--"


def view_size(data):
    try:
        bb = int(len(data))
        kb = int(bb / 1024)
        mb = int(kb / 1024)
        gb = int(mb / 1024)

        return f"{bb} Б" if not kb else (f"{kb} КБ" if not mb else (f"{mb} МБ" if not gb else f"{gb} ГБ"))
    except Exception:
        return "--"


def load_fake(file, category):
    try:
        with open(file=resource_path(file=f"fake/{file}.png"),
                  mode="rb") as fake_file:
            if DATA["settings"]["Hosting"]:
                if "hosting" not in DATA:
                    DATA.update({"hosting": {category: {f"fake_{file}.png": fake_file.read()}}})
                else:
                    if category not in DATA["hosting"]:
                        DATA["hosting"].update({category: {f"fake_{file}.png": fake_file.read()}})
                    else:
                        DATA["hosting"][category].update({f"fake_{file}.png": fake_file.read()})

                return f"fake_{file}.png"
            else:
                b64data = b64encode(s=fake_file.read()).decode(encoding="UTF-8",
                                                               errors="ignore")

                return f"data:image/png;base64, {b64data}"
    except Exception:
        return None


def load_image(image, category):
    try:
        image = image.replace("gui/",
                              "").replace(".png",
                                          "")

        with open(file=DATA["images"][image],
                  mode="rb") as image_file:
            if DATA["settings"]["Hosting"]:
                if "hosting" not in DATA:
                    DATA.update({"hosting": {category: {f"{image}.png": image_file.read()}}})
                else:
                    if category not in DATA["hosting"]:
                        DATA["hosting"].update({category: {f"{image}.png": image_file.read()}})
                    else:
                        DATA["hosting"][category].update({f"{image}.png": image_file.read()})

                return f"{image}.png"
            else:
                b64data = b64encode(s=image_file.read()).decode(encoding="UTF-8",
                                                                errors="ignore")

                return f"data:image/png;base64, {b64data}"
    except Exception:
        return None
