import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import datetime
from osu.api import OSUApi

class bot:
    def __init__(self, token):
        self.token = token
        self.keyboard0_json = open("bot/Keyboard0.json", "r").read()
        self.d_vk_osu_accounts = dict()
        self.d_vk_preferences = dict()

    def run(self, token):
        vk_session = vk_api.VkApi(token=self.token)
        vk_longpoll = VkLongPoll(vk_session, wait=25)
        vk = vk_session.get_api()
        osu_api = OSUApi(token)
        while(True):
            #вот тут будем время для уведовмлений чекать
            for event in vk_longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.from_user:
                        if self.d_vk_osu_accounts.get(event.user_id) == None:
                            if osu_api.get_osu_account(event.text).user_id:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Ваш ник - " + osu_api.get_osu_account(event.text).username,
                                    random_id=random.getrandbits(64),
                                    keyboard=self.keyboard0_json
                                )
                                self.d_vk_osu_accounts[event.user_id] = osu_api.get_osu_account(event.text)
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Ваш аккаунт не найден, введите свой ник",
                                    random_id=random.getrandbits(64)
                                )
                        else:
                            request_vars = ['статистика', 'битмапы', 'настройка']
                            if (str(event.text).lower()) in request_vars:
                                if(str(event.text).lower()) == request_vars[0]:
                                    message = ("Статистика аккаунта " + self.d_vk_osu_accounts[event.user_id].username
                                               + " на " + str(datetime.date.today().day) + "." + str(datetime.date.today().month)
                                               + "\n" + self.statistic_presenter(self.d_vk_osu_accounts[event.user_id], osu_api.get_osu_account(self.d_vk_osu_accounts[event.user_id].user_id)))
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=message,
                                        random_id=random.getrandbits(64),
                                        keyboard=self.keyboard0_json
                                    )
                                    self.d_vk_osu_accounts[event.user_id] = osu_api.get_osu_account(self.d_vk_osu_accounts[event.user_id].user_id)
                                elif (str(event.text).lower()) == request_vars[1]:
                                    message = ("Подборка битмапов на " + str(datetime.date.today().day) + "." + str(
                                                datetime.date.today().month) + "\n")
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=message,
                                        random_id=random.getrandbits(64)
                                    )
                                    for data in osu_api.get_osu_beatmaps():
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message=self.beatmap_presenter(data),
                                            random_id=random.getrandbits(64),
                                            keyboard=self.keyboard0_json
                                        )
                            else:
                                vk.messages.send(
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
        languages = ["Не указан", "Не указан", "Английский", "Японский", "Китайский", "Инструментал", "Корейский", "Французский", "Немецкий", "Шведский", "Испанский", "Итальянский"]
        genres = ["Не указан", "Не указан", "Видеоигры", "Аниме", "Рок", "Поп", "Другой", "Новинка", "Не указан", "Хип-Хоп", "Электроника"]
        result = ("\"" + osu_beatmap.title + "\" - " + osu_beatmap.artist + "\n"
                  + "Сложности:\n")
        for version, difficulty in osu_beatmap.difficulty.items():
            result = result + "\"" + str(version) + "\" - " + str(difficulty) + "\n"
        result = (result + "Создатель - " + osu_beatmap.creator + "\n"
                  + "Ссылка - https://osu.ppy.sh/beatmapsets/" + str(osu_beatmap.set_id))
        return result



