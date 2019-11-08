import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
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
                        if(self.d_vk_osu_accounts.get(event.user_id) == None):
                            if(osu_api.get_osu_account(event.text).user_id):
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
                            vk.messages.send(
                                user_id=event.user_id,
                                message=self.d_vk_osu_accounts[event.user_id].username,
                                random_id=random.getrandbits(64)
                            )

