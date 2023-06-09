import pandas as pd
import math
import locale

# Set the locale to the desired format
locale.setlocale(locale.LC_ALL, 'en_US')

# Read the stock data into a Pandas DataFrame
df = pd.read_csv('Saham/Semua/bbri.csv')

# Convert the date column to a datetime data type
df['date'] = pd.to_datetime(df['date'])

# Sort the DataFrame by date in ascending order
df = df.sort_values('date')

# Calculate moving averages
df['MA5'] = df['close'].rolling(window=5).mean()
df['MA10'] = df['close'].rolling(window=10).mean()
df['MA20'] = df['close'].rolling(window=20).mean()
df['MA30'] = df['close'].rolling(window=30).mean()
df['MA50'] = df['close'].rolling(window=50).mean()
df['MA100'] = df['close'].rolling(window=100).mean()
df['MA200'] = df['close'].rolling(window=200).mean()

listdata = []
listma = ['5','10','20','30','50','100','200']
biggest_estimated_return = 100
lowest_lost = ""
example_money = 10000000
for x in range(len(listma)):
    ma = 'MA'
    for y in range(len(listma)):
        lowerma = ma + listma[x]
        if (x == y or x > y):
            pass
        else:
            higherma =  ma + listma[y]

            # Initialize the 'Signal' column with 'Hold' for no action
            df['Signal'] = 'Hold'

            # Identify buy signals (lowerMA crossing above HigherMA)
            buy_indices = df[(df[lowerma] > df[higherma]) & (df[lowerma].shift() < df[higherma].shift())].index
            df.loc[buy_indices, 'Signal'] = 'Buy'

            # Identify sell signals (lowerMA crossing below HigherMA)
            sell_indices = df[(df[lowerma] < df[higherma]) & (df[lowerma].shift() > df[higherma].shift())].index
            df.loc[sell_indices, 'Signal'] = 'Sell'

            # Filter and print only the rows with buy and sell signals
            filtered_df = df[df['Signal'].isin(['Buy', 'Sell'])]

            # Calculate estimated returns
            previous_buy_index = None
            estimated_returns = []
            for index, row in df.iterrows():
                
                if row['Signal'] == 'Buy':
                    previous_buy_index = index
                    # if((str(lowerma)+"&"+str(higherma) ) == 'MA20&MA100'):
                    #     print("buy action " + str(row["date"]) + " price close " + str(row['close']))
                elif row['Signal'] == 'Sell' and previous_buy_index is not None:
                    # if((str(lowerma)+"&"+str(higherma) ) == 'MA20&MA100'):
                    #     print("sell action " + str(row["date"] )+ " price close " + str(row['close']))
                    buy_close = df.loc[previous_buy_index, 'close']
                    sell_close = row['close']
                    estimated_return = ((sell_close - buy_close) / buy_close) * 100
                    estimated_returns.append(estimated_return)

            firstmoney = 100
            lastmoney = firstmoney
            lost = 0
            profit = 0
            biggest_lost = 0
            biggest_profit = 0
            for i, return_value in enumerate(estimated_returns, start=1):
                lastmoney = lastmoney * ((100 + return_value)/100)
                if( (biggest_profit == 0 or biggest_profit < return_value) and return_value > 0):
                    biggest_profit = return_value
                if( (biggest_lost == 0 or (biggest_lost * -1) < (return_value * -1) ) and return_value < 0):
                    biggest_lost = return_value
                # if((str(lowerma)+"&"+str(higherma) ) == 'MA20&MA100'):
                #     print("trade " + str(i) + " " + str(return_value))
                if(return_value < 0):
                    lost = lost + 1
                elif(return_value > 0):
                    profit = profit + 1
            if(lost != 0 and profit != 0):
                listdata.append({"ma_compared": str(lowerma)+"&"+str(higherma),"probability": profit/(profit+lost) * 100,"estimated_return": (((lastmoney - firstmoney)/firstmoney)*100),"lost" : lost, "profit": profit, "biggest_profit" : biggest_profit, "biggest_lost": biggest_lost})
                if(biggest_estimated_return <  (((lastmoney - firstmoney)/firstmoney)*100)):
                    biggest_estimated_return =  (((lastmoney - firstmoney)/firstmoney)*100)
                if(lowest_lost == ""):
                    lowest_lost = biggest_lost
                elif(lowest_lost < biggest_lost):
                    lowest_lost = biggest_lost


arrange_bydis = []
for k in range(len(listdata)):
    data = listdata[k]
    dis = math.sqrt(  pow((lowest_lost - data["biggest_lost"]),2) + pow((100 - data["probability"]),2) + pow((biggest_estimated_return - data["estimated_return"]),2))
    arrange_bydis.append({"ma_compared": listdata[k]["ma_compared"], "dis" : dis})

sorted_array = sorted(arrange_bydis, key=lambda x: x["dis"])

json_arr = []
for i in range(len(sorted_array)):
    for j in range(len(listdata)):
        if(sorted_array[i]["ma_compared"] == listdata[j]["ma_compared"]):
            formatted_number = locale.format_string("%0.2f", example_money * (1 + (listdata[j]["estimated_return"]/100)), grouping=True)
            json_arr.append({"ma_compared": listdata[j]["ma_compared"],"probability": listdata[j]["probability"],"estimated_return": listdata[j]["estimated_return"],"lost" : listdata[j]["lost"], "profit": listdata[j]["profit"], "biggest_profit" : listdata[j]["biggest_profit"], "biggest_lost": listdata[j]["biggest_lost"] , "estimated_return_in_money": formatted_number, "example_money_invested" : example_money})

print(json_arr)

