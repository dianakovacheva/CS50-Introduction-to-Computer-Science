isNumber = True

while isNumber:
    height = input("Height: ")
    if height.isnumeric() and 0 < int(height) <= 8:
        isNumber = False

height = int(height)
spaceCount = height - 1

# Left side
for i in range(height):  # Rows
    for j in range(spaceCount):  # Spaces before each element
        print(" ", end="")
    for k in range(i+1):  # Elements each row
        print("#", end="")
    print("  ", end="")
    for j in range(i+1):
        print("#", end="")
    print()
    spaceCount -= 1