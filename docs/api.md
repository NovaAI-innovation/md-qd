```markdown
# Orders API - LIST Operation

This document describes the API endpoint for retrieving a list of orders.

## Endpoint: `GET /orders`

**Description:**  Retrieves a list of orders based on the specified query parameters.  Supports pagination and filtering.

**Authentication:**  Requires API Key authentication via the `X-API-KEY` header.

**Parameters:**

| Name        | Type    | In     | Required | Description                                                                                                                                                                                                                            | Example                       |
|-------------|---------|--------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| `page`      | integer | query  | No       | The page number to retrieve.  Defaults to 1.                                                                                                                                                                                          | `1`                             |
| `limit`     | integer | query  | No       | The number of orders to return per page.  Defaults to 20, maximum is 100.                                                                                                                                                               | `20`                            |
| `status`    | string  | query  | No       | Filters the orders by status.  Possible values: `pending`, `processing`, `shipped`, `delivered`, `cancelled`.                                                                                                                             | `shipped`                       |
| `customer_id` | string  | query  | No       | Filters the orders by customer ID.                                                                                                                                                                                                     | `cust123`                       |
| `order_date_from` | string  | query  | No       | Filters orders created on or after this date (inclusive).  Date format: `YYYY-MM-DD`.                                                                                                                                               | `2023-10-26`                    |
| `order_date_to`   | string  | query  | No       | Filters orders created on or before this date (inclusive).  Date format: `YYYY-MM-DD`.                                                                                                                                               | `2023-10-27`                    |
| `sort_by`   | string  | query  | No       | Specifies the field to sort the results by.  Possible values: `order_date`, `total_amount`.  Defaults to `order_date`.                                                                                                             | `total_amount`                |
| `sort_order`| string  | query  | No       | Specifies the sort order.  Possible values: `asc` (ascending), `desc` (descending). Defaults to `desc` when `sort_by` is `order_date`, otherwise defaults to `asc`.                                                                | `asc`                           |

**Request Example:**

```
GET /orders?page=2&limit=10&status=shipped&customer_id=cust123&order_date_from=2023-10-26&order_date_to=2023-10-27&sort_by=total_amount&sort_order=desc
X-API-KEY: YOUR_API_KEY
```

**Response:**

**Success (200 OK):**

```json
{
  "page": 2,
  "limit": 10,
  "total_orders": 50,
  "total_pages": 5,
  "orders": [
    {
      "order_id": "order124",
      "customer_id": "cust123",
      "order_date": "2023-10-27T10:00:00Z",
      "status": "shipped",
      "total_amount": 75.00,
      "shipping_address": {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip": "91234"
      },
      "items": [
        {
          "product_id": "prod1",
          "quantity": 1,
          "price": 25.00
        },
        {
          "product_id": "prod2",
          "quantity": 2,
          "price": 25.00
        }
      ]
    },
    {
      "order_id": "order125",
      "customer_id": "cust123",
      "order_date": "2023-10-27T12:00:00Z",
      "status": "shipped",
      "total_amount": 100.00,
      "shipping_address": {
        "street": "456 Oak Ave",
        "city": "Anytown",
        "state": "CA",
        "zip": "91234"
      },
      "items": [
        {
          "product_id": "prod3",
          "quantity": 1,
          "price": 100.00
        }
      ]
    }
  ]
}
```

**Error Responses:**

| Status Code | Error Code | Description                                                                                                                   | Example Response                                                                                                                                                              |
|-------------|------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 400         | `INVALID_PARAMETER` | One or more query parameters are invalid.  Check the error message for details.                                                                  | ```json { "error_code": "INVALID_PARAMETER", "message": "Invalid value for 'limit'. Must be between 1 and 100." } ```                                      |
| 401         | `UNAUTHORIZED`    | API Key is missing or invalid.                                                                                              | ```json { "error_code": "UNAUTHORIZED", "message": "Invalid API Key" } ```                                                                                                     |
| 500         | `INTERNAL_SERVER_ERROR` | An unexpected error occurred on the server.                                                                                                   | ```json { "error_code": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred." } ```                                                                   |

**Error Code Details:**

*   **`INVALID_PARAMETER`**:  Indicates that one or more of the provided query parameters are invalid. The `message` field will contain specific details about the invalid parameter and the expected format or allowed values.
*   **`UNAUTHORIZED`**: Indicates that the API Key is missing or invalid. Ensure that the `X-API-KEY` header is present and contains a valid API Key.
*   **`INTERNAL_SERVER_ERROR`**: Indicates a server-side error.  This should be investigated on the server logs.

**Notes:**

*   Date and time values are returned in ISO 8601 format (e.g., `YYYY-MM-DDTHH:mm:ssZ`).
*   The `total_orders` field represents the total number of orders matching the filter criteria, regardless of pagination.
*   The `total_pages` field represents the total number of pages available based on the `limit` and the total number of orders.

---

**README.md (Excerpt - relevant section):**

```markdown
## Orders API

This API allows you to manage orders.  Currently, the following operations are supported:

*   **LIST**:  Retrieves a list of orders. See [API Documentation](./docs/api.md) for details.
```
