from utils import DATA, load_fake, load_image, seconds_to_time

FUNCTIONS = {}

CURRENCY = {"1": "Битсы",
            "2": "Камни",
            "3": "Сердца"}

ELEMENTS = {"Magic": "Элемент Магии",
            "Loyalty": "Элемент Верности",
            "Laughter": "Элемент Радости",
            "Kindness": "Элемент Доброты",
            "Generosity": "Элемент Щедрости",
            "Honesty": "Элемент Честности"}

BONUS = {"ShopProduction": "Магазины",
         "MiniGames": "Мини игры",
         "MineCart": "Шахта"}

POP = {"Mane": "Грива",
       "Body": "Тело",
       "Tail": "Хвост"}

INGREDIENTS = {1: "Булавки",
               2: "Пуговицы",
               3: "Нитки",
               4: "Ленточки",
               5: "Бабочки"}

CONSUMES = {"XP": "Опыт",
            "SoftCoins": "Битсы",
            "Coins": "Битсы",
            "Gems": "Камни",
            "MinecartWheel": "Колеса"}


class Parser:
    def __init__(self, category, description=""):
        self.category = category
        self.description = description

        if "descriptions" not in DATA:
            DATA.update({"descriptions": {self.category: self.description}})
        else:
            DATA["descriptions"].update({self.category: self.description})

    def __call__(self, function):
        FUNCTIONS.update({self.category: function})

        def decorator(item, category=self.category):
            return function(item, category)

        return decorator


@Parser(category="PonyPet",
        description="Питомцы")
def ponypet(item, category):
    try:
        res_icon, res_image = load_fake(file="all",
                                        category=category), load_fake(file="all",
                                                                      category=category)
        res_name_rus, res_name_eng = "", ""
        res_owner, res_bonus, res_distance, res_time, res_additionally = "", [], [], "", []
        res_sity, res_level, res_cost = [], "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Shop",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="PetUniqueIcon",
                                                   limit=1)[0]["Icon"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            unique = item.find_all(name="Settings",
                                   limit=1)[0]["IsUnique"]

            if unique == "1":
                res_additionally.append("Персональный")
        except Exception:
            pass

        try:
            res_owner = item.find_all(name="Settings",
                                      limit=1)[0]["PonyUniqueID"]
        except Exception:
            pass

        try:
            flying = item.find_all(name="Settings",
                                   limit=1)[0]["IsFlying"]

            if flying == "1":
                res_additionally.append("Летающий")
        except Exception:
            pass

        try:
            game_bonus = item.find_all(name="Settings",
                                       limit=1)[0]["GameBonus"]

            res_bonus.append(f"Шахта: +{game_bonus}%")
        except Exception:
            pass

        try:
            task_bonus = item.find_all(name="Settings",
                                       limit=1)[0]["TaskBonus"]

            res_bonus.append(f"Задания: -{task_bonus}%")
        except Exception:
            pass

        try:
            distance_go = item.find_all(name="Settings",
                                        limit=1)[0]["DistanceGoToPony"]

            res_distance.append(f"До пони: {distance_go}")
        except Exception:
            pass

        try:
            distance_out = item.find_all(name="Settings",
                                         limit=1)[0]["DistanceGoOutFromPony"]

            res_distance.append(f"От пони: {distance_out}")
        except Exception:
            pass

        try:
            res_time = item.find_all(name="Settings",
                                     limit=1)[0]["IdleWalkTime"]
        except Exception:
            pass

        # shopdata:
        try:
            for mz in DATA["shopdata"][item["ID"]]["MapZone"]:
                try:
                    res_sity.append(DATA["russian"][DATA["mapzones"][mz]].title())
                except Exception:
                    pass
        except Exception:
            pass

        try:
            res_level = DATA["shopdata"][item["ID"]]["UnlockValue"]
        except Exception:
            pass

        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Владелец": res_owner,
                    "Бонус": (res_bonus if (len(res_bonus) > 0) else [""]),
                    "Расстояние": (res_distance if (len(res_distance) > 0) else [""]),
                    "Время простоя": res_time,
                    "Дополнительно": (res_additionally if (len(res_additionally) > 0) else [""]),
                    "Город": (res_sity if (len(res_sity) > 0) else [""]),
                    "Уровень открытия": res_level,
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="ProfileAvatarFrame",
        description="Рамки аватаров")
def profileavatarframe(item, category):
    try:
        res_icon, res_image = load_fake(file="all",
                                        category=category), load_fake(file="all",
                                                                      category=category)
        res_name_rus, res_name_eng = "", ""
        res_cost = ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Shop",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="Settings",
                                                   limit=1)[0]["PictureActive"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        # shopdata:
        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="ProfileAvatar",
        description="Аватары")
def profileavatar(item, category):
    try:
        res_icon, res_image = load_fake(file="all",
                                        category=category), load_fake(file="all",
                                                                      category=category)
        res_name_rus, res_name_eng = "", ""
        res_pony, res_cost = "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Shop",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="Settings",
                                                   limit=1)[0]["PictureActive"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        try:
            res_pony = item.find_all(name="Settings",
                                     limit=1)[0]["PonyStarsID"]
        except Exception:
            pass

        # shopdata:
        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "За звезды пони": res_pony,
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="ProgressBooster",
        description="Бустеры")
def progressbooster(item, category):
    try:
        res_icon = load_fake(file="all",
                             category=category)
        res_name_rus, res_name_eng = "", ""
        res_type, res_time, res_multiplier, res_cost = "", "", "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Shop",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        try:
            btype = item.find_all(name="Settings",
                                  limit=1)[0]["Type"]

            res_type = ("Опыт" if (btype == "0") else "Битсы")
        except Exception:
            pass

        try:
            btime = item.find_all(name="Settings",
                                  limit=1)[0]["Time"]

            res_time = seconds_to_time(s=btime)
        except Exception:
            pass

        try:
            multiplier = item.find_all(name="Settings",
                                       limit=1)[0]["Multiplier"]

            res_multiplier = f"x{multiplier}"
        except Exception:
            pass

        # shopdata:
        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Тип": res_type,
                    "Время": res_time,
                    "Множитель": res_multiplier,
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="Totem",
        description="Тотемы")
