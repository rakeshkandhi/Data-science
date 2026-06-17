# 03 - Advanced Object-Oriented Programming

## Overview
Moving beyond basic classes and inheritance, this section dives into the complex object-oriented features of Python. These constructs are heavily utilized in advanced backend frameworks (like FastAPI) and ORMs (like SQLAlchemy).

## Learning Objectives
1. **Descriptor Protocol**: Understand how attributes are managed under the hood via `__get__`, `__set__`, and `__delete__`.
2. **Multiple Inheritance & MRO**: Master the C3 Linearization algorithm. Understand exactly how `super()` works in complex inheritance trees.
3. **Metaclasses**: Learn how class creation is intercepted using `__new__` and `__init_subclass__`.
4. **Modern Data Containers**: Compare and implement `dataclasses` vs traditional classes.

## Suggested Practice
- Implement a custom Descriptor that validates if an assigned attribute is an integer within a specific range.
- Create an intricate multiple inheritance diamond and trace the Method Resolution Order (MRO) programmatically.
- Use `__init_subclass__` to automatically register new subclass models into a central registry (a common pattern in AI agents/plugins).
