Here is the English translation:

---

# Project Architecture

### API

The API is implemented using **Django Ninja (FastAPI-like)** — follow its style:

* `@router.get`, `@router.post`
* Pydantic models for request/response schemas
* automatic OpenAPI generation
* Data validation via **Pydantic v2.11**, not Django Forms/DRF
* Database access — **PostgreSQL 16** via `psycopg3`

Create **new models** by inheriting from `class BaseModel` in `core/models.py`.

---

# Rendering and Frontend

* Always use **Django Templates** to render HTML.
* **Bootstrap** — for UI styling (grid, buttons, forms, navigation, modals).
* **HTMX** — for interactivity:

  * partial HTML loading,
  * form handling,
  * DOM updates via `hx-get` / `hx-post` / `hx-target` / `hx-swap`.
* Do not use **React/Vue/Angular**.
* Server responses must be **HTML or HTML fragments**.
* Write JavaScript minimally; prefer built-in Bootstrap and HTMX features.

---

# 🔹 Code Style and Quality

You must always follow these tools and standards:

### ✦ Ruff

* Follow Ruff formatting and linting rules.
* Avoid unused imports, long lines, and messy constructions.

### ✦ Mypy

* Write correct type hints.
* Return strictly typed code.

### ✦ Pytest

* Test examples must use pytest style (functional tests, fixtures).
* Do not use Django TestCase.
* Write only what is applicable to a Django + Ninja + Pydantic project.

---

# 🔹 Dependencies

The project uses **uv**, therefore:

* Provide dependencies in the format:
  `uv add ...`
* Do not use `pip` in examples.

---

# Code and Patterns to Follow

* Use **asynchronous handlers** whenever possible with Django Ninja.
* Always separate:

  * API layer (Ninja),
  * services (pure business logic),
  * models (Django ORM).
* Use dataclasses or Pydantic models for passing data between layers.
* Use SQL only when ORM is insufficient.
* Explanations must be brief, structured, and preferably with examples.

---

# 🔹 Forbidden

* Suggesting **DRF**, **FastAPI**, **Flask**, or anything outside this stack.
* Using `pip` / `venv`.
* Using `psycopg2` or other incompatible libraries.
* Suggesting solutions outside a Docker-based workflow.

---
