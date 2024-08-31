---
title: Endpoint
---

## Overview

Welcome to the PPOB API documentation. This API provides various endpoints to manage user authentication, product
listing, balance transactions, and product transactions.

Server URL:

``` { .json .copy }
https://ppob-fake-api.fly.dev
```

API Version: `1.0.0`

---

## User

### **Login**

<span style="color:#C75151">**POST**</span> **`/api/v1/login`**

- **Summary:** Login with your account
- **Tags:** User

???+ "Content Example"

    === "Request Body"
    
        | Name     | Type   | Required | Description |
        |----------|--------|----------|-------------|
        | password | string | Yes      | User's password |
        | phone    | string | Yes      | User's phone number |
    
        
        ``` { .json .copy }
        {
          "password": "your_password",
          "phone": "1234567890"
        }
        ```
    
    === "Response"
    
        | Name    | Type    | Required | Description |
        |---------|---------|----------|-------------|
        | message | string  | Yes      | Response message |
        | status  | boolean | Yes      | Status of the login operation |
        | data    | object  | Yes      | Login data |
        | token   | string  | Yes      | Authentication token |
    
        
        ``` { .json .copy }
        {
          "message": "Login successful",
          "status": true,
          "data": {
            "token": "your_jwt_token"
          }
        }
        ```

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request POST 'https://ppob-fake-api.fly.dev/api/v1/login' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "password": "string",
        "phone": "string"
    }'
    ```

---

### **Register**

<span style="color:#C75151">**POST**</span> **`/api/v1/register`**

- **Summary:** Register new account
- **Tags:** User

???+ "Content Example"

    === "Request Body"
    
        | Name     | Type   | Required | Description        |
        |----------|--------|----------|--------------------|
        | name     | string | Yes      | User's name        |
        | phone    | string | Yes      | User's phone number|
        | password | string | Yes      | User's password    |
            
        ``` { .json .copy }
        {
          "name": "John Doe",
          "phone": "1234567890",
          "password": "your_password"
        }
    
        ```
    
    === "Response"
    
        | Name    | Type    | Required | Description         |
        |---------|---------|----------|---------------------|
        | message | string  | Yes      | Response message    |
        | status  | boolean | Yes      | Status of the registration |
        | data    | string  | Yes      | Registration data   |
                
        ``` { .json .copy }
        {
          "message": "Registration successful",
          "status": true,
          "data": "User registered"
        }
        ```

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request POST 'https://ppob-fake-api.fly.dev/api/v1/register' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "string",
        "phone": "string",
        "password": "string"
    }'
    ```

---

### **Get User Information**

<span style="color:#45AA4A">**GET**</span> **`/api/v1/user`**

- **Summary:** Get user information
- **Tags:** User

???+ "Content Example"

    === "Header Parameter"
    
        | Name          | In    | Type   | Required | Description                |
        |---------------|-------|--------|----------|----------------------------|
        | Authorization | header| string | Yes       | Bearer token for authorization |
    
    === "Response"
    
        | Name                | Type    | Required | Description                   |
        |---------------------|---------|----------|-------------------------------|
        | message             | string  | Yes      | Response message              |
        | status              | boolean | Yes      | Status of the operation       |
        | data                | object  | Yes      | User data                     |
        | id                  | string  | Yes      | User ID                       |
        | name                | string  | Yes      | User's name                   |
        | phone               | string  | Yes      | User's phone number           |
        | balance             | integer | Yes      | User's balance                |
        | last_update_balance | string  | Yes      | Last update time of the balance |
    
        ``` { .json .copy }
        {
          "message": "User data retrieved successfully",
          "status": true,
          "data": {
            "id": "user_id",
            "name": "John Doe",
            "phone": "1234567890",
            "balance": 100000,
            "last_update_balance": "2024-08-24T10:00:00Z"
          }
        }
        ```

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request GET 'https://ppob-fake-api.fly.dev/api/v1/user' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDQ4NDI1NSwianRpIjoiMWQ0NmIyZjItZTVmNS00ZjE1LThiZjUtOWRjNDYzOTlhNmI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU2YzAyZDFmLWRiOGItNGM4NS1iNjdjLWVmMDYzYzlkOGViMiIsIm5iZiI6MTcyNDQ4NDI1NSwiY3NyZiI6IjIwMzJhYTVjLWMyZDgtNGM2Mi1hNWQxLWQ0Nzk5M2FiNTA0ZSIsImV4cCI6MTcyNDU3MDY1NX0.4NlV9KSzceHFPstFTr073Lo5V5i4_1q1KNBnkLYDFaI' \
    ```

