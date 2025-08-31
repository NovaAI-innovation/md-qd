```markdown
## Automated Implementation Plan for User Update Operation

This feature automates the creation of an implementation plan for adding the `UPDATE` operation to the user management system. It analyzes existing code, identifies necessary modifications, and generates a detailed, step-by-step plan to guide developers through the implementation process. This helps reduce development time, minimize errors, and ensures consistency across the codebase.

**Usage Examples:**

To generate an implementation plan for the user update operation, use the following command:

```bash
./generate_implementation_plan.sh --operation update --entity user
```

This command will analyze the existing user management system and output a detailed plan to the console.  You can also save the plan to a file:

```bash
./generate_implementation_plan.sh --operation update --entity user --output update_user_plan.txt
```

To view available options and configurations, run the script with the `--help` flag:

```bash
./generate_implementation_plan.sh --help
```

The generated implementation plan typically includes sections such as:

*   **Prerequisites:**  Lists necessary dependencies and environment setup.
*   **Code Modifications:**  Specifies files to be modified and the exact code changes required.
*   **Testing:**  Outlines the testing strategy and test cases to ensure the `UPDATE` operation functions correctly.
*   **Deployment:**  Provides instructions for deploying the updated code.
*   **Rollback Plan:** Details the steps to revert to the previous state in case of issues.

**Configuration Options:**

The `generate_implementation_plan.sh` script accepts the following configuration options:

*   `--operation <operation>`:  Specifies the operation to be implemented (e.g., `update`, `delete`).  Required.
*   `--entity <entity>`: Specifies the entity to which the operation applies (e.g., `user`, `role`). Required.
*   `--output <filename>`:  Specifies the file to which the implementation plan should be written.  Optional; if not provided, the plan will be printed to the console.
*   `--template-dir <directory>`: Specifies the directory containing custom plan templates. Optional; defaults to `./templates`.
*   `--dry-run`:  Performs a dry run, displaying the plan without making any changes to the system. Optional.
*   `--help`: Displays help information and available options.

**Installation/Setup:**

1.  **Clone the repository:**  Ensure you have the latest version of the user management system code.
2.  **Install dependencies:**  The `generate_implementation_plan.sh` script requires Python 3 and the `jinja2` templating library.  Install these dependencies using `pip`:

    ```bash
    pip install jinja2
    ```

3.  **Make the script executable:**

    ```bash
    chmod +x generate_implementation_plan.sh
    ```

4.  **Configure Access (Optional):** If the script needs to access databases or other services, ensure it has the necessary credentials configured in the environment or through configuration files.  Refer to the existing documentation for connecting to your specific database and services.

**Example Implementation Plan Snippet:**

```
## Implementation Plan: Update User

**1. Prerequisites:**

*   Ensure the database is running and accessible.
*   Verify that you have the necessary permissions to modify the user database.

**2. Code Modifications:**

*   **File:** `src/user_service.py`
    *   **Action:** Add the `update_user` method:

        ```python
        def update_user(self, user_id, user_data):
            # Implementation details here
            pass
        ```

*   **File:** `src/user_api.py`
    *   **Action:** Add a route for handling the `UPDATE` request:

        ```python
        @app.route('/users/<user_id>', methods=['PUT'])
        def update_user_route(user_id):
            # Implementation details here
            pass
        ```

**3. Testing:**

*   **Unit Test:**  `tests/test_user_service.py`
    *   Create a test case to verify that `update_user` correctly updates user data in the database.
    *   Create a test case to handle invalid user IDs.
*   **API Test:**  Use a tool like `curl` or Postman to send a `PUT` request to the `/users/<user_id>` endpoint and verify the response.

... (rest of the implementation plan)
```
```