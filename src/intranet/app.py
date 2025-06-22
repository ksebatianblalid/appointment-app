"""FastAPI app entry point."""

from fastapi import FastAPI

from src.intranet.api.client import router as client_router

app = FastAPI()
app.include_router(client_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.intranet.app:app", host="0.0.0.0", port=6500, reload=True)
