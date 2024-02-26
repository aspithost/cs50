#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    string word = get_string("Message: ");
    for (int i = 0; word[i] != 0; i++)
    {
        int binary[8];
        for (int j = 7; j >= 0; j--)
        {
            int remainder = word[i] % 2;
            if (remainder)
            {
                binary[j] = 1;
            }
            else
            {
                binary[j] = 0;
            }
            word[i] /= 2;
        }
        for (int k = 0; k < 8; k++)
        {
            print_bulb(binary[k]);
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
