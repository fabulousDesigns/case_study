from fastapi import FastAPI

from app.routes import customers, orders, token_router

app = FastAPI()

app.include_router(token_router.router, tags=["token"], prefix="/api")
app.include_router(customers.router, tags=["customers"], prefix="/api")
app.include_router(orders.router, tags=["orders"], prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
