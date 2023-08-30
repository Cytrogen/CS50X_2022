#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Declare function
int isNumber(string text);
char rotate(char digit, int keys);

// argc = argument count (number of words typed in)
// argv[] = argument vector (augument list)
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        int n = isNumber(argv[1]);

        // If the score does not match the len
        if (n != strlen(argv[1]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        else
        {
            // Declare key
            int k = atoi(argv[1]);

            // Prompt for user input
            string plainText = get_string("plaintext: ");

            printf("ciphertext: ");

            // Rotating the digit one by one
            for (int i = 0, len = strlen(plainText); i < len; i++)
            {
                char pt = rotate(plainText[i], k);
                printf("%c", pt);
            }
            printf("\n");
        }
    }
}

// Return score = len
int isNumber(string text)
{
    int score = 0;

    for (int i = 0, len = strlen(text); i < len; i++)
    {
        // If the digit is a digit (0 ~ 9)
        if (isdigit(text[i]))
        {
            score++;
        }
    }
    return score;
}

// Return the rotating digit one by one
char rotate(char digit, int keys)
{
    char rotated;
    int temp = 0;

    // If the digit is not a letter
    if (!isalpha(digit))
    {
        rotated = digit;
    }
    else
    {
        // Use a temporary integer to represent decimal ASCII
        temp = digit + keys;

        // If the digit is uppercase
        if (isupper(digit))
        {
            while (temp > 90)
            {
                temp -= 26;
            }
        }
        else
        {
            while (temp > 122)
            {
                temp -= 26;
            }
        }
        rotated = temp;
    }
    return rotated;
}