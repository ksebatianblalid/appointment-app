"""FastAPI app entry point."""

from fastapi import FastAPI

from appointment_app.intranet.api.client import router as client_router

app = FastAPI()
app.include_router(client_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="app:app", host="0.0.0.0", port=6500, reload=True)

    from nicegui import ui
    ui.run(port=8080)  # or any port you prefer
