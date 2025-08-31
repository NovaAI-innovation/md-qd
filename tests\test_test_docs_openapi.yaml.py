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
        pytest.fail(f"OpenAPI specification file not found: {OPENAPI_YAML_PATH}")
    except yaml.YAMLError as e:
        pytest.fail(f"Error parsing OpenAPI specification: {e}")


def test_openapi_spec_exists():
    """
    Test that the OpenAPI specification file exists.
    """
    assert OPENAPI_YAML_PATH.exists(), f"OpenAPI specification file not found: {OPENAPI_YAML_PATH}"


def test_openapi_spec_is_valid_yaml(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification is valid YAML.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert isinstance(openapi_spec, dict), "OpenAPI specification is not a valid YAML dictionary."


def test_openapi_spec_has_openapi_version(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification contains the 'openapi' key.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert "openapi" in openapi_spec, "OpenAPI specification does not contain 'openapi' key."


def test_openapi_spec_openapi_version_is_valid(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'openapi' version is a string.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert isinstance(openapi_spec["openapi"], str), "OpenAPI version is not a string."
    assert openapi_spec["openapi"].startswith("3.0"), "OpenAPI version is not 3.0.x"


def test_openapi_spec_has_info(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification contains the 'info' key.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert "info" in openapi_spec, "OpenAPI specification does not contain 'info' key."


def test_openapi_spec_info_is_dict(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'info' value is a dictionary.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert isinstance(openapi_spec["info"], dict), "OpenAPI 'info' is not a dictionary."


def test_openapi_spec_info_has_title(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'info' dictionary contains the 'title' key.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert "title" in openapi_spec["info"], "OpenAPI 'info' does not contain 'title' key."


def test_openapi_spec_info_title_is_string(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'info' title is a string.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert isinstance(openapi_spec["info"]["title"], str), "OpenAPI 'info' title is not a string."


def test_openapi_spec_info_has_version(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'info' dictionary contains the 'version' key.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert "version" in openapi_spec["info"], "OpenAPI 'info' does not contain 'version' key."


def test_openapi_spec_info_version_is_string(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'info' version is a string.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert isinstance(openapi_spec["info"]["version"], str), "OpenAPI 'info' version is not a string."


def test_openapi_spec_has_paths(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification contains the 'paths' key.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert "paths" in openapi_spec, "OpenAPI specification does not contain 'paths' key."


def test_openapi_spec_paths_is_dict(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'paths' value is a dictionary.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert isinstance(openapi_spec["paths"], dict), "OpenAPI 'paths' is not a dictionary."


def test_openapi_spec_paths_are_valid(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'paths' are valid.  This is a basic check
    to ensure that each path definition is a dictionary.  More detailed validation
    would require a schema.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    for path, definition in openapi_spec["paths"].items():
        assert isinstance(definition, dict), f"Path '{path}' definition is not a dictionary."


def test_openapi_spec_has_components(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification contains the 'components' key.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert "components" in openapi_spec, "OpenAPI specification does not contain 'components' key."


def test_openapi_spec_components_is_dict(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'components' value is a dictionary.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert isinstance(openapi_spec["components"], dict), "OpenAPI 'components' is not a dictionary."


def test_openapi_spec_components_has_schemas(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'components' contains the 'schemas' key.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert "schemas" in openapi_spec["components"], "OpenAPI 'components' does not contain 'schemas' key."


def test_openapi_spec_components_schemas_is_dict(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'components' schemas value is a dictionary.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    assert isinstance(openapi_spec["components"]["schemas"], dict), "OpenAPI 'components' schemas is not a dictionary."


def test_openapi_spec_components_schemas_are_valid(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification's 'components' schemas are valid. This is a basic check
    to ensure that each schema definition is a dictionary. More detailed validation
    would require a schema.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML file.
    """
    for schema_name, definition in openapi_spec["components"]["schemas"].items():
        assert isinstance(definition, dict), f"Schema '{schema_name}' definition is not a dictionary."


def test_openapi_spec_is_valid_against_schema(openapi_spec: Dict[str, Any]):
    """
    Test that the OpenAPI specification is valid against a basic OpenAPI schema.
    This test provides a more comprehensive validation of the OpenAPI specification.

    Args:
        openapi_spec: The OpenAPI specification loaded from the YAML