def totem(item, category):
    try:
        res_icon, res_image = load_fake(file="all",
                                        category=category), load_fake(file="all",
                                                                      category=category)
        res_name_rus, res_name_eng = "", ""
        res_desc_rus, res_desc_eng = "", ""
        res_size, res_spawn, res_elements, res_production, res_mixing = "", "", [], [], []
        res_ingredients, res_clearing, res_cost = [], [], ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Production",
                                                  limit=1)[0]["ShopIcon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="Production",
                                                   limit=1)[0]["ProductIcon"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_desc_rus = DATA["russian"][item.find_all(name="Description",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_desc_eng = DATA["english"][item.find_all(name="Description",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            size = int(int(item.find_all(name="GridData",
                                         limit=1)[0]["Size"]) / 2)

            res_size = f"{size}x{size}"
        except Exception:
            pass

        try:
            el_min = item.find_all(name="Elements",
                                   limit=1)[0]["Element_Spawn_Min"]
            el_max = item.find_all(name="Elements",
                                   limit=1)[0]["Element_Spawn_Max"]

            res_spawn = f"{el_min}-{el_max}"
        except Exception:
            pass

        try:
            for el in ELEMENTS:
                try:
                    count = item.find_all(name="Elements",
                                          limit=1)[0][el]

                    if count != "0":
                        res_elements.append(f"{ELEMENTS[el]}: {count}%")
                except Exception:
                    pass
        except Exception:
            pass

        try:
            mtime = item.find_all(name="Production",
                                  limit=1)[0]["Mixing_Time"]

            res_mixing.append(f"Время: {seconds_to_time(s=mtime)}")
        except Exception:
            pass

        try:
            mskip = item.find_all(name="Production",
                                  limit=1)[0]["Mixing_SkipCost"]

            res_mixing.append(f"Пропуск: Камни: {mskip}")
        except Exception:
            pass

        try:
            ptime = item.find_all(name="Production",
                                  limit=1)[0]["Production_Time"]

            res_production.append(f"Время: {seconds_to_time(s=ptime)}")
        except Exception:
            pass

        try:
            pskip = item.find_all(name="Production",
                                  limit=1)[0]["Production_Skip"]

            res_production.append(f"Пропуск: Камни: {pskip}")
        except Exception:
            pass

        try:
            for ing in ["Ingredient_A", "Ingredient_B", "Ingredient_C"]:
                try:
                    ingred = item.find_all(name="Production",
                                           limit=1)[0][ing]

                    res_ingredients.append(ingred)
                except Exception:
                    pass
        except Exception:
            pass

        try:
            ccost = item.find_all(name="Clearing",
                                  limit=1)[0]["Clearing_Start_Cost"]

            res_clearing.append(f"Стоимость: Битсы: {ccost}")
        except Exception:
            pass

        try:
            ctime = item.find_all(name="Clearing",
                                  limit=1)[0]["Clearing_Time"]

            res_clearing.append(f"Время: {seconds_to_time(s=ctime)}")
        except Exception:
            pass

        try:
            cskip = item.find_all(name="Clearing",
                                  limit=1)[0]["Clearing_Skip_Cost"]

            res_clearing.append(f"Пропуск: Камни: {cskip}")
        except Exception:
            pass

        # shopdata:
        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_icon, res_image] if (res_image != res_icon) else [res_icon]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": ([res_icon, res_image] if (res_image != res_icon) else [res_icon]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Описание": ([res_desc_rus, res_desc_eng] if (res_desc_rus != res_desc_eng) else [res_desc_rus]),
                    "Размер": res_size,
                    "Количество элементов": res_spawn,
                    "Шанс выпадения": (res_elements if (len(res_elements) > 0) else [""]),
                    "Создание": (res_mixing if (len(res_mixing) > 0) else [""]),
                    "Сбор": (res_production if (len(res_production) > 0) else [""]),
                    "Ингредиенты": (res_ingredients if (len(res_ingredients) > 0) else [""]),
                    "Уборка": (res_clearing if (len(res_clearing) > 0) else [""]),
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="Ingredient",
        description="Ингредиенты")
def ingredient(item, category):
    try:
        res_icon = load_fake(file="all",
                             category=category)
        res_name_eng = ""
        res_level, res_cost = "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Production",
                                                  limit=1)[0]["IconProductFrame"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_name_eng = item.find_all(name="Name",
                                         limit=1)[0]["Unlocal"]
        except Exception:
            pass

        # shopdata:
        try:
            res_level = DATA["shopdata"][item["ID"]]["UnlockValue"]
        except Exception:
            pass

        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Имя": [res_name_eng]}
        else:
            return {"Изображение": [res_icon],
                    "Имя": [res_name_eng],
                    "Уровень открытия": res_level,
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="Theme",
        description="Темы")
def theme(item, category):
    try:
        res_icon = load_fake(file="all",
                             category=category)
        res_name_rus, res_name_eng = "", ""
        res_music, res_bonus, res_season, res_weather = "", "", "", ""
        res_sity, res_level, res_cost = [], "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Appearance",
                                                  limit=1)[0]["Image"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Appearance",
                                                         limit=1)[0]["Name"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Appearance",
                                                         limit=1)[0]["Name"]]
        except Exception:
            pass

        try:
            music = item.find_all(name="MaterialsOverride",
                                  limit=1)[0]["Music"]

            res_music = ("Да" if music else "")
        except Exception:
            pass

        try:
            bonus = item.find_all(name="Bonus",
                                  limit=1)[0]["ShopInCome"]

            if bonus != "0":
                res_bonus = f"+{bonus}%"
        except Exception:
            pass

        try:
            res_season = item.find_all(name="Appearance",
                                       limit=1)[0]["Season"]
        except Exception:
            pass

        try:
            res_weather = item.find_all(name="Appearance",
                                        limit=1)[0]["Weather"]
        except Exception:
            pass

        # shopdata:
        try:
            for mz in DATA["shopdata"][item["ID"]]["MapZone"]:
                try:
                    res_sity.append(DATA["russian"][DATA["mapzones"][mz]].title())
                except Exception:
                    pass
        except Exception:
            pass

        try:
            res_level = DATA["shopdata"][item["ID"]]["UnlockValue"]
        except Exception:
            pass

        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Музыка": res_music,
                    "Бонус": res_bonus,
                    "Сезон": res_season,
                    "Погода": res_weather,
                    "Город": (res_sity if (len(res_sity) > 0) else [""]),
                    "Уровень открытия": res_level,
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="Decore",
        description="Декорации")
