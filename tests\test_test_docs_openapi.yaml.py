```python
import pytest
import yaml
from typing import Dict, Any
from pathlib import Path
from jsonschema import validate, ValidationError

# Define the path to the OpenAPI YAML file
OPENAPI_YAML_PATH = Path(__file__).parent.parent / "docs" / "openapi.yaml"


@pytest.fixture(scope="session")
def openapi_spec() -> Dict[str, Any]:
    """
    Fixture to load the OpenAPI specification from the YAML file.

    Returns:
        A dictionary representing the OpenAPI specification.
    """
    try:
        with open(OPENAPI_YAML_PATH, "r") as f:
            spec = yaml.safe_load(f)
        return spec
    except FileNotFoundError:
        pytest.fail(f"OpenAPI specification file not found at: {OPENAPI_YAML_PATH}")
    except yaml.YAMLError as e:
        pytest.fail(f"Error parsing OpenAPI specification: {e}")


def test_openapi_spec_exists():
    """
    Test that the OpenAPI specification file exists.
    """
    assert OPENAPI_YAML_PATH.exists(), f"OpenAPI specification file not found at: {OPENAPI_YAML_PATH}"


def test_openapi_spec_is_valid_yaml(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification is valid YAML.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert isinstance(openapi_spec, dict), "OpenAPI specification is not a valid YAML dictionary."


def test_openapi_spec_has_required_fields(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification has the required fields.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    required_fields = ["openapi", "info", "paths"]
    for field in required_fields:
        assert field in openapi_spec, f"OpenAPI specification is missing required field: {field}"


def test_openapi_spec_openapi_version(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification has a valid OpenAPI version.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert "openapi" in openapi_spec, "OpenAPI specification is missing 'openapi' field."
    assert isinstance(openapi_spec["openapi"], str), "'openapi' field must be a string."
    assert openapi_spec["openapi"].startswith("3."), "OpenAPI version must be 3.x.x"


def test_openapi_spec_info_fields(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification has the required info fields.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert "info" in openapi_spec, "OpenAPI specification is missing 'info' field."
    info = openapi_spec["info"]
    assert isinstance(info, dict), "'info' field must be a dictionary."
    required_info_fields = ["title", "version"]
    for field in required_info_fields:
        assert field in info, f"OpenAPI specification 'info' is missing required field: {field}"


def test_openapi_spec_paths_exist_and_are_dict(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification has paths and that they are a dictionary.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert "paths" in openapi_spec, "OpenAPI specification is missing 'paths' field."
    paths = openapi_spec["paths"]
    assert isinstance(paths, dict), "'paths' field must be a dictionary."


def test_openapi_spec_paths_are_valid(openapi_spec: Dict[str, Any]):
    """
    Test that the paths in the OpenAPI specification are valid.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    paths = openapi_spec["paths"]
    for path, path_item in paths.items():
        assert isinstance(path, str), "Path must be a string."
        assert path.startswith("/"), "Path must start with a '/'"
        assert isinstance(path_item, dict), "Path item must be a dictionary."
        for method, operation in path_item.items():
            assert method in ["get", "post", "put", "patch", "delete", "options", "head", "trace"], f"Invalid HTTP method: {method}"
            assert isinstance(operation, dict), "Operation must be a dictionary."
            assert "responses" in operation, f"Operation for {method} {path} is missing 'responses' field."
            responses = operation["responses"]
            assert isinstance(responses, dict), "'responses' field must be a dictionary."
            for status_code, response in responses.items():
                try:
                    status_code = int(status_code)
                    assert 100 <= status_code <= 599, f"Invalid HTTP status code: {status_code}"
                except ValueError:
                    assert False, f"Invalid HTTP status code: {status_code}"
                assert isinstance(response, dict), "Response must be a dictionary."
                assert "description" in response, f"Response for {status_code} is missing 'description' field."


def test_openapi_spec_components_exist_and_are_dict(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification has components and that they are a dictionary.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    if "components" in openapi_spec:
        components = openapi_spec["components"]
        assert isinstance(components, dict), "'components' field must be a dictionary."


def test_openapi_spec_security_schemes_exist_and_are_dict(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification has security schemes and that they are a dictionary.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    if "components" in openapi_spec and "securitySchemes" in openapi_spec["components"]:
        security_schemes = openapi_spec["components"]["securitySchemes"]
        assert isinstance(security_schemes, dict), "'securitySchemes' field must be a dictionary."
        for scheme_name, scheme_def in security_schemes.items():
            assert isinstance(scheme_name, str), "Security scheme name must be a string."
            assert isinstance(scheme_def, dict), "Security scheme definition must be a dictionary."
            assert "type" in scheme_def, "Security scheme definition is missing 'type' field."


# Example of a more complex validation using jsonschema (requires a schema definition)
# This is just an example, adapt it to your specific needs
@pytest.mark.skip(reason="Requires a JSON schema definition for full validation")
def test_openapi_spec_validates_against_schema(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification validates against a JSON schema.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    # Load the JSON schema (replace with your actual schema path)
    schema_path = Path(__file__).parent / "openapi_schema.json"  # Example path
    try:
        with open(schema_path, "r") as f:
            schema = yaml.safe_load(f)  # or json.load(f) if it's a JSON file
    except FileNotFoundError:
        pytest.fail(f"JSON schema file not found at: {schema_path}")
    except yaml.YAMLError as e:
        pytest.fail(f"Error parsing JSON schema: {e}")

    try:
        validate(openapi_spec, schema)
    except ValidationError as e:
        pytest.fail(f"OpenAPI specification does not validate against the schema: {e}")
```