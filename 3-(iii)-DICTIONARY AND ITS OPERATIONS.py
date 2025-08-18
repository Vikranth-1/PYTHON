n = int(input("Enter number of key-value pairs: "))
di = {}
for j in range(n):
    k = input("Enter key: ")
    v = input("Enter value: ")
    di[k] = v
rk = input("Enter key to remove: ")
if rk in di:
    del di[rk]
print("Dictionary elements:")
for k, v in di.items():
    print(k,":",v,end=" , ")