def decore(item, category):
    try:
        res_icon = load_fake(file="decore",
                             category=category)
        res_name_rus, res_name_eng = "", ""
        res_pro, res_pro_bonus = "", []
        res_size, res_consume, res_xp = "", [], ""
        res_sity, res_level, res_cost = [], "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Shop",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            size = int(int(item.find_all(name="GridData",
                                         limit=1)[0]["Size"]) / 2)

            res_size = f"{size}x{size}"
        except Exception:
            pass

        try:
            pro = item.find_all(name="ProDecoration",
                                limit=1)[0]["IsProDecore"]

            res_pro = ("Да" if (pro == "1") else "")
        except Exception:
            pass

        try:
            bonus_time = item.find_all(name="ProDecoration",
                                       limit=1)[0]["TimeBonusPercent"]

            if bonus_time != "0":
                res_pro_bonus.append(f"Время: -{bonus_time}%")
        except Exception:
            pass

        try:
            bonus_bits = item.find_all(name="ProDecoration",
                                       limit=1)[0]["BitsBonusPercent"]

            if bonus_bits != "0":
                res_pro_bonus.append(f"Монеты: +{bonus_bits}%")
        except Exception:
            pass

        try:
            size_pro = item.find_all(name="ProDecoration",
                                     limit=1)[0]["GridSizeBonus"]

            if res_pro == "Да":
                res_pro_bonus.append(f"Размер: {size_pro}x{size_pro}")
        except Exception:
            pass

        try:
            ocs = item.find_all(name="OnPurchase",
                                limit=1)[0]["EarnXP"]

            if ocs != "0":
                res_xp = ocs
        except Exception:
            pass

        try:
            cda = item.find_all(name="TouchFeedback",
                                limit=1)[0]["CoinDropAmount"]

            if cda != "0":
                cdc = item.find_all(name="TouchFeedback",
                                    limit=1)[0]["CoinDropChance"]

                res_consume.append(f"Монеты: {cda}, Шанс: {cdc}")
        except Exception:
            pass

        try:
            mwda = item.find_all(name="TouchFeedback",
                                 limit=1)[0]["MinecartWheelDropAmount"]

            if mwda != "0":
                mwdc = item.find_all(name="TouchFeedback",
                                     limit=1)[0]["MinecartWheelDropChance"]

                res_consume.append(f"Колеса: {mwda}, Шанс: {mwdc}")
        except Exception:
            pass

        try:
            if len(res_consume) > 0:
                ntd = item.find_all(name="TouchFeedback",
                                    limit=1)[0]["NextTouchDelay"]

                res_consume.append(f"Задержка: {ntd}")
        except Exception:
            pass

        # shopdata:
        try:
            for mz in DATA["shopdata"][item["ID"]]["MapZone"]:
                try:
                    res_sity.append(DATA["russian"][DATA["mapzones"][mz]].title())
                except Exception:
                    pass
        except Exception:
            pass

        try:
            res_level = DATA["shopdata"][item["ID"]]["UnlockValue"]
        except Exception:
            pass

        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Размер": res_size,
                    "Супердекор": res_pro,
                    "Бонусы супердекора": (res_pro_bonus if (len(res_pro_bonus) > 0) else [""]),
                    "Бонусы": (res_consume if (len(res_consume) > 0) else [""]),
                    "Опыт за покупку": res_xp,
                    "Город": (res_sity if (len(res_sity) > 0) else [""]),
                    "Уровень открытия": res_level,
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="Pony_House",
        description="Дома и Магазины")
