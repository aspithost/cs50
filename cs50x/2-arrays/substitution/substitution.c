#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

bool is_valid_length(string cipher);
bool is_valid_cipher(string cipher);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else
    {
        string cipher = argv[1];
        if (!is_valid_length(cipher))
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
        else
        {
            if (!is_valid_cipher(cipher))
            {
                return 1;
            }
            else
            {
                string input = get_string("plaintext: ");
                printf("ciphertext: ");
                for (int i = 0; input[i] != 0; i++)
                {
                    if (isupper(input[i]))
                    {
                        printf("%c", toupper(cipher[input[i] - 65]));
                    }
                    else if (islower(input[i]))
                    {
                        printf("%c", tolower(cipher[input[i] - 97]));
                    }
                    else
                    {
                        printf("%c", input[i]);
                    }
                }
                printf("\n");
            }
        }
    }
}

bool is_valid_length(string cipher)
{
    if (cipher[25] && cipher[26] == 0)
    {
        return true;
    }
    return false;
}

bool is_valid_cipher(string input)
{
    int cipher[26];
    for (int i = 0; i < 26; i++)
    {
        int character = input[i];
        if (isalpha(character))
        {
            character = toupper(character);
            if (cipher[character - 65])
            {
                printf("May only contain every letter once\n");
                return false;
            }
            else
            {
                cipher[character - 65] = 1;
            }
        }
        else
        {
            printf("Cipher may only contain letters\n");
            return false;
        }
    }
    return true;
}