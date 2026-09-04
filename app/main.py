from fastapi import FastAPI

from app.api.routes.users import router as users_router


# Create the main FastAPI application instance.
# This is the entry point for our API and is used to register
# application-wide configuration and routes.
app = FastAPI(
    title="Blockchain Payment API",
    version="1.0.0",
)


# Register the users router with the main application.
# This keeps user-related endpoints separated from the main application file.
app.include_router(users_router)


# Root endpoint used to confirm that the API is running.
@app.get("/")
def root():
    return {
        "message": "Blockchain Payment API is running"
    }


# Simple endpoint used to verify that the application
# can communicate with the configured database.
@app.get("/db-test")
def db_test():
    return {
        "message": "Database connection is working"
    }