def pony_house(item, category):
    try:
        res_icon, res_image = load_fake(file="house",
                                        category=category), load_fake(file="house",
                                                                      category=category)
        res_name_rus, res_name_eng = "", ""
        res_size, res_construction, res_type, res_visitors, res_consumable, res_spawn = "", [], "", [], "", ""
        res_elements, res_xp, res_additionally = [], [], []
        res_sity, res_level, res_cost = [], "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Icon",
                                                  limit=1)[0]["BookIcon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="Shop",
                                                   limit=1)[0]["Icon"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            size = int(int(item.find_all(name="GridData",
                                         limit=1)[0]["Size"]) / 2)

            res_size = f"{size}x{size}"
        except Exception:
            pass

        try:
            c_time = item.find_all(name="Construction",
                                   limit=1)[0]["ConstructionTime"]

            res_construction.append(f"Время: {seconds_to_time(s=c_time)}")
        except Exception:
            pass

        try:
            c_skip = item.find_all(name="Construction",
                                   limit=1)[0]["SkipCost"]

            res_construction.append(f"Пропуск: Камни: {c_skip}")
        except Exception:
            pass

        try:
            shop = item.find_all(name="ShopModule",
                                 limit=1)[0]["IsAShop"]

            res_type = ("Магазин" if (shop == "1") else "Дом")
        except Exception:
            pass

        try:
            for p_vis in item.find_all(name="Visitors",
                                       limit=1)[0].find_all(name="Ponies",
                                                            limit=1)[0]:
                try:
                    if p_vis["Value"]:
                        res_visitors.append(p_vis["Value"])
                except Exception:
                    pass
        except Exception:
            pass

        try:
            res_consumable = item.find_all(name="ShopModule",
                                           limit=1)[0]["Consumable_A"]
        except Exception:
            pass

        try:
            el_min = item.find_all(name="Elements",
                                   limit=1)[0]["Element_Spawn_Min"]
            el_max = item.find_all(name="Elements",
                                   limit=1)[0]["Element_Spawn_Max"]

            res_spawn = f"{el_min}-{el_max}"
        except Exception:
            pass

        try:
            count = item.find_all(name="Elements",
                                  limit=1)[0]["Nothing"]

            if count != "0":
                res_elements.append(f"Ничего: {count}%")
        except Exception:
            pass

        try:
            for el in ELEMENTS:
                try:
                    count = item.find_all(name="Elements",
                                          limit=1)[0][el]

                    if count != "0":
                        res_elements.append(f"{ELEMENTS[el]}: {count}%")
                except Exception:
                    pass
        except Exception:
            pass

        try:
            xp_complete = item.find_all(name="XP",
                                        limit=1)[0]["OnConstructionComplete"]

            if xp_complete != "0":
                res_xp.append(f"За постройку: {xp_complete}")
        except Exception:
            pass

        try:
            xp_start = item.find_all(name="XP",
                                     limit=1)[0]["OnConstructionStarted"]

            if xp_start != "0":
                res_xp.append(f"За покупку: {xp_start}")
        except Exception:
            pass

        try:
            edit = item.find_all(name="EditMode",
                                 limit=1)[0]["IsAvailable"]

            if edit == "0":
                res_additionally.append("Нельзя переместить")
        except Exception:
            pass

        try:
            sell = item.find_all(name="Sell",
                                 limit=1)[0]["CanSell"]

            if sell == "1":
                res_additionally.append("Можно продать")
        except Exception:
            pass

        # shopdata:
        try:
            for mz in DATA["shopdata"][item["ID"]]["MapZone"]:
                try:
                    res_sity.append(DATA["russian"][DATA["mapzones"][mz]].title())
                except Exception:
                    pass
        except Exception:
            pass

        try:
            res_level = DATA["shopdata"][item["ID"]]["UnlockValue"]
        except Exception:
            pass

        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Размер": res_size,
                    "Строительство": (res_construction if (len(res_construction) > 0) else [""]),
                    "Тип": res_type,
                    "Гости": (res_visitors if (len(res_visitors) > 0) else [""]),
                    "Товар": res_consumable,
                    "Количество элементов": (res_spawn if (len(res_spawn) > 0) else [""]),
                    "Шанс выпадения": (res_elements if (len(res_elements) > 0) else [""]),
                    "Опыт": (res_xp if (len(res_xp) > 0) else [""]),
                    "Дополнительно": (res_additionally if (len(res_additionally) > 0) else [""]),
                    "Город": (res_sity if (len(res_sity) > 0) else [""]),
                    "Уровень открытия": res_level,
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="Pony",
        description="Персонажи")