---

## Product

### **Get All Product Postpaid**

<span style="color:#45AA4A">**GET**</span> **`/api/v1/product`**

- **Summary:** Get All product list of postpaid (single shot payment point without inquiry recipient)
- **Tags:** Product
- **Authentication:** No

???+ "Content Example"

    === "Query Parameter"
    
        | Name     | In    | Type   | Required | Description                  |
        |----------|-------|--------|----------|------------------------------|
        | category | query | string | No      | Category of the product      |
        | search   | query | string | No      | Search term for product name |
    
    === "Response"
    
        | Name         | Type    | Required | Description             |
        |--------------|---------|----------|-------------------------|
        | message      | string  | Yes      | Response message        |
        | status       | boolean | Yes      | Status of the operation |
        | data         | array   | Yes      | List of products        |
        | id           | integer | Yes      | Product ID              |
        | code         | string  | Yes      | Product code            |
        | name         | string  | Yes      | Product name            |
        | category     | string  | Yes      | Product category        |
        | sub_category | string  | Yes      | Product sub-category    |
        | description  | string  | Yes      | Product description     |
        | nominal      | integer | Yes      | Product nominal value   |
        | admin_fee    | integer | Yes      | Administrative fee      |
        | service_fee  | integer | Yes      | Service fee             |
        | status       | string  | Yes      | Product status          |
    
        ``` { .json .copy }
        {
          "message": "Products retrieved successfully",
          "status": true,
          "data": [
            {
              "id": 1,
              "code": "PROD001",
              "name": "Product 1",
              "category": "PULSA",
              "sub_category": "TELKOMSEL",
              "description": "Pulsa Telkomsel 10K",
              "nominal": 10000,
              "admin_fee": 1500,
              "service_fee": 500,
              "status": "active"
            },
            {
              "id": 2,
              "code": "PROD002",
              "name": "Product 2",
              "category": "PULSA",
              "sub_category": "INDOSAT",
              "description": "Pulsa Indosat 10K",
              "nominal": 10000,
              "admin_fee": 1500,
              "service_fee": 500,
              "status": "active"
            }
          ]
        }
        ```

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request GET 'https://ppob-fake-api.fly.dev/api/v1/product' \
    ```

---

### **Get All Product Prepaid**

<span style="color:#45AA4A">**GET**</span> **`/api/v1/product/prepaid`**

- **Summary:** Get All product list of prepaid (payment point with inquiry recipient account)
- **Tags:** Product

???+ "Content Example"

    === "Query Parameter"
    
        | Name     | In    | Type   | Required | Description                  |
        |----------|-------|--------|----------|------------------------------|
        | category | query | string | No      | Category of the product      |
        | search   | query | string | No      | Search term for product name |
    
    === "Response"
    
        | Name         | Type    | Required | Description              |
        |--------------|---------|----------|--------------------------|
        | message      | string  | Yes      | Response message         |
        | status       | boolean | Yes      | Status of the operation  |
        | data         | array   | Yes      | List of prepaid products |
        | id           | integer | Yes      | Product ID               |
        | code         | string  | Yes      | Product code             |
        | name         | string  | Yes      | Product name             |
        | category     | string  | Yes      | Product category         |
        | sub_category | string  | Yes      | Product sub-category     |
        | description  | string  | Yes      | Product description      |
        | nominal      | string    | no      | Product nominal value (nullable)    |
        | admin_fee    | integer | Yes      | Administrative fee       |
        | service_fee  | integer | Yes      | Service fee              |
        | status       | string  | Yes      | Product status           |
    
        ``` { .json .copy }
        {
          "message": "Prepaid products retrieved successfully",
          "status": true,
          "data": [
            {
              "id": 1,
              "code": "PROD_PRE_001",
              "name": "Prepaid Product 1",
              "category": "PDAM",
              "sub_category": "JAKARTA",
              "description": "PDAM Jakarta",
              "nominal": null,
              "admin_fee": 2500,
              "service_fee": 1000,
              "status": "active"
            }
          ]
        }
        ```

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request GET 'https://ppob-fake-api.fly.dev/api/v1/product/prepaid' \
    ```

