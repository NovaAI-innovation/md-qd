Okay, here's the API documentation in Markdown format for the `UPDATE` operation for users, designed to be OpenAPI/Swagger compatible. I've included endpoint descriptions, parameters, responses, examples, error codes, and authentication requirements.

```markdown
# User Management API: UPDATE User

## Overview

This endpoint allows you to update an existing user's information.  It requires authentication and specific user roles (e.g., admin) to perform the operation.

**Base URL:** `/api/v1/users`

**Authentication:** Bearer Token Authentication is required.  You must provide a valid JWT (JSON Web Token) in the `Authorization` header.

**Authorization:** Only users with the `admin` role or the user themselves (updating their own profile) can perform this operation.

## Endpoint

**Method:** `PUT`

**Path:** `/api/v1/users/{userId}`

**Description:** Updates the details of a specific user identified by their `userId`.

## Parameters

### Path Parameters

| Name     | Type    | Required | Description                                 | Example |
|----------|---------|----------|---------------------------------------------|---------|
| `userId` | `integer` | Yes      | The unique identifier of the user to update. | `123`   |

### Request Body

The request body should be a JSON object containing the fields to update.  Fields not included in the request body will remain unchanged.

**Schema:**

```json
{
  "firstName": "string",
  "lastName": "string",
  "email": "string",
  "phoneNumber": "string",
  "isActive": "boolean",
  "role": "string"
}
```

**Properties:**

| Name          | Type      | Required | Description                                                                                                | Example        |
|---------------|-----------|----------|------------------------------------------------------------------------------------------------------------|----------------|
| `firstName`   | `string`  | No       | The user's first name.                                                                                      | `"John"`       |
| `lastName`    | `string`  | No       | The user's last name.                                                                                       | `"Doe"`        |
| `email`       | `string`  | No       | The user's email address. Must be a valid email format.                                                       | `"john.doe@example.com"` |
| `phoneNumber` | `string`  | No       | The user's phone number.                                                                                    | `"555-123-4567"`|
| `isActive`    | `boolean` | No       | Indicates whether the user is active.                                                                       | `true`         |
| `role`        | `string`  | No       | The user's role.  Possible values: `admin`, `user`, `editor`.  Only updatable by admins.                     | `"user"`       |

**Example Request Body:**

```json
{
  "firstName": "Jonathan",
  "lastName": "Doe",
  "phoneNumber": "555-987-6543",
  "isActive": true
}
```

## Responses

### 200 OK

Indicates that the user was successfully updated.  The response body contains the updated user object.

**Schema:**

```json
{
  "userId": "integer",
  "firstName": "string",
  "lastName": "string",
  "email": "string",
  "phoneNumber": "string",
  "isActive": "boolean",
  "role": "string",
  "createdAt": "string",
  "updatedAt": "string"
}
```

**Example Response:**

```json
{
  "userId": 123,
  "firstName": "Jonathan",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "phoneNumber": "555-987-6543",
  "isActive": true,
  "role": "user",
  "createdAt": "2023-10-26T10:00:00Z",
  "updatedAt": "2023-10-27T11:30:00Z"
}
```

### 400 Bad Request

Indicates that the request was invalid.  This could be due to invalid data in the request body (e.g., invalid email format) or missing required parameters.

**Example Response:**

```json
{
  "error": "Invalid email format."
}
```

### 401 Unauthorized

Indicates that the user is not authenticated.  The `Authorization` header is missing or contains an invalid token.

**Example Response:**

```json
{
  "error": "Unauthorized"
}
```

### 403 Forbidden

Indicates that the user is authenticated but does not have the necessary permissions to perform this operation.  For example, a regular user trying to update another user's role or a user trying to update a field they are not allowed to change.

**Example Response:**

```json
{
  "error": "Forbidden: Insufficient privileges."
}
```

### 404 Not Found

Indicates that the user with the specified `userId` does not exist.

**Example Response:**

```json
{
  "error": "User not found."
}
```

### 500 Internal Server Error

Indicates that an unexpected error occurred on the server.

**Example Response:**

```json
{
  "error": "Internal Server Error"
}
```

## Example Request

```bash
curl -X PUT \
  '/api/v1/users/123' \
  -H 'Authorization: Bearer <YOUR_JWT_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "firstName": "Jonathan",
    "lastName": "Doe",
    "phoneNumber": "555-987-6543",
    "isActive": true
  }'
