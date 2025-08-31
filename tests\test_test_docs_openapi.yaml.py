```python
import pytest
import yaml
from typing import Dict, Any
from jsonschema import validate, ValidationError

# Define fixtures for test data
@pytest.fixture
def valid_openapi_spec() -> Dict[str, Any]:
    """Fixture providing a valid OpenAPI specification."""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Sample API",
            "version": "1.0.0"
        },
        "paths": {
            "/items": {
                "get": {
                    "summary": "List items",
                    "responses": {
                        "200": {
                            "description": "A list of items."
                        }
                    }
                }
            }
        }
    }

@pytest.fixture
def invalid_openapi_spec() -> Dict[str, Any]:
    """Fixture providing an invalid OpenAPI specification (missing version)."""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Sample API"
        },
        "paths": {
            "/items": {
                "get": {
                    "summary": "List items",
                    "responses": {
                        "200": {
                            "description": "A list of items."
                        }
                    }
                }
            }
        }
    }

@pytest.fixture
def openapi_schema() -> Dict[str, Any]:
    """Fixture providing a minimal OpenAPI schema for validation."""
    # In a real application, this would load the full OpenAPI schema.
    # For testing, a simplified schema is sufficient.
    return {
        "type": "object",
        "properties": {
            "openapi": {"type": "string"},
            "info": {"type": "object"},
            "paths": {"type": "object"}
        },
        "required": ["openapi", "info", "paths"]
    }

# Define test functions
def test_valid_openapi_spec_validation(valid_openapi_spec: Dict[str, Any], openapi_schema: Dict[str, Any]) -> None:
    """
    Test that a valid OpenAPI specification passes validation against the schema.
    """
    try:
        validate(instance=valid_openapi_spec, schema=openapi_schema)
    except ValidationError as e:
        pytest.fail(f"Validation failed: {e}")

def test_invalid_openapi_spec_validation(invalid_openapi_spec: Dict[str, Any], openapi_schema: Dict[str, Any]) -> None:
    """
    Test that an invalid OpenAPI specification raises a ValidationError.
    """
    with pytest.raises(ValidationError):
        validate(instance=invalid_openapi_spec, schema=openapi_schema)

def test_empty_openapi_spec_validation(openapi_schema: Dict[str, Any]) -> None:
    """
    Test that an empty OpenAPI specification raises a ValidationError.
    """
    with pytest.raises(ValidationError):
        validate(instance={}, schema=openapi_schema)

def test_openapi_spec_with_additional_properties(valid_openapi_spec: Dict[str, Any], openapi_schema: Dict[str, Any]) -> None:
    """
    Test that an OpenAPI specification with additional properties still validates (if allowed by the schema).
    """
    valid_openapi_spec["x-custom-property"] = "custom value"
    try:
        validate(instance=valid_openapi_spec, schema=openapi_schema)
    except ValidationError as e:
        pytest.fail(f"Validation failed: {e}")

def test_openapi_spec_with_null_values(openapi_schema: Dict[str, Any]) -> None:
    """
    Test that an OpenAPI specification with null values raises a ValidationError if not allowed by the schema.
    """
    spec = {
        "openapi": "3.0.0",
        "info": None,
        "paths": {}
    }
    with pytest.raises(ValidationError):
        validate(instance=spec, schema=openapi_schema)

def test_openapi_spec_versions(openapi_schema: Dict[str, Any]) -> None:
    """
    Test different OpenAPI versions.
    """
    spec_3_1 = {
        "openapi": "3.1.0",
        "info": {"title": "Test API", "version": "1.0"},
        "paths": {}
    }
    try:
        validate(instance=spec_3_1, schema=openapi_schema)
    except ValidationError as e:
        pytest.fail(f"Validation failed: {e}")

    spec_2_0 = {
        "swagger": "2.0",
        "info": {"title": "Test API", "version": "1.0"},
        "paths": {}
    }
    with pytest.raises(ValidationError):
        validate(instance=spec_2_0, schema=openapi_schema)

def test_openapi_spec_empty_paths(valid_openapi_spec: Dict[str, Any], openapi_schema: Dict[str, Any]) -> None:
    """
    Test OpenAPI spec with empty paths.
    """
    valid_openapi_spec["paths"] = {}
    try:
        validate(instance=valid_openapi_spec, schema=openapi_schema)
    except ValidationError as e:
        pytest.fail(f"Validation failed: {e}")

def test_openapi_spec_invalid_path_structure(valid_openapi_spec: Dict[str, Any], openapi_schema: Dict[str, Any]) -> None:
    """
    Test OpenAPI spec with invalid path structure.
    """
    valid_openapi_spec["paths"] = {"/items": "invalid"}
    with pytest.raises(ValidationError):
        validate(instance=valid_openapi_spec, schema=openapi_schema)
```