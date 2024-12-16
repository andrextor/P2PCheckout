
# **Checkout-P2P Python Integration Library**

[![pypi](https://img.shields.io/pypi/v/checkout-p2p.svg)](https://pypi.org/project/checkout-p2p/)
[![codecov](https://codecov.io/github/andrextor/python-checkout/graph/badge.svg?token=XPxrdb1Q2M)](https://codecov.io/github/andrextor/python-checkout)
[![Build Status](https://github.com/andrextor/python-checkout/actions/workflows/python-app.yml/badge.svg)](https://github.com/andrextor/python-checkout/actions)

This project is a Python library inspired by the [PlaceToPay PHP Redirection Library](https://github.com/dnetix/redirection). It is designed to simplify integration with the [PlaceToPay Web Checkout payment gateway](https://docs.placetopay.dev/en/checkout). This library provides a robust and user-friendly solution for managing diverse payment scenarios, including single payments, recurring subscriptions, and payments using subscription tokens.

---

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
        "login": "e3bba31e633c32c48011a4a70ff60497",
        "tranKey": "ak5N6IPH2kjljHG3",
    })
```

2.Create a Payment Request

```python
from checkout import RedirectRequest

redirect_request = RedirectRequest(
        returnUrl="https://example.com/return",
        ipAddress="192.168.1.1",
        userAgent="Test User Agent",
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

4.Reverse a Payment

```python

# Reverse a transaction. Returns a `ReverseResponse` object.
reverse_response = checkout.reverse("internal_reference")

print("Reverse Status:", reverse_response.status)
```

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
