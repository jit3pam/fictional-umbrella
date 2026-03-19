# fictional-umbrella

Minimal Selenium automation framework in Python using Page Objects, a central action executor, and pytest.

## Project structure

```text
.
├── conftest.py
├── core/
│   ├── action_executor.py
│   ├── base_element.py
│   ├── base_page.py
│   ├── elements/
│   │   ├── button.py
│   │   ├── dropdown.py
│   │   └── input.py
│   └── locator.py
├── pages/
│   └── login_page.py
├── requirements.txt
└── tests/
    ├── test_bidi.py
    └── test_login.py
```

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Run tests

```bash
pytest -q
```

## Included examples

- `tests/test_login.py` exercises the page-object login flow against The Internet's login form.
- `tests/test_bidi.py` adds BiDi smoke tests for basic auth headers, performance metrics, and cookie injection using Chrome DevTools support exposed by Selenium.
