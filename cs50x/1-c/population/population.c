#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int start, end;
    do
    {
        start = get_int("Start size: ");
    }
    while (start < 9);

    do
    {
        end = get_int("End size: ");
    }
    while (end < start);

    int years = 0;
    if (end > start)
    {
        do
        {
            start += (start / 3) - (start / 4);
            years ++;
        }
        while (start < end);
    }

    printf("Years: %i\n", years);
}
