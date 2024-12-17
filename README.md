# **Checkout-P2P Python Integration Library**

[![pypi](https://img.shields.io/pypi/v/checkout-p2p.svg)](https://pypi.org/project/checkout-p2p/)
[![codecov](https://codecov.io/github/andrextor/python-checkout/graph/badge.svg?token=XPxrdb1Q2M)](https://codecov.io/github/andrextor/python-checkout)
[![Build Status](https://github.com/andrextor/python-checkout/actions/workflows/python-app.yml/badge.svg)](https://github.com/andrextor/python-checkout/actions)

This project is a Python library inspired by the [PlaceToPay PHP Redirection Library](https://github.com/dnetix/redirection). It is designed to simplify integration with the [PlaceToPay Web Checkout payment gateway](https://docs.placetopay.dev/en/checkout). This library provides a robust and user-friendly solution for managing diverse payment scenarios, including single payments, recurring subscriptions, and payments using subscription tokens.

---

## Integration demo

[Replit Checkout P2P Demo](https://replit.com/@ialopez11012/PlaceToPay-Web-Checkout-Integration-Demo?v=1)

<https://github.com/user-attachments/assets/b2363b94-f59d-4ce4-8a44-72e2e503b6c2>

## Documentation

See the [Web Checkout API docs](https://docs.placetopay.dev/en/checkout).

## Installation

You don’t need this source code unless you intend to modify the package. To simply use the package, you can install it directly by running:

```sh
pip install checkout-p2p
```

## Contribution

If you’d like to contribute, request, or suggest adding new features to the library, please follow the installation guide in our [Contribution Wiki.](https://github.com/andrextor/python-checkout/wiki/Contribution)

### Requirements

- **Python 3.13+**

## Usage

Here’s a quick example to get you started with the library:

1.Configuration

Set up your Settings object with the necessary credentials:

```python
from checkout import Checkout, RedirectRequest

checkout = Checkout({
        "base_url": "https://checkout-co.placetopay.dev/",
        "login": "your_login",
        "tranKey": "your_trankey",
    })
```

2.Create a Payment Request

```python
from checkout import RedirectRequest

redirect_request = RedirectRequest(
        return_url="https://example.com/return",
        ip_address="192.168.1.1",
        user_agent="Test User Agent",
        payment={"reference": "TEST _q", "description": "Test Payment", "amount": {"currency": "COP", "total": 10000}}
    )

response = checkout.request(redirect_request)

print("Redirect to:", response.process_url)
```

3.Query a Payment Request

```python
query_response = checkout.query(123456)  # Replace with your request ID

print("Request Status:", query_response.status)
```

4 Charge using token

```python
from checkout import CollectRequest

collect_request = CollectRequest(
        return_url="https://example.com/return",
        ip_address="192.168.1.1",
        user_agent="Test User Agent",
        instrument={"token": {"token" : "your_token_c5583922eccd6d2061c1b0592b099f04e352a894f37ae51cf1a"}},
        payer={
            "email": "andres2@yopmail.com",
            "name" : "Andres",
            "surname": "López",
            "document": "111111111",
            "documentType": "CC",
            "mobile": "+573111111111"
        },
        payment={
            "reference": "TEST_COllECT", 
            "description": "Test Payment", 
            "amount": {"currency": "COP", "total": 15000}
        }
    )

# Collect. Returns a `InformationResponse` object.
collect_response = checkout.collect(collect_request)

print("Collect Status :", collect_response.status)
```

5.Reverse a Payment

```python
# Reverse a transaction. Returns a `ReverseResponse` object.
reverse_response = checkout.reverse("internal_reference")

print("Reverse Status:", reverse_response.status)
```

6.Invalidate token

```python
invalidate_token_request = {
        "locale": "en_US", 
        "instrument": {"token" : {"token" : "your_token_c5583922eccd6d2061c1b0592b099f04e352a894f37ae51cf1a"}}
}

# invalite token. Returns a `Status` object.
invalidate_response = checkout.invalidate_token(invalidate_token_request)

print("Invalidate Status:", invalidate_response.status)
print("Message:", invalidate_response.message)
```

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
