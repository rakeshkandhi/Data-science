# 02 - Advanced Functions & Functional Programming

## Overview
Functions in Python are first-class citizens. This section covers advanced functional programming paradigms that allow you to write concise, modular, and highly reusable code—essential for creating flexible AI pipelines and API endpoints.

## Learning Objectives
1. **Closures & Scope**: Understand late binding and when to use `nonlocal`.
2. **Advanced Decorators**: Build decorators that accept arguments, preserve signatures using `functools.wraps`, and implement class-based decorators.
3. **Generators & Iterators**: Understand the difference between `yield` and `return`. Learn to use `yield from` and send data to generators.
4. **Functional Tools**: Master higher-order functions like `map`, `filter`, `reduce`, and `functools.partial`.

## Suggested Practice
- Write a parameterized retry decorator (e.g., `@retry(max_attempts=3)`) for wrapping unstable LLM API calls.
- Create a data processing pipeline using chained generators to lazily process a large simulated dataset without running out of memory.