---

### Get All Category Available

<span style="color:#45AA4A">**GET**</span> **`/api/v1/category`**

- **Summary:** Get Product Category list
- **Tags:** Product

???+ "Content Example"

    === "Response"
    

    | Name        | Type    | Required | Description                 |
    |-------------|---------|----------|-----------------------------|
    | message     | string  | Yes      | Response message            |
    | status      | boolean | Yes      | Status of the operation     |
    | data        | array   | Yes      | List of product categories  |

    ``` { .json .copy }
    {
      "message": "Product categories retrieved successfully",
      "status": true,
      "data": [
        {
          "name": "Pulsa",
          "icon": "https://utsmannn.github.io/images/ic-cat-pulsa.png",
          "subcategories": [
            "INDOSAT","TELKOMSEL","XL","TRI","SMARTFREN"
          ]
        },
        {
          "name": "Internet",
          "icon": "https://utsmannn.github.io/images/ic-cat-internet.png",
          "subcategories": ["Internet"]
        },
        {
          "name": "E-Wallet",
          "icon": "https://utsmannn.github.io/images/ic-cat-e-wallet.png",
          "subcategories": [
            "GoPay","OVO","DANA","LinkAja"
          ]
        }
      ]
    }
    ```

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request GET 'https://ppob-fake-api.fly.dev/api/v1/category' \
    ```

---

## Balance Transaction

### **Topup Your Balance Account**

<span style="color:#C75151">**POST**</span> **`/api/v1/topup_balance`**

- **Summary:** Top up Balance with payment simulation by Xendit Test Environment
- **Tags:** Balance Transaction

???+ "Content Example"

    === "Header Parameter"
    
        | Name          | In     | Type   | Required | Description                    |
        |---------------|--------|--------|----------|--------------------------------|
        | Authorization | header | string | Yes       | Bearer token for authorization |
    
    === "Request Body"
    
        | Name   | Type   | Required | Description                 |
        |--------|--------|----------|-----------------------------|
        | amount | string | Yes      | Amount of top-up to balance |
    
        ``` { .json .copy }
        {
          "amount": "100000"
        }
        ```
    
    === "Response"
    
        | Name         | Type    | Required | Description                                      |
        |--------------|---------|----------|--------------------------------------------------|
        | message      | string  | Yes      | Response message                                 |
        | status       | boolean | Yes      | Status of the top-up operation                   |
        | data         | object  | Yes      | Top-up data                                      |
        | id           | string  | Yes      | Top-up transaction ID                            |
        | user_id      | string  | Yes      | User ID                                          |
        | external_id  | string  | Yes      | External ID from payment gateway                 |
        | invoice_url  | string  | Yes      | URL of the payment link by Xendit                |
        | status       | string  | Yes      | Status of the transaction (PENDING, PAID)        |
        | amount       | integer | Yes      | Total amount (nominal + admin fee + service fee) |
        | expired_date | string  | Yes      | Expiration date of the payment                   |
    
        ``` { .json .copy }
        {
          "message": "Top-up successful",
          "status": true,
          "data": {
            "id": "topup_id",
            "user_id": "user_id",
            "external_id": "external_id",
            "invoice_url": "https://payment.link",
            "status": "PENDING",
            "amount": 103000,
            "expired_date": "2024-08-25T10:00:00Z"
          }
        }
        
        ```

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request POST 'https://ppob-fake-api.fly.dev/api/v1/topup_balance' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDQ4NDI1NSwianRpIjoiMWQ0NmIyZjItZTVmNS00ZjE1LThiZjUtOWRjNDYzOTlhNmI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU2YzAyZDFmLWRiOGItNGM4NS1iNjdjLWVmMDYzYzlkOGViMiIsIm5iZiI6MTcyNDQ4NDI1NSwiY3NyZiI6IjIwMzJhYTVjLWMyZDgtNGM2Mi1hNWQxLWQ0Nzk5M2FiNTA0ZSIsImV4cCI6MTcyNDU3MDY1NX0.4NlV9KSzceHFPstFTr073Lo5V5i4_1q1KNBnkLYDFaI' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "amount": "string"
    }'
    ```

