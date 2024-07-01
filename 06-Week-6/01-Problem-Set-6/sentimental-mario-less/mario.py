rows = 0
ask_number = True

while ask_number:
    height = input("Height: ")
    if height.isnumeric() and 0 < int(height) <= 8:
        height = int(height) #Convert string to number
        ask_number = False

spaceCount = height - 1
while rows < height:
    for i in range(spaceCount):
        print(" ", end="")
    for i in range(rows):
        print("#", end="")
    print("#")
    rows += 1
    spaceCount -= 1
