# 07 - Database Architecture & SQLAlchemy

## Overview
AI agents need memory, and applications need state. This section covers robust asynchronous database interactions using SQLAlchemy 2.0, the most powerful ORM in the Python ecosystem.

## Learning Objectives
1. **Async SQLAlchemy 2.0**: Setup an `AsyncEngine` and `AsyncSession` to interact with PostgreSQL without blocking the event loop.
2. **Bridging ORMs**: Learn patterns to seamlessly convert SQLAlchemy ORM objects into Pydantic models for API responses.
3. **Migrations**: Manage database schemas safely using Alembic.
4. **Performance Optimization**: Understand the N+1 query problem and solve it using `joinedload` and `selectinload`. Grasp connection pooling concepts.

## Suggested Practice
- Set up an async SQLite/PostgreSQL database, define a User model, and write async CRUD endpoints in FastAPI.
- Create an Alembic migration to add a new column to the User table without losing data.
