#include <iostream>
#include <string>
#include <utility>

class Student {
private:
    std::string name;
    int rollNumber;
    double gpa;

public:
    // Constructor
    Student(std::string  studentName, int roll, double studentGpa)
        : name(std::move(studentName)), rollNumber(roll), gpa(studentGpa) {}

    // Getter methods
    std::string getName() const { return name; }
    int getRollNumber() const { return rollNumber; }
    double getGpa() const { return gpa; }

    // Setter methods
    void setGpa(double newGpa) {
        if (newGpa >= 0.0 && newGpa <= 4.0) {
            gpa = newGpa;
        }
    }

    // Display student details
    void display() const {
        std::cout << "Student Name: " << name 
                  << ", Roll Number: " << rollNumber 
                  << ", GPA: " << gpa << std::endl;
    }
};

int main() {
    Student student1("Deshraj Jogiya", 101, 3.8);
    student1.display();

    // Modifying details
    student1.setGpa(3.9);
    std::cout << "After GPA update:" << std::endl;
    student1.display();

    return 0;
}
