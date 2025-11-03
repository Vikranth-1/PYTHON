import pandas as pd
print("Default max rows setting:", pd.options.display.max_rows)

print("\nIf your DataFrame has more than this number of rows,")
print("pandas will display only the first and last 5 rows.\n")

pd.options.display.max_rows = 9999
print("New max rows setting:", pd.options.display.max_rows)

df = pd.read_csv('data.csv')

printf("Check the number of maximum returned rows:")

print("\nDisplaying DataFrame contents:\n")
print(df)
