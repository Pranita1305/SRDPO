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

from fastapi import FastAPI
from backend.api.routes import auth_routes, protected_routes, demand_routes, fare_routes, zone_routes

app = FastAPI(title="SRDAPO Backend")

# Include routers
app.include_router(auth_routes.router)
app.include_router(protected_routes.router)
app.include_router(demand_routes.router)
app.include_router(fare_routes.router)
app.include_router(zone_routes.router)

@app.get("/")
def root():
    return {"msg": "Welcome to SRDAPO API"}


from fastapi import FastAPI
from backend.api.routes import auth_routes, protected_routes, demand_routes, fare_routes, zone_routes
from backend.scheduler import start_scheduler

app = FastAPI(title="SRDAPO Backend")

# Include routers
app.include_router(auth_routes.router)
app.include_router(protected_routes.router)
app.include_router(demand_routes.router)
app.include_router(fare_routes.router)
app.include_router(zone_routes.router)

@app.on_event("startup")
async def startup_event():
    start_scheduler()

@app.get("/")
def root():
    return {"msg": "Welcome to SRDAPO API"}


from fastapi import FastAPI
from backend.api.routes import auth_routes, protected_routes, demand_routes, fare_routes, zone_routes, dashboard_routes
from backend.scheduler import start_scheduler
from backend.api.middleware.error_handler import ErrorHandlerMiddleware

app = FastAPI(title="SRDAPO Backend")

# Middleware
app.add_middleware(ErrorHandlerMiddleware)

# Routers
app.include_router(auth_routes.router)
app.include_router(protected_routes.router)
app.include_router(demand_routes.router)
app.include_router(fare_routes.router)
app.include_router(zone_routes.router)
app.include_router(dashboard_routes.router)

@app.on_event("startup")
async def startup_event():
    start_scheduler()

@app.get("/")
def root():
    return {"msg": "Welcome to SRDAPO API"}


from fastapi import FastAPI
from backend.api.routes import auth_routes, protected_routes, demand_routes, fare_routes, zone_routes, dashboard_routes
from backend.scheduler import start_scheduler
from backend.api.middleware.error_handler import ErrorHandlerMiddleware

app = FastAPI(title="SRDAPO Backend")

# ✅ Register middleware early
app.add_middleware(ErrorHandlerMiddleware)

# ✅ Include routers
app.include_router(auth_routes.router)
app.include_router(protected_routes.router)
app.include_router(demand_routes.router)
app.include_router(fare_routes.router)
app.include_router(zone_routes.router)
app.include_router(dashboard_routes.router)

@app.on_event("startup")
async def startup_event():
    start_scheduler()

@app.get("/")
def root():
    return {"msg": "Welcome to SRDAPO API"}
