from fastapi import FastAPI
from .database import engine, Base
from .routes import auth, users, products, orders, admin

app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(admin.router)

@app.on_event("startup")
async def startup():
    # Create database tables
    Base.metadata.create_all(bind=engine)