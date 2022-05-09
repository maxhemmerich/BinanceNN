from datetime import datetime
import pandas as pd
import requests
import pickle

'Started: Monday May 9, 3:10PM'


def getbtcdata():
    headers = {'user-agent': 'Safari/537.36'}
    requests.adapters.DEFAULT_RETRIES = 1000
    secs = 0
    while True:
        if secs == 60:
            secs = 0
        now = str(datetime.now())
    
    # Every second:
        if int(now[17:19]) == secs:
            secs = secs + 3
    
    # Add binance data to pickle file
            data = pd.DataFrame()
            r = requests.get("https://api.binance.com/api/v3/depth",
                             params=dict(symbol="BTCBUSD",limit=5000),headers=headers)
            results = r.json()
            frames = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"],
                                         dtype=float)
                      for side in ["bids", "asks"]}
            frames_list = [frames[side].assign(side=side) for side in frames]
            data = pd.concat(frames_list, axis="index",
                             ignore_index=True, sort=True)
            data.insert(3,"time",round(float(now[11:13])/24+float(now[14:16])/1440+float(now[17:19])/86400,8),True)
            with open('btc.pkl','ab+') as f:
                pickle.dump(data,f)
            print("$ " + now + " $")

try:
    getbtcdata()
except:
    try:
        getbtcdata()
    except:
        try:
            getbtcdata()
        except:
            try:
                getbtcdata()
            except:
                try:
                    getbtcdata()
                except:
                    try:
                        getbtcdata()
                    except:
                        getbtcdata()
                        
# Load pickle file
file = []
with (open("btc.pkl", "rb")) as openfile:
    while True:
        try:
            file.append(pickle.load(openfile))
        except EOFError:
            break
