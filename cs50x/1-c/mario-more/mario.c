#include <cs50.h>
#include <stdio.h>

void loop_and_print(int length, string val);

int main(void)
{
    int num;
    do
    {
        num = get_int("Height: ");
    }
    while (num < 1 || num > 8);

    for (int i = 1; i <= num; i++)
    {
        loop_and_print(num - i, " ");
        loop_and_print(i, "#");
        printf("  ");
        loop_and_print(i, "#");
        printf("\n");
    }
}

void loop_and_print(int length, string val)
{
    for (int i = 0; i < length; i ++)
    {
        printf("%s", val);
    }
}