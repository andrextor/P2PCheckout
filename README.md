
# **python-checkout Python Integration Library**

[![codecov](https://codecov.io/github/andrextor/python-checkout/graph/badge.svg?token=XPxrdb1Q2M)](https://codecov.io/github/andrextor/python-checkout)
[![Build Status](https://github.com/andrextor/python-checkout/actions/workflows/python-app.yml/badge.svg)](https://github.com/andrextor/python-checkout/actions)

This project is a Python library inspired by the [PlaceToPay PHP Redirection Library](https://github.com/dnetix/redirection). It aims to provide a robust and easy-to-use solution for integrating with PlaceToPay's payment gateway using Python. The library incorporates some enhancements to better fit Python's ecosystem and leverages modern Python tools like Pydantic and Requests for validation and HTTP handling.

---

> This `README.md` provides guidance on setting up and using the package in a local development environment. If you are looking to install and use the package in your project, please refer to the [Wiki - Quick Start](https://github.com/andrextor/python-checkout/wiki/Quick-Start). Additional documentation and detailed guides are available in the [Wiki](https://github.com/andrextor/python-checkout/wiki).

---

## **Table of contents**

1. [Features](#features)
2. [Technologies used](#technologies-used)
3. [Development setup](#development-setup)
    - [Installation for local development](#installation-for-local-development)
    - [Testing and code quality](#testing-and-code-quality)
    - [Adding dependencies](#adding-dependencies)
4. [Contributing](#contributing)
5. [License](#license)

---

## **Features**

- 🛠 **Inspired by Dnetix PHP Library**: A Python adaptation of the official PHP library, keeping the core concepts and enhancing usability.
- 🔑 **Authentication Management**: Easily handle login and transaction keys with dynamic nonce and seed generation.
- 📡 **Request Handling**: Create, query, collect, and reverse payment requests with ease.
- ✅ **Validation with Pydantic**: Ensures data integrity and validation throughout the library.
- 🌐 **HTTP Client Integration**: Built on top of the `requests` library for simplicity and flexibility.
- 🔍 **Logging**: Built-in logging for tracing requests and responses.

---

## **Technologies used**

- **Python 3.13+**
- **Pydantic**: For model validation and serialization.
- **Requests**: For HTTP client requests.
- **Logging**: To log and debug processes.
- **Typing**: To ensure type safety and better developer experience.

---

## **Development setup**

### **Installation for local development**

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

- **Centralized virtual environments** (default): Poetry places the virtual environments in a central location for all Poetry-managed projects:
  `~/.cache/pypoetry/virtualenvs/`

- **Project-Specific virtual environments** (optional): If you prefer the virtual environment to be created within your project directory (e.g., `./.venv`), you can configure Poetry to do so:

  ```bash
  poetry config virtualenvs.in-project true
  ```

Activate the environment:

```bash
poetry shell
```

### **Testing and code quality**

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

### **Adding dependencies**

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