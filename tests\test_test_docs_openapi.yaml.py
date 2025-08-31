```python
import pytest
import yaml
from typing import Any, Dict
from jsonschema import validate, ValidationError

# Define the schema for the OpenAPI/Swagger documentation YAML file
OPENAPI_SCHEMA = {
    "type": "object",
    "properties": {
        "openapi": {"type": "string"},
        "info": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "version": {"type": "string"},
            },
            "required": ["title", "version"],
        },
        "paths": {"type": "object"},
        "components": {"type": "object"},
    },
    "required": ["openapi", "info", "paths", "components"],
}


@pytest.fixture
def valid_openapi_yaml() -> str:
    """
    Fixture that returns a valid OpenAPI YAML string.
    """
    return """
    openapi: 3.0.0
    info:
      title: Sample API
      version: 1.0.0
    paths:
      /items:
        get:
          summary: List items
          responses:
            '200':
              description: Successful operation
    components:
      schemas:
        Item:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
    """


@pytest.fixture
def invalid_openapi_yaml() -> str:
    """
    Fixture that returns an invalid OpenAPI YAML string (missing 'openapi' field).
    """
    return """
    info:
      title: Sample API
      version: 1.0.0
    paths:
      /items:
        get:
          summary: List items
          responses:
            '200':
              description: Successful operation
    components:
      schemas:
        Item:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
    """


def validate_openapi_yaml(yaml_data: Dict[str, Any]) -> None:
    """
    Validates the given OpenAPI YAML data against the OpenAPI schema.

    Args:
        yaml_data: A dictionary representing the OpenAPI YAML data.

    Raises:
        ValidationError: If the YAML data does not conform to the schema.
    """
    try:
        validate(instance=yaml_data, schema=OPENAPI_SCHEMA)
    except ValidationError as e:
        raise e


def load_yaml(yaml_string: str) -> Dict[str, Any]:
    """
    Loads a YAML string into a Python dictionary.

    Args:
        yaml_string: The YAML string to load.

    Returns:
        A dictionary representing the YAML data.

    Raises:
        yaml.YAMLError: If the YAML string is invalid.
    """
    try:
        return yaml.safe_load(yaml_string)
    except yaml.YAMLError as e:
        raise e


def test_validate_openapi_yaml_valid(valid_openapi_yaml: str) -> None:
    """
    Tests that validate_openapi_yaml() does not raise an exception when given valid YAML data.
    """
    yaml_data = load_yaml(valid_openapi_yaml)
    validate_openapi_yaml(yaml_data)  # Should not raise an exception


def test_validate_openapi_yaml_invalid(invalid_openapi_yaml: str) -> None:
    """
    Tests that validate_openapi_yaml() raises a ValidationError when given invalid YAML data.
    """
    yaml_data = load_yaml(invalid_openapi_yaml)
    with pytest.raises(ValidationError):
        validate_openapi_yaml(yaml_data)


def test_load_yaml_valid(valid_openapi_yaml: str) -> None:
    """
    Tests that load_yaml() correctly loads a valid YAML string into a dictionary.
    """
    yaml_data = load_yaml(valid_openapi_yaml)
    assert isinstance(yaml_data, dict)
    assert yaml_data["info"]["title"] == "Sample API"


def test_load_yaml_invalid() -> None:
    """
    Tests that load_yaml() raises a yaml.YAMLError when given an invalid YAML string.
    """
    invalid_yaml_string = "this is not valid yaml"
    with pytest.raises(yaml.YAMLError):
        load_yaml(invalid_yaml_string)


def test_validate_openapi_yaml_empty_paths(valid_openapi_yaml: str) -> None:
    """
    Tests that validate_openapi_yaml() accepts an empty 'paths' object.
    """
    yaml_data = load_yaml(valid_openapi_yaml)
    yaml_data["paths"] = {}
    validate_openapi_yaml(yaml_data)


def test_validate_openapi_yaml_empty_components(valid_openapi_yaml: str) -> None:
    """
    Tests that validate_openapi_yaml() accepts an empty 'components' object.
    """
    yaml_data = load_yaml(valid_openapi_yaml)
    yaml_data["components"] = {}
    validate_openapi_yaml(yaml_data)


def test_validate_openapi_yaml_missing_info_field(valid_openapi_yaml: str) -> None:
    """
    Tests that validate_openapi_yaml() raises an error when a required field in 'info' is missing.
    """
    yaml_data = load_yaml(valid_openapi_yaml)
    del yaml_data["info"]["title"]
    with pytest.raises(ValidationError):
        validate_openapi_yaml(yaml_data)


def test_validate_openapi_yaml_invalid_openapi_version(valid_openapi_yaml: str) -> None:
    """
    Tests that validate_openapi_yaml() accepts a valid OpenAPI version.
    """
    yaml_data = load_yaml(valid_openapi_yaml)
    yaml_data["openapi"] = "3.1.0"
    validate_openapi_yaml(yaml_data)

    yaml_data["openapi"] = "2.0"
    with pytest.raises(ValidationError):
        validate_openapi_yaml(yaml_data)


def test_load_yaml_empty_string() -> None:
    """
    Tests that load_yaml() handles an empty string gracefully.
    """
    with pytest.raises(yaml.YAMLError):
        load_yaml("")


def test_load_yaml_none() -> None:
    """
    Tests that load_yaml() handles None input gracefully.
    """
    with pytest.raises(AttributeError):
        load_yaml(None)  # type: ignore
```