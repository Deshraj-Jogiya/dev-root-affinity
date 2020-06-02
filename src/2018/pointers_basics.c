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

    // Array traversal using pointer arithmetic
    int arr[5] = {10, 20, 30, 40, 50};
    int *arr_ptr = arr; // Same as &arr[0]

    printf("Array traversal using pointers:\n");
    for (int i = 0; i < 5; i++) {
        printf("Element %d: %d\n", i, *(arr_ptr + i));
    }

    return 0;
}
