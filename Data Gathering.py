from datetime import datetime
import pandas as pd
import requests
import pickle

secs = 0
while True:
    if secs == 60:
        secs = 0
    now = str(datetime.now())
    
# Every second:
    if int(now[17:19]) == secs:
        secs = secs + 5

# Add binance data to pickle file
        data = pd.DataFrame()
        r = requests.get("https://api.binance.com/api/v3/depth",
                         params=dict(symbol="BTCBUSD",limit=1000))
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
        print("$ " + str(datetime.now()) + " $")

# Load pickle file
file = []
with (open("btc.pkl", "rb")) as openfile:
    while True:
        try:
            file.append(pickle.load(openfile))
        except EOFError:
            break
        

# Plot Depth of Market (DOM)
# =============================================================================
# import matplotlib.pyplot as plt
# import seaborn as sns
#
#     price_summary = alldata.groupby("side").price.describe()
#     price_summary.to_markdown()
#     r = requests.get("https://api.binance.com/api/v3/ticker/bookTicker", params=dict(symbol="BTCBUSD"))
#     book_top = r.json()
#     name = book_top.pop("symbol")  # get symbol and also delete at the same time
#     s = pd.Series(book_top, name=name, dtype=float)
#     s.to_markdown()
#     fig, ax = plt.subplots()
#     
#     sns.ecdfplot(x="price", weights="quantity", stat="count", complementary=True, data=frames["bids"], ax=ax)
#     sns.ecdfplot(x="price", weights="quantity", stat="count", data=frames["asks"], ax=ax)
#     sns.scatterplot(x="price", y="quantity", hue="side", data=alldata, ax=ax)
#     
#     ax.set_xlabel("Price")
#     ax.set_ylabel("Quantity")
# =============================================================================