import urllib
import json
from osu.account import OSUAccount

class OSUApi:

    def __init__(self, token):
        self.token = token

    def get_osu_account(self, username):
        request = "https://osu.ppy.sh/api/get_user?k=" + self.token + "&" + urllib.parse.urlencode({'u': username})
        account_data = urllib.request.urlopen(request)
        parsed_data = json.loads(account_data.read())
        account = OSUAccount()
        if(len(parsed_data)):
            account.user_id = parsed_data[0]["user_id"]
            account.username = parsed_data[0]["username"]
            account.playcount = parsed_data[0]["playcount"]
            account.ranked_score = parsed_data[0]["ranked_score"]
            account.total_score = parsed_data[0]["total_score"]
            account.pp_raw = parsed_data[0]["pp_raw"]
            account.pp_rank = parsed_data[0]["pp_rank"]
            account.accuracy = parsed_data[0]["accuracy"]
        return account

