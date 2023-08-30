#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // declare variable 'name'
    // receive input from user
    string name = get_string("What's your name?: ");
    // print user's input
    printf("Hello, %s!\n", name);
}