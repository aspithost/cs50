#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 3)
    {
        printf("usage : ./reverse sync.wav reverse.wav\n");
        return 1;
    }

    // Open input file for reading
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Read header
    WAVHEADER header;
    fread(&header, sizeof(WAVHEADER), 1, input);
    long header_length = ftell(input);

    // Use check_format to ensure WAV format
    check_format(header);

    // Open output file for writing
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Write header to file
    fwrite(&header, sizeof(WAVHEADER), 1, output);

    // Use get_block_size to calculate size of block
    int block_size = get_block_size(header);

    // Write reversed audio to file
    char buffer[block_size];
    fseek(input, (-1 * block_size), SEEK_END);

    while (ftell(input) >= header_length)
    {
        fread(&buffer, block_size, 1, input);
        fwrite(&buffer, block_size, 1, output);
        fseek(input, (-2 * block_size), SEEK_CUR);
    }

    fclose(input);
    fclose(output);
}

int check_format(WAVHEADER header)
{
    char header_type[block_size + 1];

    for (int i = 0; i < block_size; i++)
    {
        header_type[i] = header.format[i];
    }
    header_type[block_size] = '\0';

    if (strcmp(header_type, "WAVE") == 0)
    {
        return 0;
    }
    else
    {
        return 1;
    }
}

int get_block_size(WAVHEADER header)
{
    // TODO #7
    int bytesPerSample = header.numChannels * header.bitsPerSample / 8;
    return bytesPerSample;
}