def pony(item, category):
    try:
        res_icon, res_image = load_fake(file="pony",
                                        category=category), load_fake(file="pony",
                                                                      category=category)
        res_name_rus, res_name_eng = "", ""
        res_desc_rus, res_desc_eng = "", ""
        res_house, res_additionally, res_xp, res_sets, res_minigames, res_stars = "", [], "", [], [], []
        res_altpony, res_alttype = "", ""
        res_sity, res_level, res_cost = [], "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Icon",
                                                  limit=1)[0]["Url"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="Shop",
                                                   limit=1)[0]["Icon"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_desc_rus = DATA["russian"][item.find_all(name="Description",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_desc_eng = DATA["english"][item.find_all(name="Description",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_house = item.find_all(name="House",
                                      limit=1)[0]["Type"]
        except Exception:
            pass

        try:
            minecart = item.find_all(name="Minigames",
                                     limit=1)[0]["CanPlayMineCart"]

            if minecart == "0":
                res_additionally.append("Недоступен в шахте")
        except Exception:
            pass

        try:
            exp = item.find_all(name="OnArrive",
                                limit=1)[0]["EarnXP"]

            if exp != "0":
                res_xp = exp
        except Exception:
            pass

        try:
            for p_sets in item.find_all(name="Sets",
                                        limit=1)[0].find_all(name="Sets",
                                                             limit=1)[0]:
                try:
                    if p_sets["Value"]:
                        res_sets.append(p_sets["Value"])
                except Exception:
                    pass
        except Exception:
            pass

        try:
            mg_rank = item.find_all(name="Minigames",
                                    limit=1)[0]["EXP_Rank"]

            res_minigames.append(f"Коэффициент опыта: {mg_rank}")
        except Exception:
            pass

        try:
            mg_time = item.find_all(name="Minigames",
                                    limit=1)[0]["TimeBetweenPlayActions"]

            res_minigames.append(f"Время ожидания: {seconds_to_time(s=mg_time)}")
        except Exception:
            pass

        try:
            mg_skip = item.find_all(name="Minigames",
                                    limit=1)[0]["PlayActionSkipAgainCost"]

            res_minigames.append(f"Пропуск времени: Камни: {mg_skip}")
        except Exception:
            pass

        try:
            res_altpony = item.find_all(name="IsChangelingWithSet",
                                        limit=1)[0]["AltPony"]
        except Exception:
            pass

        try:
            alter_set = item.find_all(name="IsChangelingWithSet",
                                      limit=1)[0]["IAmAlterSet"]

            res_alttype = ("Основная" if (alter_set == "0") else "Дополнительная")
        except Exception:
            pass

        try:
            pets = item.find_all(name="PetsAvailability",
                                 limit=1)[0]["BanPets"]

            if pets == "1":
                res_additionally.append("Без питомцев")
        except Exception:
            pass

        try:
            m_ns = item.find_all(name="Misc",
                                 limit=1)[0]["NeverShapeshift"]

            if m_ns == "1":
                res_additionally.append("Не меняет форму")
        except Exception:
            pass

        try:
            m_nc = item.find_all(name="Misc",
                                 limit=1)[0]["NeverCrystallize"]

            if m_nc == "1":
                res_additionally.append("Не кристализуется")
        except Exception:
            pass

        try:
            m_np = item.find_all(name="Misc",
                                 limit=1)[0]["IsNotPony"]

            if m_np == "1":
                res_additionally.append("Не пони")
        except Exception:
            pass

        try:
            s_h = item.find_all(name="Sound",
                                limit=1)[0]["Hello"]

            s_r = item.find_all(name="Sound",
                                limit=1)[0]["Race"]

            if s_h or s_r:
                res_additionally.append("Есть озвучка")
        except Exception:
            pass

        try:
            amount, i = {}, 0

            for sub in item.find_all(name="StarRewards",
                                     limit=1)[0].find_all(name="Amount",
                                                          limit=1)[0]:
                amount.update({i: sub["Value"]})

                i += 1

            i = 0

            for sub in item.find_all(name="StarRewards",
                                     limit=1)[0].find_all(name="ID",
                                                          limit=1)[0]:
                if sub["Value"]:
                    res_stars.append(f"{i + 1}: "
                                     f"{CONSUMES[sub['Value']] if (sub['Value'] in CONSUMES) else sub['Value']}: "
                                     f"{amount[i]}")

                i += 1
        except Exception:
            pass

        # shopdata:
        try:
            for mz in DATA["shopdata"][item["ID"]]["MapZone"]:
                try:
                    res_sity.append(DATA["russian"][DATA["mapzones"][mz]].title())
                except Exception:
                    pass
        except Exception:
            pass

        try:
            res_level = DATA["shopdata"][item["ID"]]["UnlockValue"]
        except Exception:
            pass

        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Описание": ([res_desc_rus, res_desc_eng] if (res_desc_rus != res_desc_eng) else [res_desc_rus]),
                    "Дом": res_house,
                    "Опыт за покупку": res_xp,
                    "Награды за звезды": (res_stars if (len(res_stars) > 0) else [""]),
                    "Костюмы": (res_sets if (len(res_sets) > 0) else [""]),
                    "Мини игры": (res_minigames if (len(res_minigames) > 0) else [""]),
                    "Альтернативная форма": res_altpony,
                    "Тип формы": res_alttype,
                    "Дополнительно": (res_additionally if (len(res_additionally) > 0) else [""]),
                    "Город": (res_sity if (len(res_sity) > 0) else [""]),
                    "Уровень открытия": res_level,
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="PonySet",
        description="Наборы костюмов")
def ponyset(item, category):
    try:
        res_icon, res_image = load_fake(file="all",
                                        category=category), load_fake(file="all",
                                                                      category=category)
        res_name_rus, res_name_eng = "", ""
        res_parts, res_subsets, res_type, res_bonus = [], [], "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="PonySet",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="PonySet",
                                                   limit=1)[0]["AltIcon"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="PonySet",
                                                         limit=1)[0]["Localization"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="PonySet",
                                                         limit=1)[0]["Localization"]]
        except Exception:
            pass

        try:
            bonus = item.find_all(name="Bonus",
                                  limit=1)[0]["Type"]

            if bonus:
                bonus_amount = item.find_all(name="Bonus",
                                             limit=1)[0]["Amount"]

                res_bonus = f"{BONUS[bonus]}: +{bonus_amount}%"
        except Exception:
            pass

        try:
            parts_body = item.find_all(name="Parts",
                                       limit=1)[0]["Body"]

            if parts_body:
                res_parts.append(parts_body)
        except Exception:
            pass

        try:
            parts_mane = item.find_all(name="Parts",
                                       limit=1)[0]["Mane"]

            if parts_mane:
                res_parts.append(parts_mane)
        except Exception:
            pass

        try:
            parts_tail = item.find_all(name="Parts",
                                       limit=1)[0]["Tail"]

            if parts_tail:
                res_parts.append(parts_tail)
        except Exception:
            pass

        try:
            for subset in item.find_all(name="PonySet",
                                        limit=1)[0].find_all(name="SubSets",
                                                             limit=1)[0]:
                try:
                    if subset["Value"]:
                        res_subsets.append(subset["Value"])
                except Exception:
                    pass
        except Exception:
            pass

        try:
            issubset = item.find_all(name="PonySet",
                                     limit=1)[0]["IsSubSet"]

            res_type = ("Основной" if (issubset == "0") else "Дополнительный")
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_icon, res_image] if (res_icon != res_image) else [res_icon]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": ([res_icon, res_image] if (res_icon != res_image) else [res_icon]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Части": (res_parts if (len(res_parts) > 0) else [""]),
                    "Дополнительные наборы": (res_subsets if (len(res_subsets) > 0) else [""]),
                    "Тип": res_type,
                    "Бонус": res_bonus}
    except Exception:
        return None


