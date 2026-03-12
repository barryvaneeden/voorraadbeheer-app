# CLAUDE.md — Voorraadbeheer App

This file documents the codebase structure, conventions, and workflows for AI assistants working on this project.

## Project Overview

**voorraadbeheer-app** is a Dutch-language inventory management (voorraadbeheer) web application for a furniture business. It is built with **Python + Streamlit** and uses **JSON files** for persistent storage. The app covers multiple business functions: CRM, inventory, orders, invoicing, planning, and administration.

## Running the Application

```bash
# Install dependencies
pip3 install -r requirements.txt

# Start the Streamlit app (default port 8501)
streamlit run app.py

# Dev container variant (CORS/XSRF disabled for local dev)
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

The app is accessible at `http://localhost:8501` by default.

## Repository Structure

```
voorraadbeheer-app/
├── app.py                    # Entry point — sidebar navigation + module routing
├── requirements.txt          # Python dependencies (streamlit, pandas)
├── instellingen.json         # Static config: product categories & supplier names
├── README.md                 # Minimal project readme
├── .devcontainer/
│   └── devcontainer.json     # VS Code dev container (Python 3.11)
├── data/                     # Runtime data storage (JSON files)
│   ├── field_settings.json   # Dynamic form field definitions per module
│   ├── crm_data.json         # CRM records
│   ├── orders_data.json      # Orders records
│   ├── voorraad_data.json    # Inventory records
│   └── planning_data.json    # Planning records
└── modules/                  # Feature modules — one file per module
    ├── beheer.py             # Admin: manage dynamic form fields (fully implemented)
    ├── crm.py                # Customer management (stub)
    ├── voorraad.py           # Inventory management (stub)
    ├── orders.py             # Orders management (stub)
    ├── facturatie.py         # Invoicing/billing (stub)
    ├── planning.py           # Scheduling/planning (stub)
    ├── dashboard.py          # Analytics dashboard (stub)
    ├── export_data.py        # Data export (stub)
    └── reminders.py          # Automated reminders (stub)
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Web framework | Streamlit |
| Data manipulation | pandas |
| Storage | JSON files (no database) |
| Dev environment | VS Code dev container |

## Module Architecture

Every module in `modules/` exposes a single public entry point called by `app.py`:

```python
def show():
    # all UI and logic for this module
```

`app.py` routes to modules based on the sidebar `st.selectbox` selection:

```python
if menu == "CRM":
    crm.show()
elif menu == "Beheer":
    beheer.show()
# etc.
```

When implementing a new module, always expose `show()` as the entry point and add a corresponding branch in `app.py`.

## Data Storage Pattern

All data is persisted as JSON files in the `data/` directory. The canonical pattern (from `beheer.py`):

```python
SETTINGS_FILE = "data/field_settings.json"

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
```

- Use `os.path.exists()` to create a file if it doesn't exist yet.
- Always write with `indent=4` for human-readable output.
- No migrations exist — schema changes require manual data file updates.

## Dynamic Form Fields

`beheer.py` manages per-module form field configurations stored in `data/field_settings.json`. Structure:

```json
{
  "crm": [
    {"label": "Naam klant", "type": "text", "required": true},
    {"label": "Email", "type": "email"}
  ],
  "voorraad": [],
  "orders": [],
  "facturatie": [],
  "planning": []
}
```

Supported field types: `text`, `number`, `email`, `date`, `textarea`, `selectbox`, `status`.

When implementing stub modules, use `load_settings()` from `beheer.py` to render the configured fields dynamically.

## Static Configuration

`instellingen.json` contains product categories and supplier names. **Note:** this file currently has JSON syntax errors (missing commas between array elements). Fix before parsing programmatically:

```json
{
    "Productgroepen": ["Stoelen", "Tafels", "Bureaus", "Kasten", ...],
    "Leveranciers": ["Vepa", "Vitra", "Gispen", "Casala", ...]
}
```

## Language Convention

The application UI and all variable names relating to business domain are in **Dutch**:
- `voorraadbeheer` = inventory management
- `beheer` = administration
- `orders` = orders
- `facturatie` = invoicing
- `planning` = planning
- `leveranciers` = suppliers
- `productgroepen` = product categories

Code (function names, Python identifiers, comments) may be in Dutch or English — follow whatever is already used in the file you are editing.

## Code Style

- **Python**: standard snake_case, no type annotations in existing code
- **Streamlit**: use `st.rerun()` (not deprecated `st.experimental_rerun()`)
- **Forms**: use `st.form` + `st.form_submit_button` for multi-field inputs to avoid re-running on each widget interaction
- **Columns**: use `st.columns()` for side-by-side layouts
- No linter or formatter is configured — keep code consistent with existing style

## Testing

There are currently **no tests**. When adding tests:
- Use `pytest` (add to `requirements.txt`)
- Place test files in a `tests/` directory with `test_*.py` naming
- Test data manipulation logic separately from Streamlit UI code

## Known Issues / Technical Debt

- `instellingen.json` has JSON syntax errors (missing commas) — must be fixed before use
- All modules except `beheer.py` are stubs with only `def show(): pass`
- No error handling or input validation on file I/O operations
- No authentication or access control
- `export_data.py` and `reminders.py` use `app()` as entry point instead of `show()` — standardize to `show()` when implementing

## Development Workflow

1. Create a feature branch from `master`
2. Implement changes in the relevant module file(s)
3. Run the app locally to verify (`streamlit run app.py`)
4. Commit with a clear message describing what was changed
5. Push branch and open a PR against `master`

## Dev Container

The `.devcontainer/devcontainer.json` configures a reproducible environment:
- Base image: `mcr.microsoft.com/devcontainers/python:1-3.11-bullseye`
- VS Code extensions: Python, Pylance
- On container start: installs `requirements.txt` and launches Streamlit on port 8501
