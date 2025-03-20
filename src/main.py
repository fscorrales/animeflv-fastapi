from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import animeflv_router

# # tags_metadata = [
# #     {"name": "Auth"},
# #     {"name": "Users"},
# #     {"name": "Products"},
# # ]

# # app = FastAPI(title="Final Project API", openapi_tags=tags_metadata)
app = FastAPI(title="AnimeFLV API")

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