@Parser(category="TravelersCafe",
        description="Отель \"Золотая подкова\"")
def travelerscafe(item, category):
    try:
        res_icon = load_fake(file="house",
                             category=category)
        res_name_rus, res_name_eng = "", ""
        res_size = ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Shop",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            size = int(int(item.find_all(name="GridData",
                                         limit=1)[0]["Size"]) / 2)

            res_size = f"{size}x{size}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Размер": res_size}
    except Exception:
        return None


@Parser(category="TapableContainer",
        description="")
def tapablecontainer(item, category):
    try:
        res_icon = load_fake(file="all",
                             category=category)
        res_name_rus, res_name_eng = "", ""
        res_spawn, res_capping, res_loot = [], [], []

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="UI",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="UI",
                                                         limit=1)[0]["TaskName"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="UI",
                                                         limit=1)[0]["TaskName"]]
        except Exception:
            pass

        try:
            s_i = item.find_all(name="Spawn",
                                limit=1)[0]["Interval"]

            res_spawn.append(f"Интервал: {seconds_to_time(s=s_i)}")
        except Exception:
            pass

        try:
            s_cpi = item.find_all(name="Spawn",
                                  limit=1)[0]["ChancePerInterval"]

            res_spawn.append(f"Шанс: {s_cpi}%")
        except Exception:
            pass

        try:
            i = 0

            for sub in item.find_all(name="Spawn",
                                     limit=1)[0].find_all(name="CappingPerMapZone",
                                                          limit=1)[0]:
                try:
                    res_capping.append(f"{DATA['russian'][DATA['mapzones'][str(i)]].title()}: {sub['Value']}")
                except Exception:
                    pass

                i += 1
        except Exception:
            pass

        try:
            dats = {}

            for itm in ["ItemsMinAmounts", "ItemsMaxAmounts", "ItemsChances"]:
                if itm not in dats:
                    dats.update({itm: {}})

                i = 0

                try:
                    for sub in item.find_all(name="Loot",
                                             limit=1)[0].find_all(name=itm,
                                                                  limit=1)[0]:
                        try:
                            dats[itm].update({i: sub["Value"]})
                        except Exception:
                            pass

                        i += 1
                except Exception:
                    pass

            i = 0

            for sub in item.find_all(name="Loot",
                                     limit=1)[0].find_all(name="Items",
                                                          limit=1)[0]:
                try:
                    if sub["Value"]:
                        res_loot.append(f"{CONSUMES[sub['Value']] if (sub['Value'] in CONSUMES) else sub['Value']}: "
                                        f"Количество: {dats['ItemsMinAmounts'][i]}-{dats['ItemsMaxAmounts'][i]}, "
                                        f"Шанс: {dats['ItemsChances'][i]}%")
                except Exception:
                    pass

                i += 1
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Спавн": (res_spawn if (len(res_spawn) > 0) else [""]),
                    "Ограничение для городов": (res_capping if (len(res_capping) > 0) else [""]),
                    "Награды": (res_loot if (len(res_loot) > 0) else [""])}
    except Exception:
        return None


@Parser(category="QuestSpecialItem",
        description="Специальные квестовые предметы")
def questspecialitem(item, category):
    try:
        res_icon = load_fake(file="all",
                             category=category)
        res_name_rus, res_name_eng = "", ""
        res_chance, res_consumable, res_additionally = "", "", []

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="QuestSpecialItem",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="QuestSpecialItem",
                                                         limit=1)[0]["Name"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="QuestSpecialItem",
                                                         limit=1)[0]["Name"]]
        except Exception:
            pass

        try:
            chance = item.find_all(name="QuestSpecialItem",
                                   limit=1)[0]["Chance"]

            if chance != "0":
                res_chance = f"{chance}%"
        except Exception:
            pass

        try:
            res_consumable = item.find_all(name="QuestSpecialItem",
                                           limit=1)[0]["ConsumableId"]
        except Exception:
            pass

        try:
            iu = item.find_all(name="SaveSettings",
                               limit=1)[0]["IsUnlimited"]

            if iu == "1":
                res_additionally.append("Безлимитный")
        except Exception:
            pass

        try:
            dr = item.find_all(name="SaveSettings",
                               limit=1)[0]["DisableReset"]

            if dr == "1":
                res_additionally.append("Отключен сброс")
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Шанс": res_chance,
                    "Расходный материал": res_consumable,
                    "Дополнительно": (res_additionally if (len(res_additionally) > 0) else [""])}
    except Exception:
        return None


@Parser(category="PonyPart",
        description="Костюмы")
def ponypart(item, category):
    try:
        res_icon, res_image = load_fake(file="all",
                                        category=category), load_fake(file="all",
                                                                      category=category)
        res_type, res_time, res_cost, res_linked, res_ingredients = "", "", "", "", []

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="PonyPart",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="PonyPart",
                                                   limit=1)[0]["AltIcon"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            res_type = POP[item.find_all(name="PonyPart",
                                         limit=1)[0]["Type"]]
        except Exception:
            pass

        try:
            res_linked = item.find_all(name="PonyPart",
                                       limit=1)[0]["LinkedPart"]
        except Exception:
            pass

        try:
            res_time = seconds_to_time(s=item.find_all(name="PonyPart",
                                                       limit=1)[0]["ApplyTime"])
        except Exception:
            pass

        try:
            cost = item.find_all(name="PonyPart",
                                 limit=1)[0]["PurchasePrice"]

            if cost != "0":
                res_cost = f"Камни: {cost}"
        except Exception:
            pass

        try:
            i = 1

            for sub in item.find_all(name="PonyPart",
                                     limit=1)[0].find_all(name="Ingredients",
                                                          limit=1)[0]:
                try:
                    if sub["Value"] != "0":
                        res_ingredients.append(f"{INGREDIENTS[i]}: {sub['Value']}")
                except Exception:
                    pass

                i += 1
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_icon, res_image] if (res_icon != res_image) else [res_icon])}
        else:
            return {"Изображение": ([res_icon, res_image] if (res_icon != res_image) else [res_icon]),
                    "Тип": res_type,
                    "Время надевания": res_time,
                    "Цена": res_cost,
                    "Связанная часть": res_linked,
                    "Ингредиенты": (res_ingredients if (len(res_ingredients) > 0) else [""])}
    except Exception:
        return None


