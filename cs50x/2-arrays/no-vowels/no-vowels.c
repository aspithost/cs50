// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>

string replace(string word);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("ERROR\n");
        return 1;
    }
    else
    {
        printf("%s\n", replace(argv[1]));
    }
}

string replace(string word)
{
    int i = 0;
    int keyCode;
    do
    {
        keyCode = word[i];
        switch (keyCode)
        {
            case 65:
            case 97:
                word[i] = 54;
                break;
            case 69:
            case 101:
                word[i] = 51;
                break;
            case 73:
            case 105:
                word[i] = 49;
                break;
            case 79:
            case 111:
                word[i] = 48;
                break;
        }
        i += 1;
    }
    while (keyCode);
    return word;
}