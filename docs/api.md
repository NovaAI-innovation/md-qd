Okay, here's the Markdown-formatted API documentation for the "Add UPDATE operation for users" API, covering the requirements you've specified. This documentation is designed to be compatible with OpenAPI/Swagger.

```markdown
# User API - UPDATE Operation

## Overview

This document describes the API endpoint for updating existing user information. This endpoint allows authorized clients to modify various attributes of a user, such as their email, first name, last name, and role.

**Phase:** Documentation

**API Version:** v1

## Authentication

This API endpoint requires authentication using API keys.  Include the `X-API-Key` header in your request with a valid API key.

## Endpoint

**Method:** `PUT`

**Path:** `/users/{user_id}`

**Description:** Updates an existing user with the provided information.

## Parameters

### Path Parameters

| Name      | Type   | Required | Description                               | Example      |
|-----------|--------|----------|-------------------------------------------|--------------|
| `user_id` | `integer` | Yes      | The unique identifier of the user to update. | `123`        |

### Request Body

The request body should be a JSON object containing the fields to be updated.  All fields are optional; only include the fields you wish to modify.

**Schema:**

```json
{
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "string"
}
```

**Fields:**

| Name         | Type     | Required | Description                                                                                                | Example                |
|--------------|----------|----------|------------------------------------------------------------------------------------------------------------|------------------------|
| `email`      | `string` | No       | The user's email address. Must be a valid email format.                                                   | `john.doe@example.com` |
| `first_name` | `string` | No       | The user's first name.                                                                                    | `John`                 |
| `last_name`  | `string` | No       | The user's last name.                                                                                     | `Doe`                  |
| `role`       | `string` | No       | The user's role.  Allowed values are: `admin`, `editor`, `viewer`.                                       | `editor`               |

**Example Request Body:**

```json
{
  "email": "updated.email@example.com",
  "last_name": "Smith"
}
```

## Responses

### 200 OK

**Description:** The user was successfully updated.

**Schema:**

```json
{
  "id": "integer",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "string",
  "created_at": "string",
  "updated_at": "string"
}
```

**Example Response:**

```json
{
  "id": 123,
  "email": "updated.email@example.com",
  "first_name": "John",
  "last_name": "Smith",
  "role": "editor",
  "created_at": "2023-10-26T10:00:00Z",
  "updated_at": "2023-10-27T11:00:00Z"
}
```

### 400 Bad Request

**Description:** The request was malformed or contained invalid data.

**Schema:**

```json
{
  "error": "string",
  "message": "string"
}
```

**Example Response:**

```json
{
  "error": "InvalidRequest",
  "message": "Invalid email format."
}
```

### 401 Unauthorized

**Description:** The API key is missing or invalid.

**Schema:**

```json
{
  "error": "string",
  "message": "string"
}
```

**Example Response:**

```json
{
  "error": "Unauthorized",
  "message": "Invalid API key."
}
```

### 404 Not Found

**Description:** The user with the specified ID was not found.

**Schema:**

```json
{
  "error": "string",
  "message": "string"
}
```

**Example Response:**

```json
{
  "error": "NotFound",
  "message": "User with ID 123 not found."
}
```

### 500 Internal Server Error

**Description:** An unexpected error occurred on the server.

**Schema:**

```json
{
  "error": "string",
  "message": "string"
}
```

**Example Response:**

```json
{
  "error": "InternalServerError",
  "message": "An unexpected error occurred. Please try again later."
}
```

## Error Codes and Messages

| Error Code          | HTTP Status | Description                                          |
|---------------------|-------------|------------------------------------------------------|
| `InvalidRequest`    | 400         | The request body is invalid or contains errors.      |
| `Unauthorized`      | 401         | The API key is missing or invalid.                  |
| `NotFound`          | 404         | The requested resource was not found.                |
| `InternalServerError`| 500         | An unexpected server error occurred.                 |

## Example Request (cURL)

```bash
curl -X PUT \
  'https://api.example.com/users/123' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: YOUR_API_KEY' \
  -d '{
    "email": "updated.email@example.com",
    "last_name": "Smith"
  }'