@Parser(category="Path",
        description="Дорожки")
def path(item, category):
    try:
        res_icon = load_fake(file="all",
                             category=category)
        res_name_rus, res_name_eng = "", ""
        res_sity, res_permit = [], ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Shop",
                                                  limit=1)[0]["Icon"],
                              category=category)
            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_permit = item.find_all(name="PermitID",
                                       limit=1)[0]["ID"]
        except Exception:
            pass

        # shopdata:
        try:
            try:
                for mz in DATA["shopdata"][item.find_all(name="PermitID",
                                                         limit=1)[0]["ID"]]["MapZone"]:
                    try:
                        res_sity.append(DATA["russian"][DATA["mapzones"][mz]].title())
                    except Exception:
                        pass
            except Exception:
                mz = item.find_all(name="Shop",
                                   limit=1)[0]["MapZone"]

                res_sity.append(DATA["russian"][DATA["mapzones"][mz]].title())
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "ID в магазине": res_permit,
                    "Город": (res_sity if (len(res_sity) > 0) else [""]),
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="PartySceneDecore",
        description="")
def partyscenedecore(item, category):
    try:
        res_icon = load_fake(file="all",
                             category=category)
        res_name_rus, res_name_eng = "", ""
        res_size, res_xp = "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Shop",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            size = int(int(item.find_all(name="GridData",
                                         limit=1)[0]["Size"]) / 2)

            res_size = f"{size}x{size}"
        except Exception:
            pass

        try:
            res_xp = item.find_all(name="OnPurchase",
                                   limit=1)[0]["EarnXP"]
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Размер": res_size,
                    "Опыт за покупку": res_xp}
    except Exception:
        return None


@Parser(category="MasterExpansionZone",
        description="")
def masterexpansionzone(item, category):
    try:
        res_icon = load_fake(file="all",
                             category=category)
        res_name_rus, res_name_eng = "", ""
        res_desc_rus, res_desc_eng = "", ""
        res_quest = ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Unlock",
                                                  limit=1)[0]["UnavailableImage"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Unlock",
                                                         limit=1)[0]["UnavailableTitle"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Unlock",
                                                         limit=1)[0]["UnavailableTitle"]]
        except Exception:
            pass

        try:
            res_desc_rus = DATA["russian"][item.find_all(name="Unlock",
                                                         limit=1)[0]["UnavailableText"]]
        except Exception:
            pass

        try:
            res_desc_eng = DATA["english"][item.find_all(name="Unlock",
                                                         limit=1)[0]["UnavailableText"]]
        except Exception:
            pass

        try:
            res_quest = item.find_all(name="Unlock",
                                      limit=1)[0]["UnlockQuest"]
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Описание": ([res_desc_rus, res_desc_eng] if (res_desc_rus != res_desc_eng) else [res_desc_rus]),
                    "Квест": res_quest}
    except Exception:
        return None


@Parser(category="Inn",
        description="")
def inn(item, category):
    try:
        res_icon = load_fake(file="all",
                             category=category)
        res_name_rus, res_name_eng = "", ""
        res_size, res_visitors = "", []

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Icon",
                                                  limit=1)[0]["BookIcon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            size = int(int(item.find_all(name="GridData",
                                         limit=1)[0]["Size"]) / 2)

            res_size = f"{size}x{size}"
        except Exception:
            pass

        try:
            for p_vis in item.find_all(name="Visitors",
                                       limit=1)[0].find_all(name="Ponies",
                                                            limit=1)[0]:
                try:
                    if p_vis["Value"]:
                        res_visitors.append(p_vis["Value"])
                except Exception:
                    pass
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": [res_icon],
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Размер": res_size,
                    "Гости": (res_visitors if (len(res_visitors) > 0) else [""])}
    except Exception:
        return None


@Parser(category="EquestriaGirls",
        description="Костюмы в танцах")
def equestriagirls(item, category):
    try:
        res_icon, res_icons = load_fake(file="all",
                                        category=category), []
        res_pony = ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Icons",
                                                  limit=1)[0]["Icons_Avatar"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            for icon in item.find_all(name="Icons",
                                      limit=1)[0].find_all(name="Icons_Outfit",
                                                           limit=1)[0]:
                try:
                    if icon["Value"]:
                        res_icons.append(load_image(image=icon["Value"],
                                                    category=category))
                except Exception:
                    pass
        except Exception:
            pass

        try:
            res_pony = item.find_all(name="Pony_Objectdata",
                                     limit=1)[0]["Pony"]
        except Exception:
            pass

        return {"Изображение": [res_icon, *res_icons],
                "Пони": res_pony}
    except Exception:
        return None


@Parser(category="DestroyedHouse",
        description="Разрушение дома")
def destroyedhouse(item, category):
    try:
        res_icon = load_fake(file="house",
                             category=category)
        res_desc_rus, res_desc_eng = "", ""
        res_size, res_house, res_quest = "", "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Icon",
                                                  limit=1)[0]["QuestIcon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            res_desc_rus = DATA["russian"][item.find_all(name="Description",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_desc_eng = DATA["english"][item.find_all(name="Description",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            size = int(int(item.find_all(name="GridData",
                                         limit=1)[0]["Size"]) / 2)

            res_size = f"{size}x{size}"
        except Exception:
            pass

        try:
            res_house = item.find_all(name="Reward",
                                      limit=1)[0]["Pony_House"]
        except Exception:
            pass

        try:
            res_quest = item.find_all(name="QuestForPopUp",
                                      limit=1)[0]["Quest"]
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": [res_icon],
                    "Описание": ([res_desc_rus, res_desc_eng] if (res_desc_rus != res_desc_eng) else [res_desc_rus])}
        else:
            return {"Изображение": [res_icon],
                    "Описание": ([res_desc_rus, res_desc_eng] if (res_desc_rus != res_desc_eng) else [res_desc_rus]),
                    "Размер": res_size,
                    "Дом": res_house,
                    "Квест": res_quest}
    except Exception:
        return None


