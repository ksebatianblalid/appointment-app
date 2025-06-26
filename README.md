# appointment-app

A modern appointment scheduling application designed for cloud-native deployments. This project provides a robust backend API, a user-friendly web interface, and integrations with Google Cloud and messaging services for reminders and notifications.

## Features
- Client management (name, surname, phone, email, client ID)
- Appointment scheduling and reminders
- RESTful API with FastAPI
- Responsive UI with NiceGUI
- Google Cloud integration: Firestore, Cloud Storage, Cloud Functions, Cloud Scheduler, Cloud Run
- Notification support via Twilio (SMS) and SendGrid (email)
- Configuration management with Box
- Containerized with Docker for easy deployment
- Fully tested with pytest

## Tech Stack

- **Python**
    - Python 3.12
    - FastAPI (API backend)
    - NiceGUI ([examples](https://nicegui.io/#examples)) (UI)
    - Box (configuration)
- **Google Cloud**
    - Google Cloud Storage
    - Firestore
    - Cloud Function
    - Cloud Scheduler
    - Cloud Run
        * [Integrate Firestore](https://cloud.google.com/run/docs/integrate/firestore?hl=es-419)
        * [Continuous Deployment](https://cloud.google.com/run/docs/quickstarts/deploy-continuously?hl=es-419)
- **Messaging**
    - Twilio (SMS)
    - SendGrid (Email)
- **Testing**
    - pytest
- **Containerization**
    - Docker

## Getting Started

1. Clone the repository and install dependencies using [pyproject.toml](pyproject.toml).
2. Configure environment variables for Google Cloud and messaging services.
3. Run the FastAPI backend and NiceGUI frontend.
4. Deploy to Google Cloud Run using the provided Dockerfile.

See the documentation for detailed setup and usage instructions.





