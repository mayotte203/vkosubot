import vk_api
import re
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import datetime
from osu.api import OSUApi


class bot:
    def __init__(self, token):
        self.token = token
        self.keyboard_null_json = open("bot/KeyboardNuLL.json", "r").read()
        self.keyboard0_json = open("bot/Keyboard0.json", "r").read()
        self.keyboard1_json = open("bot/Keyboard1.json", "r").read()
        self.keyboard2_json = open("bot/Keyboard2.json", "r").read()
        self.d_vk_osu_accounts = dict()
        self.d_vk_preferences = dict()
        self.d_vk_state = dict()

    def run(self, token):
        vk_session = vk_api.VkApi(token=self.token)
        vk_longpoll = VkLongPoll(vk_session, wait=25)
        self.vk = vk_session.get_api()
        self.osu_api = OSUApi(token)
        while True:
            # вот тут будем время для уведовмлений чекать
            for event in vk_longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.from_user:
                        if self.d_vk_osu_accounts.get(event.user_id) is None:
                            if self.osu_api.get_osu_account(event.text).user_id:
                                self.vk.messages.send(
                                    user_id=event.user_id,
                                    message="Ваш ник - " + self.osu_api.get_osu_account(event.text).username,
                                    random_id=random.getrandbits(64),
                                )
                                self.d_vk_osu_accounts[event.user_id] = self.osu_api.get_osu_account(event.text)
                                self.d_vk_preferences[event.user_id] = self.userPreferences()
                                self.d_vk_state[event.user_id] = 'menu'
                                self.vk.messages.send(
                                    user_id=event.user_id,
                                    message="Выберите одну из категорий ниже",
                                    random_id=random.getrandbits(64),
                                    keyboard=self.keyboard0_json
                                )
                            else:
                                self.vk.messages.send(
                                    user_id=event.user_id,
                                    message="Ваш аккаунт не найден, введите свой ник",
                                    random_id=random.getrandbits(64)
                                )
                        else:
                            if self.d_vk_state[event.user_id] == 'menu':
                                if str(event.text).lower() == 'статистика':
                                    self.send_statistic(event.user_id)
                                elif str(event.text).lower() == 'битмапы':
                                    self.send_beatmaps(event.user_id)
                                elif str(event.text).lower() == 'настройка':
                                    self.d_vk_state[event.user_id] = 'settings'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Выберите одну из категорий ниже",
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard1_json
                                    )
                                else:
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Выберите одну из категорий ниже",
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard0_json
                                    )
                            elif self.d_vk_state[event.user_id] == 'settings':
                                if str(event.text).lower() == 'настройка уведомлений':
                                    self.d_vk_state[event.user_id] = 'notifications'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Выберите нужный вариант",
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard2_json
                                    )
                                elif str(event.text).lower() == 'настройка жанров':
                                    self.d_vk_state[event.user_id] = 'genres'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message=("Введите номера необходимых жанров:\n"
                                                 + "1. Видеоигры\n"
                                                 + "2. Аниме\n"
                                                 + "3. Рок\n"
                                                 + "4. Поп\n"
                                                 + "5. Хип-Хоп\n"
                                                 + "6. Электроника\n"
                                                 + "7. Другие"),
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard_null_json
                                    )
                                elif str(event.text).lower() == 'настройка языков':
                                    self.d_vk_state[event.user_id] = 'languages'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message=("Введите номера необходимых жанров:\n"
                                                 + "1. Английский\n"
                                                 + "2. Японский\n"
                                                 + "3. Китайский\n"
                                                 + "4. Корейский\n"
                                                 + "5. Инструментал\n"
                                                 + "6. Другие"),
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard_null_json
                                    )
                                elif str(event.text).lower() == 'выход':
                                    self.d_vk_state[event.user_id] = 'menu'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Выберите одну из категорий ниже",
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard0_json
                                    )
                                else:
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Выберите одну из категорий ниже",
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard1_json
                                    )
                            elif self.d_vk_state[event.user_id] == 'notifications':
                                if str(event.text).lower() == 'отключить уведомления':
                                    self.d_vk_preferences[event.user_id].notifications = 'disable'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Настройки сохранены",
                                        random_id=random.getrandbits(64)
                                    )
                                    self.d_vk_state[event.user_id] = 'menu'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Выберите одну из категорий ниже",
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard0_json
                                    )
                                elif str(event.text).lower() == 'уведомления раз в день':
                                    self.d_vk_preferences[event.user_id].notifications = 'daily'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Настройки сохранены",
                                        random_id=random.getrandbits(64)
                                    )
                                    self.d_vk_state[event.user_id] = 'menu'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Выберите одну из категорий ниже",
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard0_json
                                    )
                                elif str(event.text).lower() == 'уведомления раз в неделю':
                                    self.d_vk_preferences[event.user_id].notifications = 'weekly'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Настройки сохранены",
                                        random_id=random.getrandbits(64)
                                    )
                                    self.d_vk_state[event.user_id] = 'menu'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Выберите одну из категорий ниже",
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard0_json
                                    )
                                elif str(event.text).lower() == 'выход':
                                    self.d_vk_state[event.user_id] = 'menu'
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Выберите одну из категорий ниже",
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard0_json
                                    )
                                else:
                                    self.vk.messages.send(
                                        user_id=event.user_id,
                                        message="Выберите одну из категорий ниже",
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard2_json
                                    )
                            elif self.d_vk_state[event.user_id] == 'genres':
                                genres_dict = {'1': [2], '2': [3], '3': [4], '4': [5], '5': [9], '6': [10],
                                               '7': [0, 1, 6, 7, 8]}
                                genres = re.findall(r'\d+', event.text)
                                genres_list = list()
                                for genre in genres:
                                    if genres_dict.get(genre) is not None:
                                        genres_list.extend(genres_dict[genre])
                                self.d_vk_preferences[event.user_id].genres = genres_list
                                self.d_vk_state[event.user_id] = 'menu'
                                self.vk.messages.send(
                                    user_id=event.user_id,
                                    message="Настройки сохранены",
                                    random_id=random.getrandbits(64)
                                )
                                self.vk.messages.send(
                                    user_id=event.user_id,
                                    message="Выберите одну из категорий ниже",
                                    random_id=random.getrandbits(64),
                                    keyboard=self.keyboard0_json
                                )
                            elif self.d_vk_state[event.user_id] == 'languages':
                                languages_dict = {'1': [2], '2': [3], '3': [4], '4': [6], '5': [5],
                                                  '6': [0, 7, 8, 9, 10, 11]}
                                languages = re.findall(r'\d+', event.text)
                                languages_list = list()
                                for language in languages:
                                    if languages_dict.get(language) is not None:
                                        languages_list.extend(languages_dict[language])
                                self.d_vk_preferences[event.user_id].languages = languages_list
                                self.d_vk_state[event.user_id] = 'menu'
                                self.vk.messages.send(
                                    user_id=event.user_id,
                                    message="Настройки сохранены",
                                    random_id=random.getrandbits(64)
                                )
                                self.vk.messages.send(
                                    user_id=event.user_id,
                                    message="Выберите одну из категорий ниже",
                                    random_id=random.getrandbits(64),
                                    keyboard=self.keyboard0_json
                                )

    def statistic_presenter(self, user_account_old, user_account_new):
        result = ""
        result += "Очки производительности - " + str(user_account_new.pp_raw)
        if user_account_new.pp_raw - user_account_old.pp_raw >= 0:
            result += "(+"
        else:
            result += "("
        result += str(round(user_account_new.pp_raw - user_account_old.pp_raw, 2)) + ")\n"
        result += "Точность - " + str(user_account_new.accuracy)
        if user_account_new.accuracy - user_account_old.accuracy >= 0:
            result += "(+"
        else:
            result += "("
        result += str(round(user_account_new.accuracy - user_account_old.accuracy, 2)) + ")\n"
        result += "Всего игр - " + str(user_account_new.playcount)
        result += "(+" + str(user_account_new.playcount - user_account_old.playcount) + ")\n"
        result += "Набрано очков - " + str(user_account_new.total_score)
        result += "(+" + str(user_account_new.total_score - user_account_old.total_score) + ")\n"
        result += "Ваш глобальный ранк - #" + str(user_account_new.pp_rank)
        if user_account_new.pp_rank - user_account_old.pp_rank >= 0:
            result += "(+"
        else:
            result += "("
        result += str(user_account_new.pp_rank - user_account_old.pp_rank) + ")"
        return result

    def beatmap_presenter(self, osu_beatmap):
        result = ("\"" + osu_beatmap.title + "\" - " + osu_beatmap.artist + "\n"
                  + "Сложности:\n")
        for version, difficulty in osu_beatmap.difficulty.items():
            result = result + "\"" + str(version) + "\" - " + str(difficulty) + "\n"
        result = (result + "Создатель - " + osu_beatmap.creator + "\n"
                  + "Ссылка - https://osu.ppy.sh/beatmapsets/" + str(osu_beatmap.set_id))
        return result

    def send_statistic(self, user_id):
        message = ("Статистика аккаунта " + self.d_vk_osu_accounts[user_id].username
                   + " на " + str(datetime.date.today().day) + "." + str(datetime.date.today().month)
                   + "\n" + self.statistic_presenter(self.d_vk_osu_accounts[user_id], self.osu_api.get_osu_account(
                    self.d_vk_osu_accounts[user_id].user_id)))
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=random.getrandbits(64),
            keyboard=self.keyboard0_json
        )
        self.d_vk_osu_accounts[user_id] = self.osu_api.get_osu_account(self.d_vk_osu_accounts[user_id].user_id)

    def send_beatmaps(self, user_id):
        message = ("Подборка битмапов на " + str(datetime.date.today().day) + "." + str(
            datetime.date.today().month) + "\n")
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=random.getrandbits(64)
        )
        for data in self.osu_api.get_osu_beatmaps():
            if (self.d_vk_preferences[user_id].genres.count(data.genre) > 0 and
                    self.d_vk_preferences[user_id].languages.count(data.language) > 0):
                self.vk.messages.send(
                    user_id=user_id,
                    message=self.beatmap_presenter(data),
                    random_id=random.getrandbits(64),
                    keyboard=self.keyboard0_json
                )

    class userPreferences:
        notifications = 0
        genres = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        languages = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
