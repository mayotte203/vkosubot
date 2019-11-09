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

    def run(self, token):
        vk_session = vk_api.VkApi(token=self.token)
        vk_longpoll = VkLongPoll(vk_session, wait=25)
        vk = vk_session.get_api()
        osu_api = OSUApi(token)
        osu_api.get_osu_account("каl")
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
                                    random_id=random.getrandbits(64)
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
                                        random_id=random.getrandbits(64)
                                    )
                                    self.d_vk_osu_accounts[event.user_id] = osu_api.get_osu_account(self.d_vk_osu_accounts[event.user_id].user_id)
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Выберите одну из категорий ниже",
                                    random_id=random.getrandbits(64),
                                    keyboard=self.keyboard0_json
                                )

    def statistic_presenter(self, user_account_old, user_account_new):
        return ("Очки производительности - " + str(user_account_new.pp_raw) + "(" + str(user_account_new.pp_raw - user_account_old.pp_raw) + ")\n"
            + "Точность - " + str(user_account_new.accuracy) + "(" + str(user_account_new.accuracy - user_account_old.accuracy) + ")\n"
            + "Всего игр - " + str(user_account_new.playcount) + "(" + str(user_account_new.playcount - user_account_old.playcount) + ")\n"
            + "Набрано очков - " + str(user_account_new.total_score) + "(" + str(user_account_new.total_score - user_account_old.total_score) + ")\n"
            + "Ваш глобальный ранк - #" + str(user_account_new.pp_rank) + "(" + str(user_account_new.pp_rank - user_account_old.pp_rank) + ")")



