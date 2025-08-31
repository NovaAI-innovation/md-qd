```markdown
## Automated Implementation Plan for Add LIST Operation for Orders

This feature automates the implementation plan for adding a `LIST` operation to your Orders service. It significantly reduces the manual effort required to expose a paginated list of orders through your API.  Instead of manually creating database queries, DTOs, and API endpoints, this feature generates a suggested implementation plan based on your existing order data model and configuration.  You can then review, customize, and apply this plan to quickly implement the `LIST` operation.

**Key Benefits:**

*   **Reduced Development Time:** Automatically generate a starting point for your `LIST` operation, saving you hours of manual coding.
*   **Improved Consistency:** Ensures a consistent approach to implementing `LIST` operations across different services.
*   **Simplified Development Process:** Streamlines the process of adding a fundamental API operation.

**Usage Examples:**

1.  **Initiate the Implementation Plan Generation:**

    From your project's root directory, run the following command:

    ```bash
    ./your-tool generate-list-plan --entity Order --output-dir src/orders
    ```

    This command will analyze your `Order` entity and generate a suggested implementation plan in the `src/orders` directory.

2.  **Review and Customize the Generated Plan:**

    The generated plan will include:

    *   **Data Access Layer (DAO) code:**  Example database queries for fetching paginated results and total counts.
    *   **Data Transfer Objects (DTOs):**  `OrderListRequest` and `OrderListResponse` DTOs defining the request and response structures.
    *   **Service Layer code:** Logic for orchestrating data retrieval and transformation.
    *   **API Endpoint definition:**  A suggested API endpoint definition (e.g., using OpenAPI/Swagger) for exposing the `LIST` operation.

    Carefully review each generated file and customize it to match your specific requirements. Pay particular attention to:

    *   **Database query optimization:**  Ensure the generated queries are efficient for your database schema.
    *   **Data transformation logic:**  Adjust the transformation logic to match your desired output format.
    *   **API endpoint security:**  Implement appropriate authentication and authorization mechanisms.

3.  **Apply the Implementation Plan:**

    After reviewing and customizing the generated plan, integrate the code into your project.  This typically involves:

    *   Copying the generated files into your project's source code directory.
    *   Updating your API routing configuration to include the new endpoint.
    *   Testing the new `LIST` operation thoroughly.

    Example of accessing the new endpoint:

    ```bash
    curl -X GET "http://localhost:8080/orders?page=1&pageSize=20"
    ```

**Configuration Options:**

The `generate-list-plan` command supports the following configuration options:

*   `--entity <entity_name>`: (Required) The name of the entity for which to generate the `LIST` operation.  For example, `Order`, `Product`, or `Customer`.
*   `--output-dir <directory>`: (Optional, defaults to the current directory) The directory where the generated files will be placed.
*   `--page-size <integer>`: (Optional, defaults to `25`) The default page size to use for the `LIST` operation.
*   `--sort-field <field_name>`: (Optional) The default field to sort the results by.
*   `--sort-direction <asc|desc>`: (Optional, defaults to `asc`) The default sort direction (ascending or descending).
*   `--database-type <type>`: (Optional, defaults to `auto-detect`) The type of the database that will be used. Possible values: `mysql`, `postgresql`, `mssql`, `sqlite`, `auto-detect`. Auto-detect will attempt to determine the database type from the environment variables.

    Example using optional parameters:

    ```bash
    ./your-tool generate-list-plan --entity Order --output-dir src/orders --page-size 50 --sort-field orderDate --sort-direction desc
    ```

**Installation/Setup:**

This feature is included as part of the core tooling. Ensure you have the latest version of the tooling installed.  No additional setup is required.
```
