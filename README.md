# Gradebook

A small Python library that records student marks, converts them to letter
grades, classifies students into academic-standing groups and exports results
as CSV or plain-text reports.

- Language: Python 3.12
- Tests: pytest + pytest-cov (coverage written to `coverage.xml`)
- Static analysis: SonarQube Cloud via GitHub Actions (`.github/workflows/sonarcloud.yml`)

## Run tests locally

```bash
python -m pip install -r requirements-dev.txt
python -m pytest --cov --cov-report=xml:coverage.xml --cov-report=term
```
