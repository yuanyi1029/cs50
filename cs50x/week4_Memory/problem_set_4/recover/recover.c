
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Declare Byte, image_pointer, image count, buffer, filename
    typedef uint8_t BYTE;
    FILE *ipointer = NULL;
    int count = 0;
    BYTE buffer[512];
    char filename[8 * sizeof(BYTE)];

    // Return 1 if 2 arguments are not given
    if (argc != 2)
    {
        printf("Usage: ./recover card.raw");
        return 1;
    }

    // Define the file pointer to point to the file
    FILE *fpointer = fopen(argv[1], "r");

    // Return 1 if fpointer returns NULL (something went wrong)
    if (fpointer == NULL)
    {
        printf("Unable to open file");
        return 1;
    }

    // Repeat until fread does not return 8 * 512 (end of file)
    while (fread(buffer, 1, sizeof(BYTE) * 512, fpointer) == sizeof(BYTE) * 512)
    {
        // Check the first 4 bytes for a JPEG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {

            // Determine filename, open a file and increase count by 1  
            sprintf(filename, "%03i.jpg", count);
            ipointer = fopen(filename, "w");
            count++;
        }

        // Write buffer to file if file pointer does not return NULL
        if (ipointer != NULL)
        {
            fwrite(buffer, 1, sizeof(BYTE) * 512, ipointer);
        }

    }
    
    fclose(ipointer);
    fclose(fpointer);

    return 0;
}
