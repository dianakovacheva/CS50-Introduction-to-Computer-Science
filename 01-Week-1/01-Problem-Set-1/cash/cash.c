#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int change_in_cents;
    do
    {
        change_in_cents = get_int("Change owed: ");
    } while (change_in_cents < 0);

    const int quarters = 25;
    const int dimes = 10;
    const int nickels = 5;
    const int pennies = 1;

    int quarters_count = 0;
    int dimes_count = 0;
    int nickels_count = 0;
    int pennies_count = 0;

    int total_coins_count = 0;

    int sum_quarters = 0;
    int sum_dimes = 0;
    int sum_nickels = 0;
    int sum_pennies = 0;

    if (change_in_cents / quarters != 0)
    {
        // Calculate how many quarters you should give customer
        quarters_count = change_in_cents / quarters;
        total_coins_count += quarters_count;
        sum_quarters = quarters_count * quarters;
        // Subtract the value of those quarters from cents
        change_in_cents = change_in_cents - sum_quarters;
    }

    if (change_in_cents / dimes != 0)
    {
        // Calculate how many dimes you should give customer
        dimes_count = change_in_cents / dimes;
        total_coins_count += dimes_count;
        sum_dimes = dimes_count * dimes;
        // Subtract the value of those dimes from remaining cents
        change_in_cents = change_in_cents - sum_dimes;
    }

    if (change_in_cents / nickels != 0)
    {
        // Calculate how many nickels you should give customer
        nickels_count = change_in_cents / nickels;
        total_coins_count += nickels_count;
        sum_nickels = nickels_count * nickels;
        // Subtract the value of those nickels from remaining cents
        change_in_cents = change_in_cents - sum_nickels;
    }

    if (change_in_cents / pennies != 0)
    {
        // Calculate how many pennies you should give customer
        pennies_count = change_in_cents / pennies;
        total_coins_count += pennies_count;
        sum_pennies = pennies_count * pennies;
        // Subtract the value of those pennies from remaining cents
        change_in_cents = change_in_cents - sum_pennies;
    }

    // Print the sum of quarters, dimes, nickels, and pennies used
    printf("%i\n", total_coins_count);
}
