#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

bool start_of_jpeg(uint8_t buffer[]);

int main(int arygc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover namefile\n");
        return 1;
    }

    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        printf("Something went wrong opening the file\n");
        return 1;
    }

    typedef uint8_t BYTE;
    const uint16_t BLOCK_SIZE = 512;
    BYTE buffer[BLOCK_SIZE];

    char file_address[8];

    uint8_t counter = 0;
    FILE *image = NULL;

    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, inptr))
    {
        if (!start_of_jpeg(buffer) && counter > 0)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, image);
        }
        else if (start_of_jpeg(buffer))
        {
            if (counter > 0)
            {
                fclose(image);
            }

            sprintf(file_address, counter < 10 ? "00%u.jpg" : "0%u.jpg", counter);

            image = fopen(file_address, "w");
            if (image == NULL)
            {
                printf("Something went wrong opening the file\n");
                return 1;
            }

            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, image);
            counter += 1;
        }
    }

    fclose(inptr);
    fclose(image);
}

bool start_of_jpeg(uint8_t buffer[])
{
    if (buffer[0] == 255 && buffer[1] == 216 && buffer[2] == 255 && buffer[3] < 223 && buffer[3] < 240)
    {
        return true;
    }
    return false;
}