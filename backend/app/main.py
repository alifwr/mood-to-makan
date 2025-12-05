from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import (
    auth, users, stores, ai, reviews, 
    foods, user_food_history
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(stores.router, prefix=f"{settings.API_V1_STR}/stores", tags=["stores"])
app.include_router(ai.router, prefix=f"{settings.API_V1_STR}/ai", tags=["ai"])
app.include_router(reviews.router, prefix=f"{settings.API_V1_STR}/reviews", tags=["reviews"])
app.include_router(foods.router, prefix=f"{settings.API_V1_STR}/foods", tags=["foods"])
app.include_router(user_food_history.router, prefix=f"{settings.API_V1_STR}/users", tags=["user-food-history"])

@app.get("/")
def root():
    return {"message": "Welcome to Mood2Makan API"}
