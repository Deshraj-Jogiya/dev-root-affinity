# C++ Object-Oriented Programming: Classes & Objects

Object-Oriented Programming (OOP) is a paradigm centered around objects rather than actions, and data rather than logic. This note explores classes, objects, and the concept of encapsulation.

## Key Concepts

1. **Class**: A user-defined blueprint or prototype from which objects are created. It groups attributes (data members) and methods (member functions) together.
2. **Object**: A self-contained unit of a class containing actual values.
3. **Encapsulation**: The practice of hiding internal details of an object and exposing only necessary operations via public methods. This prevents direct access to data members and protects state integrity.

## Access Specifiers
- `private`: Accessible only inside the class itself. Used for data members to ensure encapsulation.
- `public`: Accessible from anywhere outside the class. Used for interface methods/constructors.
- `protected`: Accessible within the class and by derived classes.

## Code Example
Below is an example of encapsulation and constructors in C++. See the full executable file at [oop_classes.cpp](file:///G:/dev-root-affinity/src/2018/oop_classes.cpp).

```cpp
#include <iostream>
#include <string>

class Student {
private:
    std::string name;
    int rollNumber;
    double gpa;

public:
    // Constructor with initializer list
    Student(std::string studentName, int roll, double studentGpa)
        : name(studentName), rollNumber(roll), gpa(studentGpa) {}

    // Public getters to access private variables safely
    std::string getName() const { return name; }
    
    // Setter with validation logic to maintain integrity
    void setGpa(double newGpa) {
        if (newGpa >= 0.0 && newGpa <= 4.0) {
            gpa = newGpa;
        }
    }
};
```

---
*Logged on 2018-05-21 10:35:00 (UTC)*
