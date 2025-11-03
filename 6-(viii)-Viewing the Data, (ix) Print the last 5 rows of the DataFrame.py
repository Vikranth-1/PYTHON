import pandas as pd
df = pd.read_csv('data.csv')
print("(vii) Viewing the Data")
print(df.head(4))
printf("(viii) Print the last 5 rows of the DataFrame:")
print(df.tail())
print(df.info())
