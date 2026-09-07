# 2026-09-07 AM — CSE Core (Medium)

## Question
What is a Virtual Table (vtable) and Virtual Table Pointer (vptr) in Object-Oriented Programming, and how do they enable Dynamic Polymorphism?

## Hint
Consider how the compiler determines which method implementation to call at runtime when a virtual function is invoked via a base class pointer.

## Answer
A Virtual Table (vtable) is a static lookup table of function pointers created by the compiler for every class containing or inheriting at least one virtual function. Each instance of such a class contains a hidden pointer, the Virtual Table Pointer (vptr), which points to the corresponding vtable for that object's dynamic type. When a virtual function is called through a base class pointer or reference at runtime, the program dereferences the object's vptr to find its vtable and retrieves the specific function address to execute. This mechanism, known as dynamic dispatch, enables runtime polymorphism at the cost of a small memory overhead (vptr per object, vtable per class) and slight execution latency due to pointer dereferencing.
