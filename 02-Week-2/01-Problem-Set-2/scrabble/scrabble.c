#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

// int compareStrings(string stringOne, string stringTwo);
int countPoints(string word);

// bool isTheSame = false;

int main(void)
{
    // Prompt the user for two words
    string first_player_word = get_string("Player 1: ");
    string second_player_word = get_string("Player 2: ");

    // Compute the score of each word
    int first_player_score = countPoints(first_player_word);
    int second_player_score = countPoints(second_player_word);

    // isTheSame = compareStrings(first_player_word, second_player_word);

    // Print the winner

    // if (!isTheSame)
    // {
    if (first_player_score > second_player_score)
    {
        printf("%s\n", "Player 1 wins!\n");
    }
    else if (first_player_score < second_player_score)
    {
        printf("%s\n", "Player 2 wins!\n");
    }
    else
    {
        printf("%s\n", "Tie!");
    }
    // }
}

// int compareStrings(string stringOne, string stringTwo)
// {

//     if (strcmp(stringOne, stringTwo) == 0)
//     {
//         isTheSame = true;
//         return isTheSame;
//     }
//     else
//     {
//         isTheSame = false;
//         return isTheSame;
//     }
// }

int countPoints(string word)
{
    int stringLength = strlen(word);
    int pointsCount = 0;

    for (int i = 0; i < stringLength; i++)
    {

        if (isupper(word[i]))
        {
            pointsCount += points[word[i] - 'A'];
        }
        else if (islower(word[i]))
        {
            pointsCount += points[word[i] - 'a'];
        }
    }
    return pointsCount;
}