```

## Error Codes and Messages

| HTTP Status Code | Error Message                   | Description                                                                                       |
|------------------|---------------------------------|---------------------------------------------------------------------------------------------------|
| 400              | "Invalid email format."         | The provided email address is not in a valid format.                                              |
| 400              | "Invalid phone number format."  | The provided phone number is not in a valid format.                                               |
| 401              | "Unauthorized"                  | The user is not authenticated.                                                                    |
| 403              | "Forbidden: Insufficient privileges." | The user does not have the necessary permissions to perform this operation.                     |
| 404              | "User not found."              | The user with the specified `userId` does not exist.                                             |
| 500              | "Internal Server Error"         | An unexpected error occurred on the server.  Check server logs for more details.                 |

## OpenAPI/Swagger Definition Snippet (YAML)

```yaml
paths:
  /api/v1/users/{userId}:
    put:
      summary: Update an existing user
      description: Updates the details of a specific user identified by their userId.
      security:
        - bearerAuth: []
      parameters:
        - in: path
          name: userId
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
                firstName:
                  type: string
                  description: The user's first name.
                lastName:
                  type: string
                  description: The user's last name.
                email:
                  type: string
                  description: The user's email address.
                phoneNumber:
                  type: string
                  description: The user's phone number.
                isActive:
                  type: boolean
                  description: Indicates whether the user is active.
                role:
                  type: string
                  description: The user's role. Possible values: admin, user, editor. Only updatable by admins.
      responses:
        '200':
          description: Successful update
          content:
            application/json:
              schema:
                type: object
                properties:
                  userId:
                    type: integer
                  firstName:
                    type: string
                  lastName:
                    type: string
                  email:
                    type: string
                  phoneNumber:
                    type: string
                  isActive:
                    type: boolean
                  role:
                    type: string
                  createdAt:
                    type: string
                    format: date-time
                  updatedAt:
                    type: string
                    format: date-time
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

**Explanation and Key Improvements:**

* **OpenAPI/Swagger Compatibility:** The Markdown is structured to directly translate into an OpenAPI/Swagger definition.  The YAML snippet provides a concrete example.  I've included schemas for requests and responses.
* **Detailed Parameter Descriptions:**  Clear descriptions are provided for each parameter, including the type, whether it's required, and example values.
* **Comprehensive Response Handling:**  All possible HTTP status codes (200, 400, 401, 403, 404, 500) are documented with example responses.  Error messages are included.
* **Authentication and Authorization:** The documentation explicitly states the authentication method (Bearer Token) and the authorization requirements (admin role or self-update).  This is crucial for security.
* **Example Request:**  A complete `curl` example is provided to demonstrate how to make the request.
* **Clear Error Codes and Messages Table:**  A table format provides a consolidated view of error codes and their corresponding messages, making it easier for developers to understand potential issues.
* **YAML Snippet:** The YAML snippet gives a clear OpenAPI definition that can be used directly with Swagger tools.  This significantly enhances the documentation's utility.
* **Schema Definitions:** Added schema definitions for both request and response bodies, making the documentation more complete and consistent with OpenAPI standards.
* **`updatedAt` and `createdAt` formats:** added `format: date-time` to the `updatedAt` and `createdAt` properties in the response schema.
* **Security Components:** Added a security component for `bearerAuth` to the OpenAPI definition.

This improved documentation provides a solid foundation for developers to understand and use the User UPDATE API endpoint.  Remember to adapt the code and examples to your specific implementation details.
