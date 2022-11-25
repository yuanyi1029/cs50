#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Defines a person data structure that contains a name and a number
typedef struct
{
    string name;
    string number;
}
person;


int main(void)
{
    // Define an array of persons of length 2
    person people[2];

    people[0].name = "Carter";
    people[0].number= "+1-617-495-1000";

    people[1].name= "David";
    people[1].number= "+1-949-468-2750";

    string name = get_string("Name: ");

    // Linear search - loop through all the names and try to find a specific name
    for (int i = 0; i < 2; i++)
    {
        if (strcmp(people[i].name, name) == 0)
        {
            printf("Found %s\n", people[1].number);
            return 0;
        }
    }
    printf("Not found\n");
    return 1;
}