---

### **Get Topup Balance History**

<span style="color:#45AA4A">**GET**</span> **`/api/v1/balance_invoice`**

- **Summary:** Get all topup balance history of your account
- **Tags:** Balance Transaction

???+ "Content Example"

    === "Header Parameter"
    
        | Name          | In     | Type   | Required | Description                    |
        |---------------|--------|--------|----------|--------------------------------|
        | Authorization | header | string | Yes       | Bearer token for authorization |
    
    === "Response"
    
        | Name         | Type    | Required | Description                               |
        |--------------|---------|----------|-------------------------------------------|
        | message      | string  | Yes      | Response message                          |
        | status       | boolean | Yes      | Status of the operation                   |
        | data         | array   | Yes      | List of top-up transactions               |
        | id           | string  | Yes      | Transaction ID                            |
        | user_id      | string  | Yes      | User ID                                   |
        | external_id  | string  | Yes      | External ID from payment gateway          |
        | invoice_url  | string  | Yes      | URL of the payment link by Xendit         |
        | status       | string  | Yes      | Status of the transaction (PENDING, PAID) |
        | amount       | integer | Yes      | Total amount of the transaction           |
        | expired_date | string  | Yes      | Expiration date of the transaction        |
    
        ``` { .json .copy }
        {
          "message": "Top-up history retrieved successfully",
          "status": true,
          "data": [
            {
              "id": "topup_id_1",
              "user_id": "user_id_1",
              "external_id": "external_id_1",
              "invoice_url": "https://payment.link",
              "status": "PAID",
              "amount": 103000,
              "expired_date": "2024-08-25T10:00:00Z"
            }
          ]
        }
    
        ```

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request GET 'https://ppob-fake-api.fly.dev/api/v1/balance_invoice' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDQ4NDI1NSwianRpIjoiMWQ0NmIyZjItZTVmNS00ZjE1LThiZjUtOWRjNDYzOTlhNmI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU2YzAyZDFmLWRiOGItNGM4NS1iNjdjLWVmMDYzYzlkOGViMiIsIm5iZiI6MTcyNDQ4NDI1NSwiY3NyZiI6IjIwMzJhYTVjLWMyZDgtNGM2Mi1hNWQxLWQ0Nzk5M2FiNTA0ZSIsImV4cCI6MTcyNDU3MDY1NX0.4NlV9KSzceHFPstFTr073Lo5V5i4_1q1KNBnkLYDFaI' \
    ```

---

## Product Transaction

### **Request New Transaction**

<span style="color:#C75151">**POST**</span> **`/api/v1/transaction`**

- **Summary:** Preliminary step that validates and prepares the transaction details before the actual execution,
  ensuring all conditions are met before processing.
- **Tags:** Product Transaction

