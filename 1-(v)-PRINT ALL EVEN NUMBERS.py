
n=int(input("Enter the max value:"))
for i in range(1, n+1):  
    if i % 2 != 0:  
        continue  
    print(i,end=",")  
