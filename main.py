from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Load constants with default values if not set
SERVER_URL = os.getenv("SERVER_URL", "0.0.0.0")
PORT = os.getenv("PORT", 8000)
ENV = os.getenv("ENV", "dev")

# Import the calculator router safely
try:
    from apps.calculator.route import router as calculator_router
except ImportError:
    calculator_router = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

# Initialize the FastAPI application
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,  # Allow sending cookies or credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Health check endpoint
@app.get("/")
async def health():
    return {"message": "Server is running"}

# Include the calculator router if available
if calculator_router:
    app.include_router(calculator_router, prefix="/calculate", tags=["Calculator"])
else:
    @app.get("/calculate")
    async def placeholder():
        return {"message": "Calculator endpoint is not configured yet"}

# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVER_URL, port=int(PORT), reload=(ENV == "dev"))
