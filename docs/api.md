Okay, here's a Markdown-formatted API documentation for adding an UPDATE operation for users, designed to be OpenAPI/Swagger compatible.  I'll cover the endpoint, parameters, request/response examples, error codes, and authentication.

```markdown
# User Management API - UPDATE User

## Overview

This endpoint allows updating an existing user's information.  It requires authentication and appropriate authorization to modify user data.

**Phase:** Documentation

**Files:** `docs/api.md`, `README.md`

## Endpoint

`PUT /users/{userId}`

## Description

Updates the user with the specified `userId`.  All provided fields will overwrite the existing values.  If a field is not provided, it will remain unchanged.

## Authentication

This endpoint requires a valid Bearer token in the `Authorization` header.  The user associated with the token must have the `users.update` permission.

## Parameters

### Path Parameters

| Name      | Type   | Required | Description                                 |
|-----------|--------|----------|---------------------------------------------|
| `userId`  | `string` | Yes      | The unique identifier of the user to update. |

### Request Body

The request body should be a JSON object containing the user's information to update.

| Name        | Type     | Required | Description                                                                                                                               |
|-------------|----------|----------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `firstName` | `string` | No       | The user's first name.                                                                                                                   |
| `lastName`  | `string` | No       | The user's last name.                                                                                                                    |
| `email`     | `string` | No       | The user's email address.  Must be a valid email format.                                                                                 |
| `isActive`  | `boolean`| No       | Indicates whether the user is active.                                                                                                       |
| `role`      | `string` | No       | The user's role (e.g., "admin", "user", "editor").                                                                                        |
| `phoneNumber`| `string` | No       | The user's phone number                                                                                                                 |

## Request Example

```json
PUT /users/64f8c7d9a0b1c2e3f4567890
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "isActive": true
}
```

## Responses

### 200 OK

The user was successfully updated.

```json
{
  "userId": "64f8c7d9a0b1c2e3f4567890",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "isActive": true,
  "role": "user",
  "phoneNumber": "555-123-4567",
  "createdAt": "2023-09-07T10:00:00Z",
  "updatedAt": "2023-09-07T10:30:00Z"
}
```

### 400 Bad Request

The request was invalid.  Check the request body for errors.

```json
{
  "error": "Invalid request body",
  "message": "The email address is not valid."
}
```

### 401 Unauthorized

The request was not authorized.  Check your authentication token.

```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token."
}
```

### 403 Forbidden

The user does not have permission to update user data.

```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions to update users."
}
```

### 404 Not Found

The user with the specified `userId` was not found.

```json
{
  "error": "Not Found",
  "message": "User with ID '64f8c7d9a0b1c2e3f4567890' not found."
}
```

### 500 Internal Server Error

An unexpected error occurred on the server.

```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred while processing the request."
}
```

## Error Codes

| HTTP Status Code | Error Code         | Description                                                                                                |
|--------------------|--------------------|------------------------------------------------------------------------------------------------------------|
| 400                | `invalid_request`  | The request body is invalid or contains missing required fields.                                        |
| 401                | `unauthorized`     | The request requires authentication.                                                                     |
| 403                | `forbidden`        | The user does not have the necessary permissions to perform this action.                                  |
| 404                | `resource_not_found`| The requested resource (user) was not found.                                                            |
| 500                | `internal_error`   | An unexpected error occurred on the server.                                                              |

## OpenAPI/Swagger Specification Snippet (Example)

```yaml
paths:
  /users/{userId}:
    put:
      summary: Update User
      description: Updates an existing user.
      security:
        - bearerAuth: []
      parameters:
        - in: path
          name: userId
          schema:
            type: string
          required: true
          description: The ID of the user to update.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                firstName:
                  type: string
                  description: The user's first name.
                lastName:
                  type: string
                  description: The user's last name.
                email:
                  type: string
                  format: email
                  description: The user's email address.
                isActive:
                  type: boolean
                  description: Whether the user is active.
                role:
                  type: string
                  description: The user's role.
                phoneNumber:
                  type: string
                  description: The user's phone number
      responses:
        '200':
          description: Successful update.
          content:
            application/json:
              schema:
                type: object
                properties:
                  userId:
                    type: string
                  firstName:
                    type: string
                  lastName:
                    type: string
                  email:
                    type: string
                  isActive:
                    type: boolean
                  role:
                    type: string
                  phoneNumber:
                    type: string
                  createdAt:
                    type: string
                    format: date-time
                  updatedAt:
                    type: string
                    format: date-time
        '400':
          description: Bad Request.
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
          description: Unauthorized.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                  message:
                    type: string
        '403':
          description: Forbidden.
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
          description: Not Found.
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
          description: Internal Server Error.
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
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

```

**Explanation and Key Improvements:**

* **OpenAPI/Swagger Compatibility:** The documentation is structured to easily translate into a full OpenAPI/Swagger specification.  I've provided a YAML snippet as an example.  The use of `schema`, `type`, `format`, and descriptions aligns with the OpenAPI standard.
* **Comprehensive Parameter Documentation:**  Clearly defines path parameters and request body parameters, including their types, whether they are required, and detailed descriptions.
* **Detailed Request/Response Examples:**  Provides realistic JSON examples for both the request and various response scenarios (success and error cases).
* **Error Handling:** Documents common error codes (400, 401, 403, 404, 500) and their corresponding messages, making it easier for developers to debug issues.  Includes a table summarizing the error codes.
* **Authentication:**  Specifies the authentication requirements (Bearer token) and the necessary permissions (`users.update`).  Includes an example `Authorization` header.
* **Clear Endpoint Description:**  A concise explanation of what the endpoint does.
* **YAML Snippet:** A YAML snippet illustrating how the documentation translates to a Swagger specification. This is a key addition for direct import into Swagger tools.  It includes the `securitySchemes` component for defining the Bearer token authentication.
* **`Content-Type` Header:** Added the `Content-Type` header to the request example for clarity.
* **`updatedAt` and `createdAt` fields in response** Added those fields to the response to show how they would be returned in a real world scenario.
* **Role field** Added role field to the request body to allow update of the user's role.
* **Phone Number field** Added phone number field to the request body to allow update of the user's phone number.

**How to Use:**

1.  **Copy and Paste:** Copy the Markdown content into your `docs/api.md` file.
2.  **Update Placeholders:** Replace the placeholder values (e.g., `userId`, example token) with your actual values.
3.  **Integrate with Swagger:** Use a tool like Swagger Editor (editor.swagger.io) or Swagger UI to visualize and interact with your API documentation.  You can either write the complete OpenAPI specification or use the provided YAML snippet as a starting point.
4.  **README.md Integration:**  In your `README.md`, include a link to `docs/api.md` and a brief summary of the API.  For example:

    ```markdown
    # User Management API

    This API provides endpoints for managing user accounts.  See the [API documentation](docs/api.md) for details.
    ```

This comprehensive documentation should give developers a clear understanding of how to use the UPDATE user endpoint. Remember to adapt it to your specific implementation details.
