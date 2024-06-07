#include <cs50.h>
#include <stdio.h>
#include <string.h>

int get_digit(long input, int pos);
int get_long_length(long num);
int sum_digits(long num);

int main(void)
{
    long credit_card_num = get_long("Number: ");
    int credit_card_length = get_long_length(credit_card_num);

    int sum = 0;
    int num_length = get_long_length(credit_card_num);
    int curr_digit;
    int first_num;
    bool isInvalid = true;

    for (int i = 1; i <= num_length; i++)
    {
        curr_digit = get_digit(credit_card_num, i);
        if (i % 2 != 0)
        {
            sum += curr_digit;
        }
        else
        {
            sum += sum_digits(curr_digit * 2);
        }
    }

    first_num = get_digit(sum, 1);

    if (first_num != 0)
    {
        printf("%s\n", "INVALID");
        return 0;
    }

    int first_digit = get_digit(credit_card_num, credit_card_length);
    int second_digit = get_digit(credit_card_num, credit_card_length - 1);

    // American Express
    if (num_length == 15 && first_digit == 3)
    {
        if (second_digit == 4 || second_digit == 7)
        {
            printf("%s\n", "AMEX");
            isInvalid = false;
        }
    }
    // Mastercard
    if (num_length == 16 && first_digit == 5)
    {

        if (second_digit == 1 || second_digit == 2 || second_digit == 3 || second_digit == 4 ||
            second_digit == 5)
        {
            printf("%s\n", "MASTERCARD");
            isInvalid = false;
        }
    }

    if (num_length == 13 || num_length == 16)
    {
        if (first_digit == 4)
        {
            printf("%s\n", "VISA");
            isInvalid = false;
        }
    }

    if (isInvalid)
    {
        printf("%s\n", "INVALID");
    }

    return 0;
};

int get_digit(long input, int pos)
{
    int remainder;
    long temp = input;
    int counter = 1;

    while (counter <= pos)
    {
        remainder = temp % 10;
        if (remainder == 0 && temp < 10)
        {
            return temp;
        }
        if (counter == pos)
        {
            return remainder;
        }
        temp = (temp - remainder) / 10;
        counter++;
    }
    return -1;
}

int get_long_length(long num)
{
    long long_n = num;
    int counter = 0;

    while (long_n > 0)
    {
        long_n = long_n / 10;
        counter += 1;
    }
    return counter;
}

int sum_digits(long num)
{
    int sum = 0;
    int num_length = get_long_length(num);

    for (int i = 1; i <= num_length; i++)
    {
        sum += get_digit(num, i);
    }

    return sum;
}
