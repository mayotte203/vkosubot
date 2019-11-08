from bot.bot import bot
from osu.api import OSUApi
vk_token = "20f1ca667234cd3e4a16b37f1dcda331a1e02d247a5bf0885bc21f05a4117c5310842b3cada12fa84a5f6"
osu_token = "3541ef6f05c8814ed2396befc4dded47f09f104e"

osu_bot = bot(vk_token)
osu_bot.run(osu_token)

