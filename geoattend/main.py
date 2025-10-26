from fastapi import FastAPI
from .api.v1 import router_users

app = FastAPI(
    title="GeoAttend API",
    version="0.1.0",
    description="Geoattend Backend"
)

app.include_router(router_users.router, prefix="/api/v1", tags=["Users"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to GeoAttend API"}