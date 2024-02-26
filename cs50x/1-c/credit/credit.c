#include <cs50.h>
#include <stdio.h>

// bool is_valid_creditcard(int card);
int get_length(long num);
bool check_valid_length(int length);
int get_checksum(int length, long num);
int get_remainder_digit(long n, int nth_digit);

int main(void)
{
    long credit_card = get_long("Number: ");

    int length = get_length(credit_card);

    bool valid_length = check_valid_length(length);

    if (valid_length)
    {
        int checksum = get_checksum(length, credit_card);
        if (!(checksum % 10))
        {
            int first_digit = get_remainder_digit(credit_card, 1);
            if (first_digit == 4 && (length == 13 || length == 16))
            {
                printf("VISA\n");
            }
            else if (first_digit == 3 || first_digit == 5)
            {
                int second_digit = get_remainder_digit(credit_card, 2);
                if (first_digit == 3 && (second_digit == 4 || second_digit == 7))
                {
                    printf("AMEX\n");
                }
                else if (first_digit == 5 && (second_digit > 0 && second_digit < 6))
                {
                    printf("MASTERCARD\n");
                }
                else
                {
                    printf("INVALID\n");
                }
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

// amex = 15; 34 && 37
// master = 16; 51-55
// visa = 13 || 16; 4

int get_checksum(int length, long num)
{
    int counter = 0;
    int checksum = 0;
    for (int i = length; i > 0; i --)
    {
        int integer = num % 10;
        if (counter % 2)
        {
            int doubled = integer * 2;
            if (doubled >= 10)
            {
                checksum += (doubled % 10) + 1;
            }
            else
            {
                checksum += doubled;
            }
        }
        else
        {
            checksum += integer;
        }
        counter ++;
        num /= 10;
    }
    return checksum;
}

int get_length(long num)
{
    int count = 0;
    do
    {
        num /= 10;
        count ++;
    }
    while (num > 0);
    return count;
}

bool check_valid_length(int length)
{
    if (length < 13 || length == 14 || length > 16)
    {
        return false;
    }
    return true;
}

int get_remainder_digit(long n, int nth_digit)
{
    int remainder = 1;
    for (int i = 0; i < nth_digit; i++)
    {
        remainder *= 10;
    }
    do
    {
        n /= 10;
    }
    while (n > (remainder));
    return n % 10;
}