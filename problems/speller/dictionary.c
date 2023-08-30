// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
// const unsigned int N = 26;
const unsigned int N = 100;
unsigned int hashValue;
unsigned int count;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // Hash the word and access the linked list
    int hashValueCheck = hash(word);
    node *n = table[hashValueCheck];

    // If n exists
    while (n)
    {
        // If the word matches
        if (strcasecmp(word, n->word) == 0)
        {
            return true;
        }
        n = n->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int number = 0;

    // Loop all the words
    for (int i = 0; i < strlen(word); i++)
    {
        // Add up the ASCII values
        number += tolower(word[i]);
    }
    // return toupper(word[0]) - 'A';
    return number % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Open dictionary file
    FILE *dict = fopen(dictionary, "r");
    // Return false if fail
    if (dict == NULL)
    {
        return false;
    }

    // Initialise word array
    char word[LENGTH + 1];

    // Scan all the strings from the dictionary file
    while (fscanf(dict, "%s", word) != EOF)
    {
        // Allocate memory for each word
        node *n = malloc(sizeof(node));
        // If malloc fails
        if (n == NULL)
        {
            return false;
        }

        // Copy word into node
        strcpy(n->word, word);
        // Hash the word -> hash value
        hashValue = hash(word);

        // Set pointer
        n->next = table[hashValue];
        table[hashValue] = n;

        // Increase the word count
        count++;
    }

    // Close file
    fclose(dict);

    // return false;
    // As the file is loaded, return true
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    // count is the word count
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];
        // If n is not NULL, free the current n
        while (n)
        {
            node *temp = n;
            n = n->next;
            free(temp);
        }

        // If n is NULL
        if (i == N - 1 && n == NULL)
        {
            // The dictionary is unloaded successfully from the memory
            return true;
        }
    }
    return false;
}
