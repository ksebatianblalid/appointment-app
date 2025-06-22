# GitHub Copilot Instructions for Appointment App

## General Rules
- All code must comply with PEP8.
- If a function or method is added, a corresponding test must be created using pytest.
- Use Python 3.12 as the base version.

## Frameworks and Services
- Backend: FastAPI
- UI: NiceGUI
- Deployment: Google Cloud Run
- Database: Google Cloud Firestore
- File Storage: Google Cloud Storage
- Testing: pytest
- Containerization: Docker

## Best Practices
- Document all functions and methods with docstrings.
- Use static typing (type hints) in all functions and methods.
- Maintain separation of concerns (UI, business logic, data access).
- Do not store credentials in the repository. Use environment variables or Google Secret Manager.
- FastAPI endpoints must validate data with Pydantic.
- Tests must be in a `tests/` folder and cover both positive and negative cases.
- Use only `pyproject.toml` for dependencies and project metadata.
- For configuration variables, use the [Box](https://pypi.org/project/python-box/) library to manage and access settings in a structured way.

## Example Workflow
1. Create a new function in the backend (FastAPI):
    - Add the function in the appropriate file.
    - Add the test in `tests/`.
    - Verify PEP8 compliance.
2. If modifying the UI (NiceGUI):
    - Keep presentation logic separate from business logic.
    - Add tests if applicable.
3. For deployment on Cloud Run:
    - Include an optimized `Dockerfile` for Python 3.12.
    - Use environment variables for configuration.
4. For Firestore and Storage:
    - Use the official Google Cloud libraries.
    - Handle errors and reconnections.

## Commits and Pull Requests
- Commit messages must be clear and descriptive.
- All changes must go through Pull Request and code review.
- Run all tests before merging.

## Security
- Do not expose sensitive data in logs or API responses.
- Validate and sanitize all user input.

## Standard Python Project Structure

Recommended folder structure for this project:

```
src/
    intranet/           # Main application package
        __init__.py
        app.py                # FastAPI app entry point
        ui/                    # NiceGUI UI components
            __init__.py
            ...
        api/                   # API endpoints and routers
            __init__.py
            ...
        models/                # Pydantic models and data schemas
            __init__.py
            ...
        services/              # Business logic and service classes
            __init__.py
    
            ...
    reminders/             # Reminder logic (e.g., Twilio integration)
        __init__.py
        app.py
        ...
    db/                    # Firestore and storage access logic
        __init__.py
        ...
    utils/                 # Utility functions
        __init__.py
    conf/                 # Configuration management using Box
        __init__.py
        settings.py          # Configuration settings using Box
        application.json     # Application configuration
        development/
        
tests/                     # Pytest test cases
Dockerfile                 # For Cloud Run deployment
pyproject.toml             # Project metadata and dependencies
README.md                  # Project documentation
```

- Keep all application code inside the `src/` package.
- Place all tests in the `tests/` folder, mirroring the app structure where possible.
- Do not commit sensitive files like `.env`.

---

Follow these instructions to maintain the quality and security of the project.