???+ "Content Example"

    === "Header Parameter"
    
        | Name          | In     | Type   | Required | Description                    |
        |---------------|--------|--------|----------|--------------------------------|
        | Authorization | header | string | Yes       | Bearer token for authorization |
    
    === "Request Body"
    
        | Name             | Type   | Required | Description         |
        |------------------|--------|----------|---------------------|
        | product_code     | string | Yes      | Code of the product |
        | recipient_number | string | Yes      | Recipient's number  |
    
        ``` { .json .copy }
        {
          "product_code": "PROD001",
          "recipient_number": "1234567890"
        }
        
        ```
    
    === "Response"
    
        | Name             | Type    | Required | Description                       |
        |------------------|---------|----------|-----------------------------------|
        | message          | string  | Yes      | Response message                  |
        | status           | boolean | Yes      | Status of the transaction request |
        | data             | object  | Yes      | Transaction data                  |
        | id               | string  | Yes      | Transaction ID                    |
        | product_code     | string  | Yes      | Product code                      |
        | user_id          | string  | Yes      | User ID                           |
        | amount           | integer | Yes      | Amount of the transaction         |
        | date             | string  | Yes      | Transaction date                  |
        | status           | string  | Yes      | Status of the transaction         |
        | recipient_number | string  | Yes      | Recipient's number                |
        | prepaid_account  | object  | Yes      | Prepaid account information       |
        | merchant_account  | object  | No      | Merchant account information, only from QRIS      |
        | description      | string  | Yes      | Description of the transaction    |
    
        ``` { .json .copy }
        {
          "message": "Transaction requested successfully",
          "status": true,
          "data": {
            "id": "transaction_id",
            "product_code": "PROD001",
            "user_id": "user_id",
            "amount": 105000,
            "date": "2024-08-24T10:00:00Z",
            "status": "PENDING",
            "recipient_number": "1234567890",
            "prepaid_account": {
              "name": "John Doe",
              "number": "1234567890"
            },
            "merchant_account": null,
            "description": "Pulsa Telkomsel 10K"
          }
        }
        ```

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request POST 'https://ppob-fake-api.fly.dev/api/v1/transaction' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDQ4NDI1NSwianRpIjoiMWQ0NmIyZjItZTVmNS00ZjE1LThiZjUtOWRjNDYzOTlhNmI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU2YzAyZDFmLWRiOGItNGM4NS1iNjdjLWVmMDYzYzlkOGViMiIsIm5iZiI6MTcyNDQ4NDI1NSwiY3NyZiI6IjIwMzJhYTVjLWMyZDgtNGM2Mi1hNWQxLWQ0Nzk5M2FiNTA0ZSIsImV4cCI6MTcyNDU3MDY1NX0.4NlV9KSzceHFPstFTr073Lo5V5i4_1q1KNBnkLYDFaI' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "product_code": "string",
        "recipient_number": "string"
    }'
    ```

---

### **Request New QRIS Transaction**

<span style="color:#C75151">**POST**</span> **`/api/v1/transaction/qris`**

- **Summary:** Using QRIS for preliminary step that validates and prepares the transaction details before the actual
  execution, ensuring all conditions are met before processing.
- **Tags:** Product Transaction

???+ "Content Example"

    === "Header Parameter"
    
        | Name          | In     | Type   | Required | Description                    |
        |---------------|--------|--------|----------|--------------------------------|
        | Authorization | header | string | Yes       | Bearer token for authorization |
    
    === "Request Body"
    
        | Name             | Type   | Required | Description         |
        |------------------|--------|----------|---------------------|
        | content     | string | Yes      | Content of QRIS |
        | amount | string | No      | Amount you needed, if amount include in QRIS, you no need this  |
    
        ``` { .json .copy }
        {
          "content": "00020101021126550016ID.CO.SHOPEE.WWW01189360091800000000180202180303UBE51440014ID.CO.QRIS.WWW0215ID20190022915550303UBE5204839853033605802ID5906Baznas6013Jakarta Pusat61051034062070703A016304A402",
          "amount": "20000"
        }
        
        ```
    
    === "Response"
    
        | Name             | Type    | Required | Description                       |
        |------------------|---------|----------|-----------------------------------|
        | message          | string  | Yes      | Response message                  |
        | status           | boolean | Yes      | Status of the transaction request |
        | data             | object  | Yes      | Transaction data                  |
        | id               | string  | Yes      | Transaction ID                    |
        | product_code     | string  | Yes      | Product code                      |
        | user_id          | string  | Yes      | User ID                           |
        | amount           | integer | Yes      | Amount of the transaction         |
        | date             | string  | Yes      | Transaction date                  |
        | status           | string  | Yes      | Status of the transaction         |
        | recipient_number | string  | No      | Recipient's number                |
        | prepaid_account  | object  | No      | Prepaid account information       |
        | merchant_account  | object  | Yes      | Merchant account information, only from QRIS      |
        | description      | string  | Yes      | Description of the transaction    |
    
        ``` { .json .copy }
        {
          "message": "Transaction requested successfully",
          "status": true,
          "data": {
            "id": "transaction_id",
            "product_code": "QRIS",
            "user_id": "user_id",
            "amount": 20000,
            "date": "2024-08-24T10:00:00Z",
            "status": "PENDING",
            "recipient_number": null,
            "prepaid_account": null,
            "merchant_account": {
              "id": "ID2019002291555",
              "name": "Baznas",
              "city": "Jakarta Pusat"
            },
            "description": "Pulsa Telkomsel 10K"
          }
        }
        ```

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request POST 'https://ppob-fake-api.fly.dev/api/v1/transaction' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDQ4NDI1NSwianRpIjoiMWQ0NmIyZjItZTVmNS00ZjE1LThiZjUtOWRjNDYzOTlhNmI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU2YzAyZDFmLWRiOGItNGM4NS1iNjdjLWVmMDYzYzlkOGViMiIsIm5iZiI6MTcyNDQ4NDI1NSwiY3NyZiI6IjIwMzJhYTVjLWMyZDgtNGM2Mi1hNWQxLWQ0Nzk5M2FiNTA0ZSIsImV4cCI6MTcyNDU3MDY1NX0.4NlV9KSzceHFPstFTr073Lo5V5i4_1q1KNBnkLYDFaI' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "product_code": "string",
        "recipient_number": "string"
    }'
    ```

