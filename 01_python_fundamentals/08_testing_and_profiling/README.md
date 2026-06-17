# 08 - Testing & Profiling

## Overview
Production AI systems must be rigorously tested and profiled for performance bottlenecks. This section ensures your code is reliable, testable, and efficient before deployment.

## Learning Objectives
1. **Pytest Fundamentals**: Master advanced fixtures, scopes, and test parameterization. Use `pytest-asyncio` for async endpoints.
2. **Mocking**: Use `unittest.mock.patch` to isolate units of code.
3. **Testing AI Workflows**: Learn to use `pytest-httpx` or `respx` to mock external API calls (like OpenAI) so tests run instantly and without API costs.
4. **Profiling**: Use `cProfile` and `py-spy` to find CPU bottlenecks, and `memory_profiler` to trace memory leaks.

## Suggested Practice
- Write a suite of `pytest` functions to test a FastAPI endpoint, using fixtures to spin up an in-memory test database.
- Use `respx` to mock a call to an external LLM provider, testing how your application handles a simulated 500 Server Error or Timeout.
