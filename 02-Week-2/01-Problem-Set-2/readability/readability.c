#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int countLetters(string input);
int countWords(string input);
int countSentences(string input);

int main(void)
{
    string input;

    do
    {
        // Prompt the user for some text
        input = get_string("Text: ");
    } while (isspace(input[0]) || ispunct(input[0])); // Will not start with a space

    // Count the number of letters, words, and sentences in the text
    int lettersCount = countLetters(input);
    int wordsCount = countWords(input);
    int sentencesCount = countSentences(input);

    float avg_num_of_letters =
        ((float)lettersCount / wordsCount) * 100; // Average number of letters per 100 words

    float avg_num_of_sentences =
        ((float)sentencesCount / wordsCount) * 100; // Average number of sentences per 100 words

    // Compute the Coleman-Liau index
    int index = round(0.0588 * avg_num_of_letters - 0.296 * avg_num_of_sentences - 15.8);

    // Print the grade level
    if (index > 16)
    {
        printf("%s\n", "Grade 16+");
    }
    else if (index < 1)
    {
        printf("%s\n", "Before Grade 1");
    }
    else
    {
        printf("%s%i\n", "Grade ", index);
    }
}

int countLetters(string input)
{
    int lettersCount = 0;
    int inputLength = strlen(input);

    if (inputLength)
    {

        for (int i = 0; i < inputLength; i++)
        {

            if (isalpha(input[i]))
            {
                lettersCount++;
            }
        }
    }
    return lettersCount;
}

int countWords(string input)
{
    int wordsCount = 0;
    int spacesCount = 0;
    int inputLength = strlen(input);

    if (inputLength)
    {
        for (int i = 0; i < inputLength; i++)
        {
            if (input[i] == ' ' && input[i + 1] != ' ')
            {
                spacesCount++;
            }
        }
    }

    wordsCount = spacesCount + 1;
    return wordsCount;
}

int countSentences(string input)
{
    int sentencesCount = 0;
    int inputLength = strlen(input);

    if (inputLength)
    {

        for (int i = 0; i < inputLength; i++)
        {
            if (input[i] == '.' || input[i] == '!' || input[i] == '?')
            {
                sentencesCount++;
            }
        }
    }

    return sentencesCount;
}