---

### **Execute Transaction**

<span style="color:#C75151">**POST**</span> **`/api/v1/transaction/execute`**

- **Summary:** After you created the transaction, you must execute with your password and impacted to your balance
- **Tags:** Product Transaction

???+ "Content Example"

    === "Header Parameter"
    
        | Name          | In     | Type   | Required | Description                    |
        |---------------|--------|--------|----------|--------------------------------|
        | Authorization | header | string | Yes       | Bearer token for authorization |
    
    === "Request Body"
    
        | Name             | Type   | Required | Description         |
        |------------------|--------|----------|---------------------|
        | transaction_id     | string | Yes      | Id of transaction |
        | password | string | Yes      | Your password account  |
    
        ``` { .json .copy }
        {
          "transaction_id": "qwerty",
          "password": "12345"
        }
        ```
    
    === "Response Body"
    
        | Name             | Type    | Required | Description                                 |
        |------------------|---------|----------|---------------------------------------------|
        | message          | string  | Yes      | Response message                            |
        | status           | boolean | Yes      | Status of the transaction execution         |
        | data             | object  | Yes      | Transaction data                            |
        | id               | string  | Yes      | Transaction ID                              |
        | product_code     | string  | Yes      | Product code                                |
        | user_id          | string  | Yes      | User ID                                     |
        | amount           | integer | Yes      | Amount of the transaction                   |
        | date             | string  | Yes      | Transaction date                            |
        | status           | string  | Yes      | Status of the transaction                   |
        | recipient_number | string  | Yes      | Recipient's number                          |
        | prepaid_account  | object  | No       | Prepaid account information (if applicable) |
        | merchant_account  | object  | No      | Merchant account information, only from QRIS      |
        | description      | string  | Yes      | Description of the transaction              |
    
        ``` { .json .copy }
        {
          "message": "Transaction executed successfully",
          "status": true,
          "data": {
            "id": "transaction_id",
            "product_code": "PROD001",
            "user_id": "user_id",
            "amount": 105000,
            "date": "2024-08-24T10:00:00Z",
            "status": "COMPLETED",
            "recipient_number": "1234567890",
            "prepaid_account": {
              "name": "John Doe",
              "number": "1234567890"
            },
            "description": "Pulsa Telkomsel 10K"
          }
        }
        ```

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request POST 'https://ppob-fake-api.fly.dev/api/v1/transaction/execute' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDQ4NDI1NSwianRpIjoiMWQ0NmIyZjItZTVmNS00ZjE1LThiZjUtOWRjNDYzOTlhNmI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU2YzAyZDFmLWRiOGItNGM4NS1iNjdjLWVmMDYzYzlkOGViMiIsIm5iZiI6MTcyNDQ4NDI1NSwiY3NyZiI6IjIwMzJhYTVjLWMyZDgtNGM2Mi1hNWQxLWQ0Nzk5M2FiNTA0ZSIsImV4cCI6MTcyNDU3MDY1NX0.4NlV9KSzceHFPstFTr073Lo5V5i4_1q1KNBnkLYDFaI' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "transaction_id": "string",
        "password": "string"
    }'
    ```

---

### **Get All History Transaction**

<span style="color:#45AA4A">**GET**</span> **`/api/v1/transaction`**

- **Summary:** Get all transaction history
- **Tags:** Product Transaction

???+ "Content Example"

    === "Header Parameter"
    
        | Name          | In     | Type   | Required | Description                    |
        |---------------|--------|--------|----------|--------------------------------|
        | Authorization | header | string | Yes       | Bearer token for authorization |
    
    === "Response"
    
        | Name             | Type    | Required | Description                                 |
        |------------------|---------|----------|---------------------------------------------|
        | message          | string  | Yes      | Response message                            |
        | status           | boolean | Yes      | Status of the operation                     |
        | data             | array   | Yes      | List of transactions                        |
        | id               | string  | Yes      | Transaction ID                              |
        | product_code     | string  | Yes      | Product code                                |
        | user_id          | string  | Yes      | User ID                                     |
        | amount           | integer | Yes      | Amount of the transaction                   |
        | date             | string  | Yes      | Transaction date                            |
        | status           | string  | Yes      | Status of the transaction                   |
        | recipient_number | string  | No      | Recipient's number                          |
        | prepaid_account  | object  | No       | Prepaid account information (if applicable) |
        | merchant_account  | object  | No      | Merchant account information, only from QRIS      |
        | description      | string  | Yes      | Description of the transaction              |

??? example "Request Example"

    ``` { .shell .copy }
    curl --location --request GET 'https://ppob-fake-api.fly.dev/api/v1/transaction' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDQ4NDI1NSwianRpIjoiMWQ0NmIyZjItZTVmNS00ZjE1LThiZjUtOWRjNDYzOTlhNmI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU2YzAyZDFmLWRiOGItNGM4NS1iNjdjLWVmMDYzYzlkOGViMiIsIm5iZiI6MTcyNDQ4NDI1NSwiY3NyZiI6IjIwMzJhYTVjLWMyZDgtNGM2Mi1hNWQxLWQ0Nzk5M2FiNTA0ZSIsImV4cCI6MTcyNDU3MDY1NX0.4NlV9KSzceHFPstFTr073Lo5V5i4_1q1KNBnkLYDFaI' \
    ```

---