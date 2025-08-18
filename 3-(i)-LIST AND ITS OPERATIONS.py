li=list(map(int, input("Enter numbers separated by space: ").split()))
li.append(int(input("Enter number to append: ")))
li.insert(int(input("Insert position: ")), int(input("Value to insert: ")))
li.remove(int(input("Enter number to remove: ")))
print("Popped element:",li.pop())
print("List elements:")
for i in li:
    print(i,end=",")
