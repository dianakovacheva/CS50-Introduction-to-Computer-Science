from cs50 import get_float

quarters = 0.25 * 100
dimes = 0.10 * 100
nickels = 0.05 * 100
pennies = 0.01 * 100

quarters_count = 0
dimes_count = 0
nickels_count = 0
pennies_count = 0

money = 0
total_coins_count = 0

# Prompt the user for change owed, in cents.
while True:
    user_input = get_float("Change: ")
    if user_input > 0:
        money = round(user_input * 100)
        break

# Calculate how many quarters you should give customer. Subtract the value of those quarters from cents.
if money / quarters != 0:
    quarters_count += int(money / quarters)
    total_coins_count += quarters_count
    money -= quarters * quarters_count

# Calculate how many dimes you should give customer. Subtract the value of those dimes from remaining cents.
if money / dimes != 0:
    dimes_count += int(money / dimes)
    total_coins_count += dimes_count
    money -= dimes * dimes_count

# Calculate how many nickels you should give customer. Subtract the value of those nickels from remaining cents.
if money / nickels != 0:
    nickels_count += int(money / nickels)
    total_coins_count += nickels_count
    money -= nickels * nickels_count

# Calculate how many pennies you should give customer. Subtract the value of those pennies from remaining cents.
if money / pennies != 0:
    pennies_count += int(money / pennies)
    total_coins_count += pennies_count
    money -= pennies * pennies_count

# Print that sum
print(total_coins_count)