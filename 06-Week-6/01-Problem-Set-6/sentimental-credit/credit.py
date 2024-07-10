from cs50 import get_int

is_valid_input = True
card_number = ""

# Prompt the user for input
while is_valid_input:
    user_input = get_int("Number: ")
    if user_input > 0 and len(str(user_input)) >= 13:
        card_number = str(user_input)
        break
    else:
        is_valid_input = False
        print("INVALID")

# Check for card length and starting digits
card_number_list = list(card_number)

# convert list members to integers
# card_number_list = [int(x) for x in card_number_list]

# MASTERCARD
if len(card_number) == 16 and card_number_list[0] == "5":
    if card_number_list[1] == "1" or card_number_list[1] == "2" or card_number_list[1] == "3" or card_number_list[1] == "4" or card_number_list[1] == "5":
        print("MASTERCARD")
    else:
        print("INVALID")

# AMEX
if len(card_number) == 15 and card_number_list[0] == "3":
    if card_number_list[1] == "4" or card_number_list[1] == "7":
        print("AMEX")
    else:
        print("INVALID")

# VISA
# Get all second to last digits
second_to_last_digit = card_number[len(card_number) - 2:None:-2]
result_multiplied_second_to_last_digit = ""

for num in second_to_last_digit:
    multiplied_num = int(num) * 2
    result_multiplied_second_to_last_digit += str(multiplied_num)

sum_of_multiplied_second_to_last_digit = 0

for num in result_multiplied_second_to_last_digit:
    sum_of_multiplied_second_to_last_digit += int(num)

# Get the digits of the card_num that weren't multiplied by 2
rest_digits = card_number[(len(card_number) - 1):None:-2]

sum_of_rest_digits = 0

for num in rest_digits:
    sum_of_rest_digits += int(num)

# Calculate check_sum
check_sum = second_to_last_digit = sum_of_multiplied_second_to_last_digit + sum_of_rest_digits

# Check if the last digit of check_sum is equal to 0
check_sum_to_string = str(check_sum)

# Print result
if len(card_number) == 13 or len(card_number) == 16 and card_number_list[0] == "4":
    if int(check_sum_to_string[len(check_sum_to_string) - 1]) == 0:
        print("VISA")
    else:
        print("INVALID")