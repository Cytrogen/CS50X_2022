#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop each row
    for (int i = 0; i < height; i++)
    {
        // Loop each column
        for (int j = 0; j < width; j++)
        {
            // Calculate the average
            // Color grey RGB ~= (128,128,128) -> half
            double red = image[i][j].rgbtRed;
            double green = image[i][j].rgbtGreen;
            double blue = image[i][j].rgbtBlue;

            // Check50: have to round
            int average = round((red + green + blue) / 3);

            // Set the values
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop each row
    for (int i = 0; i < height; i++)
    {
        // Loop each column
        for (int j = 0; j < width; j++)
        {
            // Only swap half of the image
            if (j < (width / 2))
            {
                // Swap
                RGBTRIPLE *a = &image[i][j];
                RGBTRIPLE *b = &image[i][width - (j + 1)];
                RGBTRIPLE temp;
                temp = *a;
                *a = *b;
                *b = temp;
            }
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of the image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // Loop each row
    for (int i = 0; i < height; i++)
    {
        // Loop each column
        for (int j = 0; j < width; j++)
        {
            double redSum = 0;
            double blueSum = 0;
            double greenSum = 0;
            int count = 0;

            // Loop each row surrounds row i until it finishes looping the bottom row of row i
            // Example:
            // i = 2
            // k = 1; k++
            // k = 2; k++
            // k = 3; for loop function stops
            for (int k = i - 1; k <= i + 1; k++)
            {
                // Loop each column surrounds column j until it finishes looping the right row of column j
                // Same for the for loop above
                for (int l = j - 1; l <= j + 1; l++)
                {
                    // Target pixel can't have negative-th row and column
                    if (k >= 0 && l >= 0)
                    {
                        // Target pixel can't be outside of the image
                        // Note: i or j is smaller than height or width, therefore k or l
                        if (k < height && l < width)
                        {
                            // According to box blur, the new value of each pixel will be the average of the values of all the pixels surround it (also includes the current pixel itself)

                            // Add all the values in sum variables
                            redSum += copy[k][l].rgbtRed;
                            blueSum += copy[k][l].rgbtBlue;
                            greenSum += copy[k][l].rgbtGreen;
                            count++;
                        }
                    }
                }
            }
            // Average the sum values
            // Check50: have to round
            image[i][j].rgbtRed = round(redSum / count);
            image[i][j].rgbtBlue = round(blueSum / count);
            image[i][j].rgbtGreen = round(greenSum / count);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of the image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // Sobel Operator
    // 3x3 grid
    // computes the new value of each pixel by taking a weighted sum of the values for the surrounding pixels
    // two weighted sums:
    // Gx: detecting edges in the x direction
    // Gy: detecting edges in the y direction

    // Create two kernels
    int kernelGx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int kernelGy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    // Loop each row
    for (int i = 0; i < height; i++)
    {
        // Loop each column
        for (int j = 0; j < width; j++)
        {
            // Weighted sum of the RGB values in the x direction
            double redGx = 0;
            double greenGx = 0;
            double blueGx = 0;

            // Weighted sum of the RGB values in the x direction
            double redGy = 0;
            double greenGy = 0;
            double blueGy = 0;

            // x-th row in a 3x3 box
            // Note: corresponding value in a kernel
            int row = 0;

            // Loop each row surrounds row i until it finishes looping the bottom row of row i
            for (int k = i - 1; k <= i + 1; k++)
            {
                // x-th column in a 3x3 box
                int column = 0;

                // Loop each column surrounds column j until it finishes looping the right row of column j
                for (int l = j - 1; l <= j + 1; l++)
                {
                    // Target pixel can't have negative-th row and column
                    if (k >= 0 && l >= 0)
                    {
                        // Target pixel can't be outside of the image
                        if (k < height && l < width)
                        {
                            // Calculate Gx values
                            redGx += (kernelGx[row][column] * copy[k][l].rgbtRed);
                            greenGx += (kernelGx[row][column] * copy[k][l].rgbtGreen);
                            blueGx += (kernelGx[row][column] * copy[k][l].rgbtBlue);

                            // Calculate Gy values
                            redGy += (kernelGy[row][column] * copy[k][l].rgbtRed);
                            greenGy += (kernelGy[row][column] * copy[k][l].rgbtGreen);
                            blueGy += (kernelGy[row][column] * copy[k][l].rgbtBlue);
                        }
                    }
                    column++;
                }
                row++;
            }
            // Combine Gx values and Gy values
            double redSum = round(sqrt(pow(redGx, 2) + pow(redGy, 2)));
            double greenSum = round(sqrt(pow(greenGx, 2) + pow(greenGy, 2)));
            double blueSum = round(sqrt(pow(blueGx, 2) + pow(blueGy, 2)));

            // Set the values
            // The Sobel filter algorithm combines Gx and Gy into a final value by calculating the square root of Gx^2 + Gy^2
            // If xxxSum is greater than 255 then it will be 255, otherwise it's going to be xxxSum
            // Note: a = (b == 0) ? 1 : 0;
            image[i][j].rgbtRed = (redSum > 255) ? 255 : redSum;
            image[i][j].rgbtGreen = (greenSum > 255) ? 255 : greenSum;
            image[i][j].rgbtBlue = (blueSum > 255) ? 255 : blueSum;
        }
    }
    return;
}