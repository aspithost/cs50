// Check that a password has at least one lowercase letter, uppercase letter, number and symbol
// Practice iterating through a string
// Practice using the ctype library

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password))
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol\n");
    }
}

// TODO: Complete the Boolean function below
bool valid(string password)
{
    bool upper_case = false;
    bool lower_case = false;
    bool number = false;
    bool symbol = false;
    for (int i = 0; password[i] != 0; i++)
    {
        if (isdigit(password[i]))
        {
            number = true;
        }
        else if (islower(password[i]))
        {
            lower_case = true;
        }
        else if (isupper(password[i]))
        {
            upper_case = true;
        }
        else if (password[i] > 32)
        {
            symbol = true;
        }
    }
    if (upper_case && lower_case && number && symbol)
    {
        return true;
    }
    else
    {
        return false;
    }
}
