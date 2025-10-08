import pandas as pd
data = {
"calories": [420, 380, 390],
"duration": [50, 40, 45]
}
df = pd.DataFrame(data)
print("(i) Create a simple Pandas DataFrame:\n")
print(df)

print("\n(ii)Locate Row Program:\n")
print(df.loc[0])

print("\n(iii)use a list of indexes:\n")
print(df.loc[[0, 1]])
