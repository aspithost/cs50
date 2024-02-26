#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string text = get_string("Text: ");
    int letters = 0;
    int words = 1;
    int sentences = 0;
    int previous_character = 0;
    for (int i = 0; text[i] != 0; i++)
    {
        if (text[i] == 32)
        {
            words += 1;
        }
        else if (isalpha(text[i]))
        {
            letters += 1;
        }
        else if (text[i] == 33 || text[i] == 46 || text[i] == 63)
        {
            sentences += 1;
        }
        previous_character = text[i];
    }
    float result = 0.0588 * ((letters * 100.00) / words) - 0.296 * ((sentences * 100.00) / words) - 15.8;
    int rounded = round(result);
    if (result < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (rounded >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", rounded);
    }
}