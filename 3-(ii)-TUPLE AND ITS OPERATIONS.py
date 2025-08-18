t=tuple(map(int, input("Enter numbers separated by space: ").split()))
print("Tuple elements:")
for i in t:
    print(i,end=",")
print("\nFirst element:",t[0])
print("Last element:",t[-1])
