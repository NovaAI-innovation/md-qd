```python
import pytest
import yaml
from typing import Dict, Any
from jsonschema import validate, ValidationError

def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    Loads a YAML file and returns its content as a dictionary.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        Dict[str, Any]: The content of the YAML file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the YAML file is invalid.
    """
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML file: {file_path}. Error: {e}")


def validate_openapi(data: Dict[str, Any]) -> None:
    """
    Validates an OpenAPI specification against the OpenAPI schema.

    Args:
        data (Dict[str, Any]): The OpenAPI specification as a dictionary.

    Raises:
        ValidationError: If the OpenAPI specification is invalid.
    """
    # Basic validation - check for required fields
    required_fields = ["openapi", "info", "paths"]
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")

    # More comprehensive validation would require loading the OpenAPI schema
    # and validating against it using jsonschema.validate.
    # This is a placeholder for that functionality.
    # Example:
    # from jsonschema import validate
    # openapi_schema = load_yaml("path/to/openapi_schema.yaml")
    # validate(instance=data, schema=openapi_schema)
    pass


# Fixtures
@pytest.fixture
def valid_openapi_data() -> Dict[str, Any]:
    """
    Fixture that returns a valid OpenAPI specification.
    """
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
def invalid_openapi_data() -> Dict[str, Any]:
    """
    Fixture that returns an invalid OpenAPI specification (missing 'paths').
    """
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Sample API",
            "version": "1.0.0"
        }
    }


@pytest.fixture
def sample_yaml_file(tmp_path):
    """
    Fixture that creates a sample YAML file for testing.
    """
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "sample.yaml"
    p.write_text("openapi: 3.0.0\ninfo:\n  title: Sample API\n  version: 1.0.0\npaths: {}")
    return str(p)


@pytest.fixture
def invalid_yaml_file(tmp_path):
    """
    Fixture that creates an invalid YAML file for testing.
    """
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "invalid.yaml"
    p.write_text("openapi: 3.0.0\ninfo:\n  title: Sample API\n  version: 1.0.0\npaths: \n")  # Invalid YAML
    return str(p)


# Unit tests for load_yaml
def test_load_yaml_valid_file(sample_yaml_file: str, valid_openapi_data: Dict[str, Any]):
    """
    Tests loading a valid YAML file.
    """
    data = load_yaml(sample_yaml_file)
    assert data == valid_openapi_data


def test_load_yaml_file_not_found():
    """
    Tests loading a non-existent YAML file.
    """
    with pytest.raises(FileNotFoundError):
        load_yaml("non_existent_file.yaml")


def test_load_yaml_invalid_file(invalid_yaml_file: str):
    """
    Tests loading an invalid YAML file.
    """
    with pytest.raises(yaml.YAMLError):
        load_yaml(invalid_yaml_file)


# Unit tests for validate_openapi
def test_validate_openapi_valid_data(valid_openapi_data: Dict[str, Any]):
    """
    Tests validating a valid OpenAPI specification.
    """
    validate_openapi(valid_openapi_data)  # Should not raise an exception


def test_validate_openapi_invalid_data(invalid_openapi_data: Dict[str, Any]):
    """
    Tests validating an invalid OpenAPI specification.
    """
    with pytest.raises(ValidationError):
        validate_openapi(invalid_openapi_data)


# Integration tests
def test_load_and_validate_openapi(sample_yaml_file: str):
    """
    Tests loading a YAML file and validating its OpenAPI specification.
    """
    data = load_yaml(sample_yaml_file)
    validate_openapi(data)


def test_load_and_validate_invalid_openapi(invalid_yaml_file: str):
    """
    Tests loading an invalid YAML file and attempting to validate its OpenAPI specification.
    """
    with pytest.raises((yaml.YAMLError, ValidationError)):
        data = load_yaml(invalid_yaml_file)
        validate_openapi(data)
```