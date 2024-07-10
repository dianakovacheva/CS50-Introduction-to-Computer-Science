from cs50 import get_string
import re

# Prompt the user for some text
user_input = get_string("Text: ")

# Count the number of letters, words, and sentences in the text
letters_count = len(re.findall(r'[a-zA-z]',user_input)) # Only alphabetic characters are counted as letters
words_count = len(user_input.split())
sentences_count = len(re.findall(r'[.!?]', user_input))

L = 0  # Average number of letters per 100 words in the text
S = 0  # Average number of sentences per 100 words in the text

L = letters_count / words_count * 100
S = sentences_count / words_count * 100


# Compute the Coleman-Liau index
index = round(0.0588 * L - 0.296 * S - 15.8)

# Print the grade level
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f'Grade {index}')