# 04 - Type Safety & Pydantic

## Overview
Python is dynamically typed, but modern production AI engineering requires strict type safety. This section covers advanced type hinting (up to Python 3.12) and Pydantic V2, the backbone of data validation in FastAPI and LangChain.

## Learning Objectives
1. **Advanced Typing (3.11/3.12)**: Master the new generics syntax (`class Box[T]:`), `Protocol` for duck-typing, `ParamSpec`, and the `Self` type.
2. **Static Analysis**: Understand how to configure and run `mypy` or `pyright`.
3. **Pydantic V2 Core**: Define robust `BaseModel`s, utilize complex `Field` configurations, and understand serialization.
4. **Custom Validation**: Implement `@field_validator` and `@model_validator` to enforce complex business logic on AI-generated outputs.

## Suggested Practice
- Write a purely static-typed function using `ParamSpec` to preserve the signature of a decorated function.
- Create a complex nested Pydantic model representing a JSON response expected from an LLM, and implement a custom validator that ensures specific semantic rules are met.
