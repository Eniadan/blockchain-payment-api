from fastapi import FastAPI


app = FastAPI(
    title="Blockchain Payment API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Blockchain Payment API is running"
    }