```

## OpenAPI (Swagger) Specification Snippet

```yaml
paths:
  /users/{user_id}:
    put:
      summary: Update an existing user
      description: Updates an existing user with the provided information.
      tags:
        - Users
      security:
        - APIKeyAuth: []
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
          required: true
          description: The unique identifier of the user to update.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  format: email
                  description: The user's email address.
                first_name:
                  type: string
                  description: The user's first name.
                last_name:
                  type: string
                  description: The user's last name.
                role:
                  type: string
                  enum: [admin, editor, viewer]
                  description: The user's role.
      responses:
        '200':
          description: The user was successfully updated.
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  email:
                    type: string
                  first_name:
                    type: string
                  last_name:
                    type: string
                  role:
                    type: string
                  created_at:
                    type: string
                    format: date-time
                  updated_at:
                    type: string
                    format: date-time
        '400':
          description: The request was malformed or contained invalid data.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                  message:
                    type: string
        '401':
          description: The API key is missing or invalid.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                  message:
                    type: string
        '404':
          description: The user with the specified ID was not found.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                  message:
                    type: string
        '500':
          description: An unexpected error occurred on the server.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                  message:
                    type: string
components:
  securitySchemes:
    APIKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
```

**Explanation and Key Improvements:**

*   **OpenAPI/Swagger Compatibility:** The Markdown is structured to be easily converted into a full OpenAPI/Swagger specification. I've also included a YAML snippet that represents the core of the API definition. This is crucial for automated documentation generation and API exploration tools.
*   **Clear Endpoint Description:**  Provides a concise overview of the endpoint's purpose.
*   **Detailed Parameter Documentation:**  Each parameter (path and request body) is clearly defined with its type, requirement status, description, and example value.  The request body schema is explicitly defined.
*   **Comprehensive Response Documentation:**  Each possible response (200, 400, 401, 404, 500) is documented with a description, schema, and example. This helps developers understand the expected responses and how to handle them.
*   **Error Codes and Messages Table:**  A table provides a quick reference for the error codes and their meanings.
*   **Authentication:**  Explicitly states the authentication requirements (API key) and how to include it in the request.  Includes an example of using `X-API-Key`.  The OpenAPI snippet includes a `securitySchemes` section.
*   **Example Request (cURL):**  A practical example using `curl` helps developers quickly test the endpoint.  This is *very* helpful.
*   **YAML Snippet:** This provides a starting point for a full OpenAPI specification.  It includes the `paths` definition for the `/users/{user_id}` PUT endpoint and a `components` section defining the `APIKeyAuth` security scheme.  This makes it easy to import into Swagger Editor or other OpenAPI tools.
*   **Required Fields Clarification:**  The documentation clearly states whether fields in the request body are required or optional.
*   **Enum Values:**  For the `role` field, the allowed values (`admin`, `editor`, `viewer`) are explicitly listed.  This is important for data validation.
*   **Date-Time Format:** The `created_at` and `updated_at` fields in the response are specified with the `date-time` format in the OpenAPI snippet.

**How to Integrate into Your Workflow:**

1.  **Save as `docs/api.md`:**  Save this Markdown content to your `docs/api.md` file.
2.  **Update `README.md`:** Add a link to the `docs/api.md` file in your `README.md` file.  For example:

    ```markdown
    # My User API

    ...

    ## API Documentation

    Detailed API documentation can be found in [docs/api.md](docs/api.md).
    ```

3.  **Use OpenAPI Tools:**  Copy the YAML snippet and paste it into the Swagger Editor (https://editor.swagger.io/) or a similar tool.  You can then generate client SDKs, server stubs, or interactive API documentation.  You can also use tools to automatically generate the OpenAPI specification from annotations in your code (e.g., Springdoc OpenAPI for Java).

This comprehensive documentation will significantly improve the usability and understanding of your User API's UPDATE operation. Remember to keep the documentation up-to-date as your API evolves.
