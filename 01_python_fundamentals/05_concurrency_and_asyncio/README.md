# 05 - Concurrency & Asyncio

## Overview
Concurrency is the key to scaling AI backends. When your API needs to make thousands of slow network calls to OpenAI or Anthropic, synchronous code will fail. This section covers the intricacies of Python's concurrency model and `asyncio`.

## Learning Objectives
1. **The GIL**: Understand the Global Interpreter Lock, and when to use Multithreading vs Multiprocessing.
2. **Asyncio Core**: Grasp the Event Loop, Coroutines, Tasks, and Futures.
3. **Structured Concurrency (Python 3.11+)**: Master `asyncio.TaskGroup` to safely manage and cancel groups of asynchronous tasks.
4. **Exception Handling**: Use `ExceptionGroup` and `except*` to handle multiple concurrent failures gracefully.
5. **AI Use Cases**: Learn to throttle API requests using `asyncio.Semaphore`.

## Suggested Practice
- Write a script that hits an API endpoint 100 times synchronously, then rewrite it using `asyncio.gather` and compare execution times.
- Refactor the async script to use `asyncio.TaskGroup`, implementing a fallback mechanism if one of the tasks fails.
