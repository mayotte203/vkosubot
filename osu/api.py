import urllib
import json
from osu.account import OSUAccount
from osu.beatmap import OSUBeatmap

class OSUApi:

    def __init__(self, token):
        self.token = token

    def get_osu_account(self, username):
        request = "https://osu.ppy.sh/api/get_user?k=" + self.token + "&" + urllib.parse.urlencode({'u': username})
        account_data = urllib.request.urlopen(request)
        parsed_data = json.loads(account_data.read())
        account = OSUAccount()
        if len(parsed_data):
            account.user_id = parsed_data[0]["user_id"]
            account.username = str(parsed_data[0]["username"])
            account.playcount = int(parsed_data[0]["playcount"])
            account.ranked_score = int(parsed_data[0]["ranked_score"])
            account.total_score = int(parsed_data[0]["total_score"])
            account.pp_raw = round(float(parsed_data[0]["pp_raw"]), 2)
            account.pp_rank = int(parsed_data[0]["pp_rank"])
            account.accuracy = round(float(parsed_data[0]["accuracy"]), 2)
        return account

    def get_osu_beatmaps(self):
        request = "https://osu.ppy.sh/api/get_beatmaps?k=" + self.token + "&limit=10&m=0"
        beatmaps_data = urllib.request.urlopen(request)
        parsed_data = json.loads(beatmaps_data.read())
        beatmaps_list = []
        for data in parsed_data:
            if len(list(filter(lambda x: x.set_id == int(data["beatmapset_id"]), beatmaps_list))) == 0:
                beatmaps_list.append(OSUBeatmap(
                    set_id=int(data["beatmapset_id"]),
                    map_id=int(data["beatmap_id"]),
                    artist=str(data["artist"]),
                    title=str(data["title"]),
                    creator=str(data["creator"]),
                    genre=int(data["genre_id"]),
                    language=int(data["language_id"]),
                    difficulty={str(data["version"]) : (round(float(data["difficultyrating"]), 2))}
                ))
            else:
                for beatmap in beatmaps_list:
                    if beatmap.set_id == int(data["beatmapset_id"]):
                        beatmap.difficulty[str(data["version"])] = round(float(data["difficultyrating"]), 2)
        return beatmaps_list

