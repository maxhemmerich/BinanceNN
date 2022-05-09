from datetime import datetime
import pandas as pd
import requests
import pickle

'Started: Monday May 9, 3:10PM'

# Create data gathering function
def getbtcdata():

    # Request parameters
    headers = {'user-agent': 'Safari/537.36'}
    requests.adapters.DEFAULT_RETRIES = 1000
    
    # Make loop for seconds
    secs = 0
    while True:
        if secs == 60:
            secs = 0
        now = str(datetime.now())
    
    # Get data every 3 seconds (limit for 10,000 prices):
        if int(now[17:19]) == secs:
            secs = secs + 3
    
    # Get Binance BTC data in a dataframe
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
    
    # Add time (decimal)
            data.insert(3,"time",round(float(now[11:13])/24+float(now[14:16])/1440+float(now[17:19])/86400,8),True)
    
    # Dump data to pickle file        
            with open('btc.pkl','ab+') as f:
                pickle.dump(data,f)
                
    # Print time of collection            
            print("$ " + now + " $")

# Try 7 times to handle network errors
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
                        
# Load pickle file (for after data collection)
file = []
with (open("btc.pkl", "rb")) as openfile:
    while True:
        try:
            file.append(pickle.load(openfile))
        except EOFError:
            break
