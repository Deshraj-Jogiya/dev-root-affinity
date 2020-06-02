# Understanding C Pointers

Pointers are fundamental variables in C that store the memory address of another variable. This note outlines basic pointer syntax, dereferencing, and passing arguments by reference.

## Memory Addresses & Pointer Declaration
In C, the address-of operator `&` retrieves the memory address of a variable. A pointer is declared using the asterisk symbol `*`.

```c
#include <stdio.h>

void increment(int *value) {
    *value = *value + 1; // Dereferencing the pointer to modify the original variable
}

int main() {
    int score = 95;
    int *ptr = &score; // Store the memory address of score

    printf("Score value: %d\n", score);
    printf("Score memory address: %p\n", (void*)&score);
    printf("Pointer stored address: %p\n", (void*)ptr);
    printf("Value at stored address (dereferenced): %d\n", *ptr);

    // Call by reference
    increment(&score);
    printf("Score after increment: %d\n", score);

    return 0;
}
```

## Pointers & Arrays
An array name in C acts as a constant pointer pointing to the first element of the array. We can use pointer arithmetic to traverse array elements efficiently:

```c
int arr[5] = {10, 20, 30, 40, 50};
int *arr_ptr = arr; // Same as &arr[0]

for (int i = 0; i < 5; i++) {
    printf("Element %d: %d\n", i, *(arr_ptr + i));
}
```
