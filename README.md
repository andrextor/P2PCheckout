# **python-checkout Python Integration Library**

[![codecov](https://codecov.io/github/andrextor/python-checkout/graph/badge.svg?token=XPxrdb1Q2M)](https://codecov.io/github/andrextor/python-checkout)
[![Build Status](https://github.com/andrextor/python-checkout/actions/workflows/python-app.yml/badge.svg)](https://github.com/andrextor/python-checkout/actions)

This project is a Python library inspired by the [PlaceToPay PHP Redirection Library](https://github.com/dnetix/redirection). It aims to provide a robust and easy-to-use solution for integrating with PlaceToPay's payment gateway using Python. The library incorporates some enhancements to better fit Python's ecosystem and leverages modern Python tools like Pydantic and Requests for validation and HTTP handling.

---

## **Table of Contents**

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Quick Start](#quick-start)
    - [Installing the Package](#installing-the-package)
    - [Basic Usage](#basic-usage)
4. [Development Setup](#development-setup)
    - [Installation for Local Development](#installation-for-local-development)
    - [Testing and Code Quality](#testing-and-code-quality)
    - [Adding Dependencies](#adding-dependencies)
5. [Project Structure](#project-structure)
6. [Contributing](#contributing)
7. [License](#license)

---

## **Features**

- 🛠 **Inspired by Dnetix PHP Library**: A Python adaptation of the official PHP library, maintaining core concepts and improving usability.
- 🔑 **Authentication Management**: Easily handle login and transaction keys with dynamic nonce and seed generation.
- 📡 **Request Handling**: Create, query, collect, and reverse payment requests with ease.
- ✅ **Validation with Pydantic**: Ensures data integrity and validation throughout the library.
- 🌐 **HTTP Client Integration**: Built on top of the `requests` library for simplicity and flexibility.
- 🔍 **Logging**: Built-in logging for tracing requests and responses.

---

## **Technologies Used**

- **Python 3.13+**
- **Pydantic**: For model validation and serialization.
- **Requests**: For HTTP client requests.
- **Logging**: To log and debug processes.
- **Typing**: To ensure type safety and improve developer experience.

---

## **Quick Start**

### **Installing the Package**

To install the library in your Python project, run:

```bash
pip install p2pcheckout
```

### **Basic Usage**

Here’s an example to get started:

#### 1. Configuration

Set up your Settings object with the necessary credentials:

```python
from checkout import Checkout

# Configuration
config = {
    "base_url": "https://example.placetopay.com/redirection/",
    "login": "your_login",
    "tranKey": "your_transaction_key",
    "timeout": 10,
    "headers": {"Accept": "application/json", 'Content-Type': 'application/json'},
}

checkout = Checkout(**config)
```

#### 2. Create a Payment Request

```python
from messages.requests.redirect import RedirectRequest
from messages.responses.redirect import RedirectResponse

redirect_request = RedirectRequest(
    amount={"currency": "COP", "total": 10000},
    payment={"reference": "TEST123", "description": "Test Payment"}
)

# This request returns a `RedirectResponse` object containing the process URL.
response: RedirectResponse = checkout.request(redirect_request)

print("Redirect to:", response.process_url)
```

#### 3. Query a Payment Request

```python
from messages.responses.information import RedirectInformation

# Query a session by request ID. Returns a `RedirectInformation` object.
query_response: RedirectInformation = checkout.query(123456)  # Replace with your request ID

print("Request Status:", query_response.status)
```

#### 4. Reverse a Payment

```python
from messages.responses.reverse import ReverseResponse

# Reverse a transaction. Returns a `ReverseResponse` object.
reverse_response: ReverseResponse = checkout.reverse("internal_reference")

print("Reverse Status:", reverse_response.status)
```

---

## **Development Setup**

### **Installation for Local Development**

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/andrextor/python-checkout.git
cd python-checkout
```

Install Poetry if not already installed:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Install dependencies:

```bash
poetry install --no-root
```

To activate the development environment:

- **Centralized Virtual Environments** (default): Poetry places the virtual environments in a central location for all Poetry-managed projects:
  `~/.cache/pypoetry/virtualenvs/`

- **Project-Specific Virtual Environments** (optional): If you prefer the virtual environment to be created within your project directory (e.g., `./.venv`), you can configure Poetry to do so:

  ```bash
  poetry config virtualenvs.in-project true
  ```

Activate the environment:

```bash
poetry shell
```

### **Testing and Code Quality**

Run tests:

```bash
poetry run pytest --cov=src
```

Use the following commands for code formatting and linting:

```bash
poetry run black .
poetry run flake8
poetry run isort .
```

Run type checks using mypy:

```bash
poetry run mypy src
```

### **Adding Dependencies**

To manage dependencies for your project, use Poetry as follows:

- Add a runtime dependency:

  ```bash
  poetry add <package_name>
  ```

- Add a development dependency:

  ```bash
  poetry add --group dev <package_name>
  ```

This ensures that your project remains modular and adheres to best practices for dependency management.

---

## **Project Structure**

- **entities**: Core models like Settings, Authentication, and payment-related entities (Amount, Transaction, etc.).
- **messages**: Request and response objects for PlaceToPay interactions.
- **exceptions**: Custom exception handling for the library.
- **client**: HTTP client interactions, including RestCarrier.
- **contracts**: Interfaces for reusable components.
- **tests**: Unit tests for validating the library's functionality.

---

## **Contributing**

We welcome contributions! Follow these steps to contribute:

1. Fork the repository:

   ```bash
   git fork https://github.com/andrextor/python-checkout.git
   ```

2. Create a feature branch:

   ```bash
   git checkout -b feature/new-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add new feature"
   ```

4. Push to the branch:

   ```bash
   git push origin feature/new-feature
   ```

5. Open a pull request on GitHub.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.