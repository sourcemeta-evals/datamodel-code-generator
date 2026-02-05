# Requirements for --use-type-alias flag

## Feature Overview
Add a `--use-type-alias` CLI flag that generates Python type aliases instead of RootModel classes.

## Implementation Requirements

### 1. CLI Flag
- Add `--use-type-alias` flag to `arguments.py`
- Add corresponding config field to `__main__.py` Config class
- Pass through to `generate()` function

### 2. Type Alias Generation Logic
Handle the matrix of Python versions and Pydantic versions:
- **Pydantic v2 + Python 3.12+**: Use native `type` statement
- **Pydantic v2 + Python 3.9-3.11**: Use `TypeAliasType` from `typing_extensions`
- **Pydantic v1 (all Python versions)**: Use `TypeAlias` annotation
- **Non-Pydantic output types** (msgspec, TypedDict, dataclass): Use `TypeAlias` annotation for 3.9-3.11 and `type` statement for 3.12+

### 3. Import Handling
- For Python 3.9, `TypeAlias` must be imported from `typing_extensions`
- For Python 3.10-3.11, `TypeAlias` can be imported from `typing`
- For Python 3.12+, no import needed for `type` statement
- `TypeAliasType` must be imported from `typing_extensions`

### 4. Template Files
Create new template files for type alias generation:
- `type_alias.jinja2` - For native `type` statement (Python 3.12+)
- `type_alias_type.jinja2` - For `TypeAliasType` (Pydantic v2, Python 3.9-3.11)
- `type_alias_annotation.jinja2` - For `TypeAlias` annotation (Pydantic v1, non-Pydantic)

### 5. Model Classes
Create TypeAlias model classes that:
- Extend from appropriate base classes
- Use correct templates based on Python/Pydantic version
- Handle imports correctly

### 6. Limitations to Document
- Type aliases don't fully support field-specific metadata (default, alias, etc.)
- Type aliases don't support RootModel features like `model_config`
- Pydantic v1 TypeAlias cannot be combined with `Annotated`

## Expected Output Examples

**Current output (Pydantic v2):**
```python
class Total(RootModel[int]):
    root: Annotated[int, Field(ge=0, title="Total")]

class UserId(RootModel[str]):
    root: str
```

**Desired output with `--use-type-alias` (Pydantic v2, Python 3.12+):**
```python
type Total = Annotated[int, Field(ge=0, title="Total")]
type UserId = str
```

**Desired output with `--use-type-alias` (Pydantic v2, Python 3.9-3.11):**
```python
from typing_extensions import TypeAliasType
Total = TypeAliasType("Total", Annotated[int, Field(ge=0, title="Total")])
UserId = TypeAliasType("UserId", str)
```

**Desired output with `--use-type-alias` (Pydantic v1):**
```python
from typing import TypeAlias  # or typing_extensions for 3.9
Total: TypeAlias = int  # Note: Pydantic v1 can't handle Annotated with TypeAlias
UserId: TypeAlias = str
```
