import sys
from fairlay_public_api import FairlayPythonPublic

fairlay = FairlayPythonPublic()
print(fairlay.get_server_time())
print(fairlay.get_competitions(1))
print(fairlay.get_markets_and_odds({
    "OnlyActive": True,
    "NoZombie": False
}))