import pandas as pd

df = pd.read_csv('List Emiten/all.csv')

for i in range(len(df)):
    print(df["code"][i] + " " + df["name"][i])