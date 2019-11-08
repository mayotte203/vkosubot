import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import time

keyboard = "{    \"one_time\": false,    \"buttons\": [        [{            \"action\": {                \"type\": \"location\",                \"payload\": \"{\\\"button\\\": \\\"1\\\"}\"            }        }],        [{            \"action\": {                \"type\": \"open_app\",                \"app_id\": 6979558,                \"owner_id\": -181108510,                \"hash\": \"sendKeyboard\",                \"label\": \"Отправить клавиатуру\"            }        }],        [{            \"action\": {                \"type\": \"vkpay\",                \"hash\": \"action=transfer-to-group&group_id=181108510&aid=10\"            }        }],        [{                \"action\": {                    \"type\": \"text\",                    \"payload\": \"{\\\"button\\\": \\\"1\\\"}\",                    \"label\": \"Negative\"                },                \"color\": \"negative\"            },            {                \"action\": {                    \"type\": \"text\",                    \"payload\": \"{\\\"button\\\": \\\"2\\\"}\",                    \"label\": \"Positive\"                },                \"color\": \"positive\"            },            {                \"action\": {                    \"type\": \"text\",                    \"payload\": \"{\\\"button\\\": \\\"2\\\"}\",                    \"label\": \"Primary\"                },                \"color\": \"primary\"            },            {                \"action\": {                    \"type\": \"text\",                    \"payload\": \"{\\\"button\\\": \\\"2\\\"}\",                    \"label\": \"Secondary\"                },                \"color\": \"secondary\"            }        ]    ]}"

class bot:
    def __init__(self, token):
        self.token = token
        self.keyboard0_json = open("bot/Keyboard0.json", "r").read()


    def run(self):
        vk_session = vk_api.VkApi(token=self.token)
        vk_longpoll = VkLongPoll(vk_session, wait=25)
        vk = vk_session.get_api()
        while(True):
            print("test")
            #вот тут будем время для уведовмлений чекать
            for event in vk_longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.from_user:
                        vk.messages.send(
                            user_id=event.user_id,
                            message='Ваш текст',
                            random_id=random.getrandbits(64),
                            keyboard=self.keyboard0_json
                        )
