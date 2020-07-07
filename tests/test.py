import active as LOL
import time

while True:
    time.sleep(5)
    if LOL.check_status():
        break
act = LOL.ActiveGame()
for player in act.players:
    print(player.champion_name)