@Parser(category="Consumable",
        description="Расходный материал")
def consumable(item, category):
    try:
        res_icon, res_image = load_fake(file="all",
                                        category=category), load_fake(file="all",
                                                                      category=category)
        res_name_rus, res_name_eng = "", ""
        res_time, res_skip, res_consume = "", "", []

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Graphic",
                                                  limit=1)[0]["Sprite"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="Production",
                                                   limit=1)[0]["IconProductFrame"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Name",
                                                         limit=1)[0]["Unlocal"]]
        except Exception:
            pass

        try:
            time = item.find_all(name="Production",
                                 limit=1)[0]["Time"]

            if time != "0":
                res_time = seconds_to_time(s=time)
        except Exception:
            pass

        try:
            skip = item.find_all(name="Production",
                                 limit=1)[0]["SkipCost"]

            if skip != "0":
                res_skip = f"Камни: {skip}"
        except Exception:
            pass

        try:
            for con in CONSUMES:
                try:
                    con_val = item.find_all(name="Consume",
                                            limit=1)[0][con]

                    if con_val != "0":
                        res_consume.append(f"{CONSUMES[con]}: {con_val}")
                except Exception:
                    pass
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_icon, res_image] if (res_icon != res_image) else [res_icon]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": ([res_icon, res_image] if (res_icon != res_image) else [res_icon]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Время": res_time,
                    "Пропуск": res_skip,
                    "Бонусы": (res_consume if (len(res_consume) > 0) else [""])}
    except Exception:
        return None


@Parser(category="PlayerCardBackground",
        description="Фоны")
def playercardbackground(item, category):
    try:
        res_icon, res_image = load_fake(file="all",
                                        category=category), load_fake(file="all",
                                                                      category=category)
        bg_image_1, bg_image_2 = load_fake(file="all",
                                           category=category), load_fake(file="all",
                                                                         category=category)
        res_name_rus, res_name_eng = "", ""
        res_cost = ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Shop",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="Settings",
                                                   limit=1)[0]["PictureActive"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            bg_image_1 = load_image(image=item.find_all(name="Settings",
                                                        limit=1)[0]["BackgroundImage"],
                                    category=category)

            if bg_image_1:
                res_image = bg_image_1
        except Exception:
            pass

        try:
            bg_image_2 = load_image(image=item.find_all(name="Settings",
                                                        limit=1)[0]["BackgroundImageFrame"],
                                    category=category)

            if bg_image_2:
                res_image = bg_image_2
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        # shopdata:
        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Фон": ([bg_image_1, bg_image_2] if (bg_image_1 != bg_image_2) else [bg_image_1]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="PlayerCardBackgroundFrame",
        description="Рамки фонов")
def playercardbackgroundframe(item, category):
    try:
        res_icon, res_image = load_fake(file="all",
                                        category=category), load_fake(file="all",
                                                                      category=category)
        res_name_rus, res_name_eng = "", ""
        res_cost = ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Shop",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="Settings",
                                                   limit=1)[0]["PictureActive"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        # shopdata:
        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None


@Parser(category="PlayerCardCutieMark",
        description="Метки")
def playercardcutiemark(item, category):
    try:
        res_icon, res_image = load_fake(file="all",
                                        category=category), load_fake(file="all",
                                                                      category=category)
        res_name_rus, res_name_eng = "", ""
        res_pony, res_cost = "", ""

        # gameobjectdata:
        try:
            icon = load_image(image=item.find_all(name="Shop",
                                                  limit=1)[0]["Icon"],
                              category=category)

            if icon:
                res_icon = icon
        except Exception:
            pass

        try:
            image = load_image(image=item.find_all(name="Settings",
                                                   limit=1)[0]["PictureActive"],
                               category=category)

            if image:
                res_image = image
        except Exception:
            pass

        try:
            res_name_rus = DATA["russian"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        try:
            res_name_eng = DATA["english"][item.find_all(name="Shop",
                                                         limit=1)[0]["Label"]]
        except Exception:
            pass

        try:
            res_pony = item.find_all(name="Settings",
                                     limit=1)[0]["PonyStarsID"]
        except Exception:
            pass

        # shopdata:
        try:
            c_type = DATA["shopdata"][item["ID"]]["CurrencyType"]
            c_value = DATA["shopdata"][item["ID"]]["Cost"]

            if (c_type != "0") and (c_value != "0"):
                res_cost = f"{CURRENCY[c_type]}: {c_value}"
        except Exception:
            pass

        if DATA["settings"]["Lite"]:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus])}
        else:
            return {"Изображение": ([res_image, res_icon] if (res_image != res_icon) else [res_image]),
                    "Имя": ([res_name_rus, res_name_eng] if (res_name_rus != res_name_eng) else [res_name_rus]),
                    "За звезды пони": res_pony,
                    "Цена": res_cost,
                    "Магазин": ("Можно купить" if (item["ID"] in DATA["shopdata"]) else "Нельзя купить")}
    except Exception:
        return None
