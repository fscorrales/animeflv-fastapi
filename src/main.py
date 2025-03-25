from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import animeflv_router

# Create a FastAPI instance
app = FastAPI(
    title="AnimeFLV FastAPI",
    description="""
    FastAPI version of animeflv-api for animeflv.net.  
    """,
    contact={
        "name": "GitHub Repository",
        "url": "https://github.com/fscorrales/animeflv-fastapi",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    version="1.0.0",
)


# Include our API routes
app.include_router(animeflv_router)


# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # uvicorn src.main:app --loop asyncio
