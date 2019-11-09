from bot.bot import bot
from osu.api import OSUApi
vk_token = "529521db9f05c9176672d8ceedfd01cb503a179ada3af15b3bba5693d1b0a0eabc1bedcfc2e5ff1bb7b83"
osu_token = "3541ef6f05c8814ed2396befc4dded47f09f104e"

osu_bot = bot(vk_token)
osu_bot.run(osu_token)

