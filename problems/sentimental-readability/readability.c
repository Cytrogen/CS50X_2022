#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// Declare the function
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Prompt for user input
    string x = get_string("Text: ");

    // Get the numbers of letters, words, and sentences
    int letters = count_letters(x);
    float words = count_words(x);
    int sentences = count_sentences(x);

    // Calculate the average number of letters and sentences
    float wordToHund = 100 / words;
    float l = letters * wordToHund;
    float s = sentences * wordToHund;

    // Coleman-Liau index
    float index = 0.0588 * l - 0.296 * s - 15.8;
    int grade = round(index);

    if (grade <= 0)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

// Return the number of letters in user input
int count_letters(string text)
{
    int letter = 0;

    // Get the digits one by one
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        // If the digit is a letter
        if (isalpha(text[i]))
        {
            letter++;
        }
    }
    return letter;
}

// Return the number of words in user input
int count_words(string text)
{
    int word = 0;

    // Get the digits one by one
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        // If the digit is a whitespace
        if (isspace(text[i]))
        {
            word++;
        }
    }

    // (word.number) = (white space.number) + 1
    word += 1;
    return word;
}

// Return the number of sentences in user input
int count_sentences(string text)
{
    int sentence = 0;

    // Get the digits one by one
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        // If the digit is a period, an exclamation point, or a question mark
        if ((text[i] == '.') || (text[i] == '!') || (text[i] == '?'))
        {
            sentence++;
        }
    }
    return sentence;
}