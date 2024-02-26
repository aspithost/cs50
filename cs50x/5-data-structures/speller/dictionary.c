// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <math.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 143091;

// Hash table
node *table[N];

// Counter
uint32_t counter = 0;

// bool check_word(node *current_node, const char *word);
void unloader(node *current_node);

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    uint16_t hash_int = hash(word);
    node *current_node = table[hash_int];

    while (current_node != NULL)
    {
        if (strcasecmp(current_node->word, word) == 0)
        {
            return true;
        }
        current_node = current_node->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    uint8_t length = strlen(word);

    uint32_t hash = 0;

    for (int i = 0; i < length; i++)
    {
        hash = (7 * hash + tolower(word[i])) % N;
    }

    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    char word[LENGTH + 1];

    while (fscanf(file, "%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            printf("Could not open %s.\n", dictionary);
            return false;
        }

        uint16_t hash_int = hash(word);

        // Copy word into new node
        strcpy(new_node->word, word);

        // Set pointer of new_node->next to first entry in table
        new_node->next = table[hash_int];

        // Set first entry pointer in table to new_node
        table[hash_int] = new_node;

        counter += 1;
    }
    fclose(file);
    return true;
}


// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            unloader(table[i]);
        }
    }
    // TODO
    return true;
}

void unloader(node *current_node)
{
    if (current_node->next != NULL)
    {
        unloader(current_node->next);
    }

    free(current_node);
}