# Development Standards

Project: AI Operating Agent (AOA)

Version: 1.0

---

# Table of Contents

1. Purpose

2. Engineering Principles

3. Git Workflow

4. Branch Strategy

5. Commit Convention

6. Coding Standards

7. Naming Convention

8. Folder Convention



# 1. Purpose

This document defines the engineering standards used throughout the AOA project.

The objective is to ensure consistency, maintainability, readability, and long-term scalability across the codebase.

All contributors should follow these standards.


# 2. Engineering Principles

Development should follow these principles.

## Simplicity

Keep implementations simple whenever possible.

---

## Readability

Code should prioritize readability over cleverness.

---

## Maintainability

Every component should be easy to modify without affecting unrelated modules.

---

## Scalability

Architectural decisions should support future growth.

---

## Testability

Components should be designed to support automated testing.

---

## Documentation

Important architectural decisions should always be documented.


# 3. Git Workflow

The project uses Git for version control.

Development follows a feature-based workflow.

Each major feature is developed independently before being merged into the main branch.


# 4. Branch Strategy

Main Branch

- main

Development Branch

- develop

Feature Branches

- feature/auth
- feature/chat
- feature/workflow
- feature/memory
- feature/rag

Bug Fixes

- fix/login
- fix/api

Hotfix

- hotfix/security


# 5. Commit Convention

Commit messages should follow a consistent format.

Examples:

feat: add authentication module

fix: resolve workflow execution bug

docs: update system architecture

refactor: improve execution engine

test: add unit tests

chore: update dependencies


# 6. Coding Standards

The project follows consistent coding practices.

General Rules:

- Write clean and readable code.
- Keep functions small and focused.
- Avoid duplicated logic.
- Prefer composition over inheritance.
- Use type hints whenever possible.
- Write meaningful variable names.
- Handle errors explicitly.
- Avoid hardcoded values.


# 7. Naming Convention

## Files

snake_case.py

example:

execution_engine.py

memory_service.py

---

## Classes

PascalCase

example:

ExecutionEngine

MemoryService

---

## Functions

snake_case

example:

create_employee()

execute_workflow()

---

## Variables

snake_case

example:

employee_id

workflow_name

execution_status

---

## Constants

UPPER_CASE

example:

MAX_RETRY

DEFAULT_TIMEOUT


# 8. Folder Convention

The project follows a modular folder structure.

Example:

app/

api/

core/

services/

agents/

workflows/

memory/

knowledge/

database/

models/

schemas/

utils/

tests/
