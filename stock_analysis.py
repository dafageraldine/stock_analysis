import pandas as pd

# Read the stock data into a Pandas DataFrame
df = pd.read_csv('AAPL_data.csv')  # Replace 'stock_data.csv' with the path to your data file

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

ma = 'MA'
lowerma = ma + '10'
higherma =  ma + '50'

# Print the DataFrame with moving averages
# print(df)

# df['Crossing'] = None
# for i in range(1, len(df)):
#     if df['MA5'].iloc[i] > df['MA10'].iloc[i] and df['MA5'].iloc[i - 1] < df['MA10'].iloc[i - 1]:
#         df.loc[i, 'Crossing'] = 'MA5 crossing above MA10'
#     elif df['MA5'].iloc[i] < df['MA10'].iloc[i] and df['MA5'].iloc[i - 1] > df['MA10'].iloc[i - 1]:
#         df.loc[i, 'Crossing'] = 'MA5 crossing below MA10'

# Print the DataFrame with MA crossings
# print(df[['date', 'close', 'MA5', 'MA10', 'Crossing']])

# crossings = []
# for i in range(1, len(df)):
#     if df['MA5'].iloc[i] > df['MA10'].iloc[i] and df['MA5'].iloc[i - 1] < df['MA10'].iloc[i - 1]:
#         crossings.append((df['date'].iloc[i], 'MA5 crossing above MA10'))
#     elif df['MA5'].iloc[i] < df['MA10'].iloc[i] and df['MA5'].iloc[i - 1] > df['MA10'].iloc[i - 1]:
#         crossings.append((df['date'].iloc[i], 'MA5 crossing below MA10'))

# # Print the crossing data
# for crossing in crossings:
#     print(crossing)

# Initialize the 'Signal' column with 'Hold' for no action
# df['Signal'] = 'Hold'

# # Identify buy signals (MA5 crossing above MA10)
# buy_indices = df[(df['MA5'] > df['MA10']) & (df['MA5'].shift(1) < df['MA10'].shift(1))].index
# df.loc[buy_indices, 'Signal'] = 'Buy'

# # Identify sell signals (MA5 crossing below MA10)
# sell_indices = df[(df['MA5'] < df['MA10']) & (df['MA5'].shift(1) > df['MA10'].shift(1))].index
# df.loc[sell_indices, 'Signal'] = 'Sell'

# # Print the DataFrame with signals
# print(df[['date', 'close', 'MA5', 'MA10', 'Signal']])

# Initialize the 'Signal' column with 'Hold' for no action
df['Signal'] = 'Hold'

# Identify buy signals (MA5 crossing above MA10)
buy_indices = df[(df[lowerma] > df[higherma]) & (df[lowerma].shift(1) < df[higherma].shift(1))].index
df.loc[buy_indices, 'Signal'] = 'Buy'

# Identify sell signals (MA5 crossing below MA10)
sell_indices = df[(df[lowerma] < df[higherma]) & (df[lowerma].shift(1) > df[higherma].shift(1))].index
df.loc[sell_indices, 'Signal'] = 'Sell'

# Filter and print only the rows with buy and sell signals
filtered_df = df[df['Signal'].isin(['Buy', 'Sell'])]
# print(filtered_df[['date', 'close', 'MA20', 'MA50', 'Signal']])

# Initialize the 'Signal' column with 'Hold' for no action
# df['Signal'] = 'Hold'

# # Identify buy signals (MA5 crossing above MA10)
# buy_indices = df[(df['MA5'] > df['MA10']) & (df['MA5'].shift(1) < df['MA10'].shift(1))].index
# df.loc[buy_indices, 'Signal'] = 'Buy'

# # Identify sell signals (MA5 crossing below MA10)
# sell_indices = df[(df['MA5'] < df['MA10']) & (df['MA5'].shift(1) > df['MA10'].shift(1))].index
# df.loc[sell_indices, 'Signal'] = 'Sell'

# # Filter the data within the specified date range
# start_date = pd.to_datetime('2018-01-08 00:00:00')
# end_date = pd.to_datetime('2018-01-25 00:00:00')
# filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# # Print the filtered data
# print(filtered_df[['date', 'close', 'MA5', 'MA10', 'Signal']])

# Calculate estimated returns
previous_buy_index = None
estimated_returns = []
for index, row in df.iterrows():
    if row['Signal'] == 'Buy':
        previous_buy_index = index
    elif row['Signal'] == 'Sell' and previous_buy_index is not None:
        buy_close = df.loc[previous_buy_index, 'close']
        sell_close = row['close']
        estimated_return = (sell_close - buy_close) / buy_close
        estimated_returns.append(estimated_return)

# Print the estimated returns
# print("Estimated Returns:")
returnall = 0
lost = 0
profit = 0
for i, return_value in enumerate(estimated_returns, start=1):
    # print(f"Trade {i}: {return_value:.2%}")
    returnall = returnall + return_value
    if(return_value < 0):
        lost = lost + 1
    elif(return_value > 0):
        profit = profit + 1

print("all return calculated : " + str(returnall))
print("lost : " + str(lost) + " profit : " + str(profit) + " prosentase " + str(profit/(profit+lost) * 100))