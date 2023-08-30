#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long x;
    int count = 0;

    // Prompt user for input
    x = get_long("Number: ");

    // Get digits
    count = 0;
    long n = x;
    while (n != 0)
    {
        n /= 10;
        count++;
    }

    int doubleSum = 0;
    int singleSum = 0;
    long y = x;

    // Representing the digits that will be doubled, and the digits that will not be doubled
    int doubleDigit;
    int singleDigit;

    // For double digits
    int dTen;
    int dOne;

    do
    {
        // Starting from the last digit
        // Remove the last digit
        singleDigit = y % 10;
        y /= 10;
        singleSum += singleDigit;

        // Going to the 2nd last digit
        // Remove the 2nd last digit
        // Double the 2nd last digit
        doubleDigit = y % 10;
        y /= 10;
        doubleDigit *= 2;

        // Separare the digit with tens place
        dTen = doubleDigit % 10;
        dOne = doubleDigit / 10;
        doubleSum += dTen + dOne;

        // Repeat all of the above and get
    }
    while (y > 0);

    // Get the last digit of the finalSum
    // Test is the number valid
    int finalSum = singleSum + doubleSum;
    finalSum %= 10;
    if (finalSum == 0)
    {
        // Representing the two head digits
        // Keep dividing by 10 until there's only two digits left
        long startDigit = x;
        do
        {
            startDigit /= 10;
        }
        while (startDigit > 100);

        // Test card type:
        //     AMEX: 15; 34, 37
        //     MASTERCARD: 16; 51, 52, 53, 54, 55
        //     VISA: 13, 16; 4
        if ((count == 15) && (startDigit == 34 || startDigit == 37))
        {
            printf("AMEX\n");
        }
        else if ((count == 13 || count == 16) && (startDigit >= 40 && startDigit <= 49))
        {
            printf("VISA\n");
        }
        else if ((count == 16) && (startDigit >= 51 && startDigit <= 55))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}