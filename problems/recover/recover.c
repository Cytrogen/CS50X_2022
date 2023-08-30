#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *image = fopen(argv[1], "r");
    if (image == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // uint8_t = 8 bits or 1 byte
    // Buffer = 512 bytes
    uint8_t buffer[512];

    // A pointer to the file that will be written to
    FILE *finalImage = NULL;

    // Name of the JPEGs
    char fileName[8];

    // x-th JPEG found
    int count = 0;

    // Read and loop through all the 512-bytes
    while (fread(&buffer, 1, 512, image) == 512)
    {
        // From the walkthrough
        // If find the header of JPEG
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If it's not the first JPEG, close the previous finalImage
            // Note: JPEGs come one after another
            if (!(count == 0))
            {
                fclose(finalImage);
            }

            // From the walkthrough
            // Initialise a finalImage
            // Note: %03i = an integer with three digits
            // Note: count = the number that will turn to %03i
            sprintf(fileName, "%03i.jpg", count);
            finalImage = fopen(fileName, "w");
            count++;
        }

        // If JPEG found, write to finalImage
        if (!(count == 0))
        {
            fwrite(&buffer, 512, 1, finalImage);
        }
    }
    fclose(image);
    fclose(finalImage);

    return 0;
}