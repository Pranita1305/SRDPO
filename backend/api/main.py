# FastAPI entry point
from fastapi import FastAPI
from backend.api.routes import protected_routes, auth_routes

app = FastAPI(title="SRDAPO API")

# Routes
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(protected_routes.router, prefix="/protected", tags=["Protected"])

@app.get("/")
def root():
    return {"msg": "Welcome to SRDAPO API"}

from fastapi import FastAPI
from backend.api.routes import auth_routes, demand_routes, fare_routes, protected_routes

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(demand_routes.router)
app.include_router(fare_routes.router)
app.include_router(protected_routes.router)
