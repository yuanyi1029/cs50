#include <stdio.h>
#include <cs50.h>

// Try using int data type for x and y and input 2000000000 for both x and y
// Output will be -294967296 instead of 4000000000. This is integer overflow
// Integer overflow happens when the leftmost bit is carried over an extra place

// Example:
// max bits = 3,  maximum can count up to 111 (7)
// If we add an extra 1, we get 1000 but the leftmost bit is used to represent the sign of a number
// if max bits is 3, 1000 will represent -8 instead of 8

// Back to our case, the integer variable can only store between 294962796 and -294962796
// Therefore when adding 2 very large numbers, the sum exceeds the biggest number that the variable can store

// Solution: use long data type for variables




// Try inputing 1 for x and 3 for y -> Output will be 0.33333334326744079590
// This is floating point imprecision
// This occurs because there is a finite number of bits trying to represent an infinite number (0.3333333...)
// The computer will decide on how many bits to store the closest value of it, leading to imprecision


int main(void)
{
    long x = get_long("What's x? ");
    long y = get_long("What's y? ");

    printf("%li\n", x+y);

    float a = get_float("What's a? ");
    float b = get_float("What's b? ");

    printf("%.20f\n", a/b);
}