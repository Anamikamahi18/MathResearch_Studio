# Contributing to MathResearch Studio

Thank you for your interest in contributing to **MathResearch Studio**! This document outlines how to participate in the project, submit improvements, and maintain the quality standards of the codebase.

---

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Setup](#development-setup)
5. [Coding Standards](#coding-standards)
6. [Testing Requirements](#testing-requirements)
7. [Pull Request Process](#pull-request-process)
8. [Reporting Bugs](#reporting-bugs)
9. [Suggesting Features](#suggesting-features)

---

## Code of Conduct

By participating in this project, you agree to uphold the [Code of Conduct](./CODE_OF_CONDUCT.md). Please treat all contributors with respect and professionalism.

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/MathResearch_Studio.git
   cd MathResearch_Studio
   ```
3. **Set up** the development environment (see [Development Setup](#development-setup)).
4. **Create a branch** for your work:
   ```bash
   git checkout -b feature/my-improvement
   ```

---

## How to Contribute

### Good First Contributions
- Improve documentation, docstrings, or inline comments.
- Fix typos in the README, docs, or UI text.
- Add additional test cases for existing functionality.
- Improve error messages for better user clarity.

### Larger Contributions
- New export format adapters.
- Additional LLM provider adapters (`OpenAIAdapter`, `OllamaAdapter`).
- Performance improvements for the embedding or retrieval pipeline.
- UI improvements that preserve the researcher-friendly interface design.

---

## Development Setup

### Prerequisites
- Python 3.11+ (3.12 recommended)
- Git

### Steps
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Verify setup by running all tests
python -m pytest
```

All **225 tests** should pass before you begin making changes.

---

## Coding Standards

- **Style**: Follow [PEP 8](https://peps.python.org/pep-0008/) Python style guidelines.
- **Docstrings**: Use Google Python docstring style for all public classes and methods.
- **Type Hints**: Add type annotations for all function parameters and return types.
- **Logging**: Use the project logger (`logging.getLogger(__name__)`) — do not use `print()` in module code.
- **Modularity**: Keep UI, parsing, retrieval, and RAG logic in their respective layers. Avoid cross-layer coupling.
- **No New Dependencies**: If a new dependency is required, discuss it in an issue first.

---

## Testing Requirements

All contributions must maintain or improve test coverage:

- **Run the full test suite** before submitting:
  ```bash
  python -m pytest
  ```
- **Add tests** for any new behavior you introduce.
- **Do not break** existing tests.
- **Target**: 225/225 tests passing (100% pass rate).

---

## Pull Request Process

1. Ensure all tests pass locally.
2. Update documentation if your change affects behavior or interfaces.
3. Write a clear PR description:
   - **What** changed.
   - **Why** it was changed.
   - **How** to test the change.
4. Keep PRs focused — one logical change per PR.
5. A maintainer will review and provide feedback within a reasonable time.

---

## Reporting Bugs

Please open a [GitHub Issue](https://github.com/Anamikamahi18/MathResearch_Studio/issues) with:
- A clear title describing the bug.
- Steps to reproduce the issue.
- Expected behaviour vs. actual behaviour.
- Python version and OS environment.

---

## Suggesting Features

Open a [GitHub Issue](https://github.com/Anamikamahi18/MathResearch_Studio/issues) labelled `enhancement` with:
- A clear description of the proposed feature.
- The use case it addresses for mathematics researchers.
- Any relevant references or prior art.

---

Thank you for helping make MathResearch Studio better for the mathematics research community!
