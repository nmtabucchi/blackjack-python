# AGENTS.md - Blackjack Python Project

A Python learning course project with a FastAPI backend implementing a Blackjack game API and MongoDB database.

## Project Structure

```
blackjack-python/
├── Basic/                    # Python fundamentals (00-13)
├── Intermediate/             # Intermediate Python (00-08)
├── Backend/
│   └── FastAPI/
│       ├── main.py           # FastAPI app entry point
│       ├── requirements.txt   # Dependencies
│       ├── negocio/           # Business logic layer
│       │   ├── models/        # Pydantic models
│       │   └── dto/           # Data transfer objects
│       ├── dataBase/          # Database layer
│       │   ├── client.py      # MongoDB client
│       │   └── schemas/       # Database schemas
│       ├── routers/           # API route handlers
│       │   ├── users_db.py   # User CRUD endpoints
│       │   └── blackjack/     # Blackjack game endpoints
│       └── tests/             # Unit tests
└── collection - postman/      # API documentation
```

## Build/Lint/Test Commands

### Running Tests

Tests use Python's built-in `unittest` with FastAPI's `TestClient`.

```bash
# Run all tests
python -m unittest discover -s Backend/FastAPI/tests -v

# Run specific test file
python -m unittest Backend/FastAPI/tests/tests_blackjack.py -v

# Run specific test class
python -m unittest Backend.FastAPI.tests.tests_blackjack.TestBlackjackV2 -v

# Run single test method
python -m unittest Backend.FastAPI.tests.tests_blackjack.TestBlackjackV2.test_hit -v

# Run single test from file
python -m unittest Backend/FastAPI/tests/tests_blackjack.py::TestBlackjackV2::test_hit -v
```

### Running the Backend

```bash
# Install dependencies
pip install -r Backend/FastAPI/requirements.txt

# Run with uvicorn
cd Backend/FastAPI
uvicorn main:app --reload

# Run with fastapi CLI
cd Backend/FastAPI
fastapi dev main.py
```

### Running Lessons

```bash
# Run basic lesson
python Basic/11_classes.py

# Run intermediate lesson
python Intermediate/04_lambdas.py
```

## Code Style Guidelines

### General Style

- **Python Version**: 3.10+
- **Indentation**: 4 spaces (no tabs)
- **Line Length**: ~120 characters max
- **Language**: Spanish for comments and error messages (project convention)

### Type Hints

Use type hints for function parameters and return values:

```python
# Good - with type hints
def calcular_puntos(cartas: list[dict]) -> int:
    return sum(c["puntos"] for c in cartas)

async def new_game(dni: int) -> dict[str, str]:
    ...

# Avoid - missing type hints
def calcular_puntos(cartas):
    ...
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Variables | snake_case | `user_id`, `puntos_jugador` |
| Functions | snake_case | `calcular_puntos()`, `search_user()` |
| Classes | PascalCase | `Person`, `TestBlackjackV2` |
| Constants | UPPER_SNAKE | `VALORES`, `PALOS` |
| Private vars | double underscore | `__name` |

### Import Organization

Organize imports in three groups with blank lines between:

```python
# Standard library
from uuid import uuid4
import random

# Third-party libraries
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from bson import ObjectId

# Local application imports
from db.models.user import User
from db.schemas.user import user_schema
```

### Pydantic Models

Use Pydantic `BaseModel` for data validation:

```python
from pydantic import BaseModel

class User(BaseModel):
    uuid: str | None = None
    dni: int
    username: str
    saldo: float = 20000.0
```

### FastAPI Router Pattern

```python
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/v2/blackjack",
    tags=["Black Jack v2"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

@router.post("/new-game")
async def new_game(dni: int):
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no existe"
        )
    return {"user_id": user_id, "mensaje": "Partida creada"}
```

### Error Handling

- Use `HTTPException` for API errors with appropriate status codes
- Use `try/except` for database operations
- Return error messages in Spanish

```python
try:
    user = db_client.users.find_one({field: key})
    return User(**user_schema(user))
except:
    return {"error": "No se ha encontrado el usuario"}
```

### List/Dict Comprehensions

Use comprehensions for creating collections:

```python
# List comprehension
ases = sum(1 for c in cartas if c["valor"] == "A")

# Nested list comprehension
mazo = [
    {"valor": v, "palo": p, "puntos": pts}
    for v, pts in valores.items()
    for p in palos
]
```

### Comments

- Explain the "why", not the "what"
- Use Spanish throughout (project convention)
- Use docstrings for complex functions

```python
def calcular_puntos(cartas):
    """Calcula los puntos de una mano de Blackjack."""
    # Cuenta cuántos Ases hay en la mano
    ases = sum(1 for c in cartas if c["valor"] == "A")
```

### Testing Conventions

- Test class names: `Test<FeatureName>`
- Test method names: `test_<description>`
- Use `setUpClass` for shared fixtures
- Test file naming: `tests_<entity>.py`

```python
class TestBlackjackV2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_hit(self):
        response = self.client.post("/v2/blackjack/hit/user1")
        self.assertEqual(response.status_code, 200)
```

### MongoDB Patterns

- Use `ObjectId` for document IDs
- Convert Pydantic models to dicts before database operations

```python
user_dict = dict(user)
del user_dict["id"]  # Remove UUID for insert
id = db_client.users.insert_one(user_dict).inserted_id
```

### API Response Patterns

```python
# Success
return {"user_id": user_id, "mensaje": "Partida creada"}

# Error
raise HTTPException(status_code=404, detail="Partida no encontrada")
```
