```markdown
# API Documentation

This document provides comprehensive information about our API, including endpoints, parameters, responses, and authentication requirements.  We use OpenAPI/Swagger to define our API, ensuring clarity and ease of integration.

**Note:**  This documentation is automatically generated and may be subject to change.

## Authentication

This API requires authentication using **API Keys**.  You must include your API key in the `X-API-Key` header of every request.

```
X-API-Key: YOUR_API_KEY
```

If the API Key is missing or invalid, you will receive a `401 Unauthorized` error.

## Endpoints

### 1. Get User Information

*   **Endpoint:** `GET /users/{user_id}`
*   **Description:** Retrieves information about a specific user.
*   **Parameters:**

    *   `user_id` (Path, required):  The ID of the user to retrieve.  (Type: integer)

*   **Request Example:**

    ```
    GET /users/123
    X-API-Key: YOUR_API_KEY
    ```

*   **Responses:**

    *   **200 OK:**  Successful retrieval of user information.

        ```json
        {
          "id": 123,
          "username": "johndoe",
          "email": "john.doe@example.com",
          "firstName": "John",
          "lastName": "Doe"
        }
        ```

    *   **401 Unauthorized:**  Invalid or missing API Key.

        ```json
        {
          "error": "Unauthorized",
          "message": "Invalid or missing API Key"
        }
        ```

    *   **404 Not Found:**  User not found.

        ```json
        {
          "error": "Not Found",
          "message": "User with ID 123 not found"
        }
        ```

*   **Error Codes:**

    *   `401`: Unauthorized - Indicates an invalid or missing API Key.
    *   `404`: Not Found - Indicates that the requested resource was not found.

### 2. Create a New User

*   **Endpoint:** `POST /users`
*   **Description:** Creates a new user.
*   **Parameters:**

    *   **Request Body (application/json):**

        ```json
        {
          "username": "newuser",
          "email": "newuser@example.com",
          "firstName": "New",
          "lastName": "User"
        }
        ```

*   **Request Example:**

    ```
    POST /users
    Content-Type: application/json
    X-API-Key: YOUR_API_KEY

    {
      "username": "newuser",
      "email": "newuser@example.com",
      "firstName": "New",
      "lastName": "User"
    }
    ```

*   **Responses:**

    *   **201 Created:**  User successfully created.  Returns the newly created user object.

        ```json
        {
          "id": 456,
          "username": "newuser",
          "email": "newuser@example.com",
          "firstName": "New",
          "lastName": "User"
        }
        ```

    *   **400 Bad Request:**  Invalid request body.

        ```json
        {
          "error": "Bad Request",
          "message": "Username is required"
        }
        ```

    *   **401 Unauthorized:**  Invalid or missing API Key.

        ```json
        {
          "error": "Unauthorized",
          "message": "Invalid or missing API Key"
        }
        ```

*   **Error Codes:**

    *   `400`: Bad Request - Indicates an invalid request body.  The `message` field will provide details about the error.
    *   `401`: Unauthorized - Indicates an invalid or missing API Key.

### 3. Update an Existing User

*   **Endpoint:** `PUT /users/{user_id}`
*   **Description:** Updates an existing user.
*   **Parameters:**

    *   `user_id` (Path, required): The ID of the user to update. (Type: integer)
    *   **Request Body (application/json):**

        ```json
        {
          "email": "updated.email@example.com",
          "firstName": "UpdatedFirstName"
        }
        ```

*   **Request Example:**

    ```
    PUT /users/123
    Content-Type: application/json
    X-API-Key: YOUR_API_KEY

    {
      "email": "updated.email@example.com",
      "firstName": "UpdatedFirstName"
    }
    ```

*   **Responses:**

    *   **200 OK:** User successfully updated. Returns the updated user object.

        ```json
        {
          "id": 123,
          "username": "johndoe",
          "email": "updated.email@example.com",
          "firstName": "UpdatedFirstName",
          "lastName": "Doe"
        }
        ```

    *   **400 Bad Request:** Invalid request body.

        ```json
        {
          "error": "Bad Request",
          "message": "Invalid email format"
        }
        ```

    *   **401 Unauthorized:** Invalid or missing API Key.

        ```json
        {
          "error": "Unauthorized",
          "message": "Invalid or missing API Key"
        }
        ```

    *   **404 Not Found:** User not found.

        ```json
        {
          "error": "Not Found",
          "message": "User with ID 123 not found"
        }
        ```

*   **Error Codes:**

    *   `400`: Bad Request - Indicates an invalid request body. The `message` field will provide details about the error.
    *   `401`: Unauthorized - Indicates an invalid or missing API Key.
    *   `404`: Not Found - Indicates that the requested resource was not found.

### 4. Delete a User

*   **Endpoint:** `DELETE /users/{user_id}`
*   **Description:** Deletes an existing user.
*   **Parameters:**

    *   `user_id` (Path, required): The ID of the user to delete. (Type: integer)

*   **Request Example:**

    ```
    DELETE /users/123
    X-API-Key: YOUR_API_KEY
    ```

*   **Responses:**

    *   **204 No Content:** User successfully deleted.  No content is returned.

    *   **401 Unauthorized:** Invalid or missing API Key.

        ```json
        {
          "error": "Unauthorized",
          "message": "Invalid or missing API Key"
        }
        ```

    *   **404 Not Found:** User not found.

        ```json
        {
          "error": "Not Found",
          "message": "User with ID 123 not found"
        }
        ```

*   **Error Codes:**

    *   `401`: Unauthorized - Indicates an invalid or missing API Key.
    *   `404`: Not Found - Indicates that the requested resource was not found.

## Rate Limiting

*   Rate limiting is in effect to ensure the stability of the API.  You are limited to **100 requests per minute**.  If you exceed this limit, you will receive a `429 Too Many Requests` error.

    ```json
    {
      "error": "Too Many Requests",
      "message": "Rate limit exceeded. Try again in 60 seconds."
    }
    ```

*   The following headers are returned with each response to indicate your rate limit status:

    *   `X-RateLimit-Limit`: The maximum number of requests allowed per minute.
    *   `X-RateLimit-Remaining`: The number of requests remaining in the current minute.
    *   `X-RateLimit-Reset`: The time at which the rate limit will be reset (in seconds since the epoch).

## Contributing

We welcome contributions to improve this API documentation.  Please submit pull requests with any corrections or additions.

```
```
