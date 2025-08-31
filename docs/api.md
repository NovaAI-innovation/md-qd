```markdown
# API Documentation

This document provides comprehensive information about the API, including endpoints, parameters, responses, error codes, and authentication requirements.  This documentation is generated from OpenAPI/Swagger specifications.

## Authentication

This API uses **API Key** authentication. You must include a valid API key in the `X-API-Key` header for all requests.

*   **Header:** `X-API-Key: YOUR_API_KEY`

If the API key is missing or invalid, you will receive a `401 Unauthorized` error.

## Endpoints

### 1.  `/users`

*   **Description:** Retrieves a list of all users.
*   **Method:** `GET`
*   **Authentication:** Required (API Key)

    **Parameters:**

    *   `limit` (query parameter, optional):  The maximum number of users to return.  Defaults to 10.  Type: `integer`.
    *   `offset` (query parameter, optional):  The offset to start the list from.  Used for pagination.  Defaults to 0.  Type: `integer`.

    **Example Request:**

    ```
    GET /users?limit=20&offset=0
    X-API-Key: YOUR_API_KEY
    ```

    **Responses:**

    *   **200 OK:** Successful retrieval of users.

        ```json
        [
          {
            "id": 1,
            "username": "john.doe",
            "email": "john.doe@example.com"
          },
          {
            "id": 2,
            "username": "jane.smith",
            "email": "jane.smith@example.com"
          }
        ]
        ```

    *   **401 Unauthorized:** Invalid or missing API key.

        ```json
        {
          "error": "Unauthorized",
          "message": "Invalid API key"
        }
        ```

    *   **500 Internal Server Error:** An unexpected error occurred on the server.

        ```json
        {
          "error": "Internal Server Error",
          "message": "An unexpected error occurred."
        }
        ```

### 2.  `/users/{id}`

*   **Description:** Retrieves a specific user by ID.
*   **Method:** `GET`
*   **Authentication:** Required (API Key)

    **Parameters:**

    *   `id` (path parameter, required): The ID of the user to retrieve. Type: `integer`.

    **Example Request:**

    ```
    GET /users/123
    X-API-Key: YOUR_API_KEY
    ```

    **Responses:**

    *   **200 OK:** Successful retrieval of the user.

        ```json
        {
          "id": 123,
          "username": "example.user",
          "email": "example.user@example.com"
        }
        ```

    *   **401 Unauthorized:** Invalid or missing API key.

        ```json
        {
          "error": "Unauthorized",
          "message": "Invalid API key"
        }
        ```

    *   **404 Not Found:**  User with the specified ID not found.

        ```json
        {
          "error": "Not Found",
          "message": "User with ID 123 not found"
        }
        ```

    *   **500 Internal Server Error:** An unexpected error occurred on the server.

        ```json
        {
          "error": "Internal Server Error",
          "message": "An unexpected error occurred."
        }
        ```

### 3.  `/users`

*   **Description:** Creates a new user.
*   **Method:** `POST`
*   **Authentication:** Required (API Key)

    **Request Body:**

    ```json
    {
      "username": "newuser",
      "email": "newuser@example.com"
    }
    ```

    **Parameters:**

    *   `username` (body parameter, required): The username for the new user. Type: `string`.
    *   `email` (body parameter, required): The email address for the new user. Type: `string`.

    **Example Request:**

    ```
    POST /users
    Content-Type: application/json
    X-API-Key: YOUR_API_KEY

    {
      "username": "newuser",
      "email": "newuser@example.com"
    }
    ```

    **Responses:**

    *   **201 Created:** Successfully created the user.  Returns the newly created user object.

        ```json
        {
          "id": 456,
          "username": "newuser",
          "email": "newuser@example.com"
        }
        ```

    *   **400 Bad Request:** Invalid request body or missing parameters.

        ```json
        {
          "error": "Bad Request",
          "message": "Missing required parameter: username"
        }
        ```

    *   **401 Unauthorized:** Invalid or missing API key.

        ```json
        {
          "error": "Unauthorized",
          "message": "Invalid API key"
        }
        ```

    *   **500 Internal Server Error:** An unexpected error occurred on the server.

        ```json
        {
          "error": "Internal Server Error",
          "message": "An unexpected error occurred."
        }
        ```

### 4. `/users/{id}`

*   **Description:** Updates an existing user.
*   **Method:** `PUT`
*   **Authentication:** Required (API Key)

    **Parameters:**

    *   `id` (path parameter, required): The ID of the user to update. Type: `integer`.

    **Request Body:**

    ```json
    {
      "username": "updateduser",
      "email": "updateduser@example.com"
    }
    ```

    **Example Request:**

    ```
    PUT /users/123
    Content-Type: application/json
    X-API-Key: YOUR_API_KEY

    {
      "username": "updateduser",
      "email": "updateduser@example.com"
    }
    ```

    **Responses:**

    *   **200 OK:** Successfully updated the user.

        ```json
        {
          "id": 123,
          "username": "updateduser",
          "email": "updateduser@example.com"
        }
        ```

    *   **400 Bad Request:** Invalid request body.

        ```json
        {
          "error": "Bad Request",
          "message": "Invalid email format."
        }
        ```

    *   **401 Unauthorized:** Invalid or missing API key.

        ```json
        {
          "error": "Unauthorized",
          "message": "Invalid API key"
        }
        ```

    *   **404 Not Found:** User with the specified ID not found.

        ```json
        {
          "error": "Not Found",
          "message": "User with ID 123 not found"
        }
        ```

    *   **500 Internal Server Error:** An unexpected error occurred on the server.

        ```json
        {
          "error": "Internal Server Error",
          "message": "An unexpected error occurred."
        }
        ```

### 5. `/users/{id}`

*   **Description:** Deletes a user.
*   **Method:** `DELETE`
*   **Authentication:** Required (API Key)

    **Parameters:**

    *   `id` (path parameter, required): The ID of the user to delete. Type: `integer`.

    **Example Request:**

    ```
    DELETE /users/123
    X-API-Key: YOUR_API_KEY
    ```

    **Responses:**

    *   **204 No Content:** Successfully deleted the user. (No response body)

    *   **401 Unauthorized:** Invalid or missing API key.

        ```json
        {
          "error": "Unauthorized",
          "message": "Invalid API key"
        }
        ```

    *   **404 Not Found:** User with the specified ID not found.

        ```json
        {
          "error": "Not Found",
          "message": "User with ID 123 not found"
        }
        ```

    *   **500 Internal Server Error:** An unexpected error occurred on the server.

        ```json
        {
          "error": "Internal Server Error",
          "message": "An unexpected error occurred."
        }
        ```

## Error Codes and Messages

The API uses standard HTTP status codes to indicate the success or failure of a request.  Here's a summary of common error codes:

*   **400 Bad Request:** The request was malformed or invalid.  See the response body for details.
*   **401 Unauthorized:** Authentication failed due to a missing or invalid API key.
*   **403 Forbidden:** The client does not have permission to access the resource. (Not used in this example, but included for completeness)
*   **404 Not Found:** The requested resource was not found.
*   **500 Internal Server Error:** An unexpected error occurred on the server.

**Note:**  This documentation is a sample.  A full OpenAPI/Swagger specification would be in JSON or YAML format and used with tools like Swagger UI or Redoc to generate interactive documentation.  This markdown is designed to be a human-readable representation of that specification.  This document assumes that the actual OpenAPI/Swagger file is being generated separately.
```
