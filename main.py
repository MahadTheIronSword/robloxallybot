#########################################
#  Roblox Ally Bot                      #
#                                       #
#                                       #
#########################################


import random
import requests
import time

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
AUTH_URL = 'https://auth.roblox.com/v2/logout'
GROUP_URL = 'https://groups.roblox.com/v1/groups/%s/relationships/allies/%s'
ORIGIN = 'https://roblox.com'
REFERER = 'https://www.roblox.com/groups/%s'

COOKIE = input('What is your .ROBLOSECURITY?:\n')
GROUP_ID = input('What is your group id?:\n')
MIN_ID = input('Min Id:\n')
MAX_ID = input('Max Id:\n')


def OBTAIN_TOKEN():
    AuthRequest = requests.post(
        AUTH_URL,
        headers={
            'User-Agent': USER_AGENT
        },
        cookies={
            '.ROBLOSECURITY': COOKIE
        }
    )

    XSRF = AuthRequest.headers.get('x-csrf-token')

    if XSRF:
        return XSRF
    else:
        return None


class Bot:
    def __init__(self):
        self.TOKEN = OBTAIN_TOKEN()

    def ALLY_GROUP(self, session):
        RANDOM_GROUP = random.randint(int(MIN_ID), int(MAX_ID))

        GroupAllyRequest = session.post(
            GROUP_URL % (GROUP_ID, RANDOM_GROUP),
            headers={
                'User-Agent': USER_AGENT,
                'x-csrf-token': self.TOKEN,
                'Origin': ORIGIN,
                'Referer': REFERER % GROUP_ID
            },
            cookies={
                '.ROBLOSECURITY': COOKIE
            },
            allow_redirects=False
        )

        return GroupAllyRequest


NewBot = Bot()

while True:
    AllyRequest = NewBot.ALLY_GROUP(requests.Session())
    print(AllyRequest.json())
    if AllyRequest.status_code == 200:
        print('Successfully allied!')
    elif AllyRequest.status_code == 429:
        print('429 - Waiting 150 seconds')
        time.sleep(150)
    elif AllyRequest.status_code == 401:
        NewBot.TOKEN = OBTAIN_TOKEN()

    time.sleep(3)
