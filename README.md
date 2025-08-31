```markdown
## Automated Implementation Plan for Add LIST Operation for Orders

This feature automates the implementation plan generation for adding the `LIST` operation to the Orders service. It analyzes your existing codebase, identifies necessary changes, and generates a detailed, step-by-step implementation plan to streamline the development process. This feature significantly reduces the manual effort required to plan and execute the addition of a `LIST` operation, saving time and minimizing potential errors.

**Description**

The Automated Implementation Plan for `LIST` operation provides a structured approach to adding the functionality to retrieve a list of orders.  It analyzes existing order-related code, including data models, database interactions, and API endpoints, and then generates a comprehensive plan encompassing tasks such as:

*   Defining the API endpoint for retrieving orders.
*   Implementing pagination and filtering options.
*   Creating database queries to efficiently retrieve order data.
*   Handling potential errors and edge cases.
*   Updating documentation with the new `LIST` operation.
*   Adding necessary unit and integration tests.

**Usage Examples**

To generate the implementation plan, use the following command:

```bash
./your_script.sh generate_list_plan --service orders --output-dir ./implementation_plans
```

This command will generate a detailed implementation plan in the `./implementation_plans` directory.  The plan will be presented in a human-readable format (e.g., Markdown or YAML) and include specific instructions for each step.

Example of a generated plan snippet:

```markdown
### Task 1: Define API Endpoint

*   **Description:** Create a new API endpoint `/orders` that accepts GET requests.
*   **Implementation Details:**
    *   Add a new route in your API routing configuration.
    *   Ensure the endpoint supports pagination parameters (e.g., `page`, `page_size`).
    *   Consider adding filtering parameters (e.g., `status`, `customer_id`).
*   **Code Example (Conceptual):**

    ```python
    # Example using a hypothetical framework
    @app.route('/orders', methods=['GET'])
    def list_orders():
        # ... implementation details ...
        return jsonify(orders)
    ```

### Task 2: Implement Database Query

*   **Description:** Create a database query to retrieve orders based on the provided filters and pagination parameters.
*   **Implementation Details:**
    *   Use your preferred database query language (e.g., SQL, MongoDB query language).
    *   Optimize the query for performance, especially when dealing with large datasets.
    *   Handle potential database errors.
*   **Code Example (Conceptual - SQL):**

    ```sql
    SELECT * FROM orders
    WHERE status = :status AND customer_id = :customer_id
    LIMIT :page_size OFFSET :offset;
    ```
```

**New Configuration Options**

The following new configuration options are available:

*   `--service`: Specifies the name of the service to generate the implementation plan for. (Required)  Defaults to `orders` if not specified, but it's best practice to explicitly define it.
    *   **Example:** `--service payments`
*   `--output-dir`:  Specifies the directory where the generated implementation plan should be saved. (Optional)
    *   **Default:**  `./implementation_plans`
    *   **Example:** `--output-dir ./my_plans`
*   `--template`: Specifies the template to use for generating the implementation plan. (Optional).  Different templates may provide varying levels of detail or focus on different aspects of the implementation.
    *   **Default:** `default` (a general-purpose template)
    *   **Example:** `--template detailed` (for a more in-depth plan)
*   `--database-type`: Specifies the database type being used. (Optional). This helps the generator provide more accurate database-specific code examples in the generated plan.
    *   **Default:** `generic`
    *   **Example:** `--database-type postgresql`

You can configure these options via command-line arguments, environment variables, or a configuration file.  Refer to the complete configuration documentation for more details.

**Installation/Setup Instructions**

This feature is included as part of the core toolset. No separate installation is required. Ensure you have the latest version of the tool to access this functionality.  You can check your current version and update if necessary using the following command:

```bash
./your_script.sh --version
./your_script.sh --update
```

Ensure that your environment is properly configured and has access to the necessary dependencies, such as database connection details and API configuration files. The feature will attempt to automatically detect these settings, but you may need to configure them manually if they are not in the standard locations.
```