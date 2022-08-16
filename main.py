from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

# import admin.main
from context_processors import CartMiddleware
from dependencies import env
import cart
import shop
import orders
import payment
import coupon
import psycopg2
from psycopg2.extras import RealDictCursor
# import admin
import User
# from admin import main
from shop import main, models
from cart import main
from orders import main, models
from coupon import main, models
from payment import main
from database import engine
from User import main
from context_processors import CartMiddleware
from config import settings


secret_key = settings.session_key

middleware = [
    Middleware(SessionMiddleware, secret_key=secret_key),
    Middleware(CartMiddleware)
]

app = FastAPI(middleware=middleware)

env.globals["cart_context"] = CartMiddleware.cart

app.mount("/static", StaticFiles(directory="static"), name="static")

# shop.models.Base.metadata.create_all(bind=engine)
# orders.models.Base.metadata.create_all(bind=engine)
# coupon.models.Base.metadata.create_all(bind=engine)

# routers
app.include_router(shop.main.router)
app.include_router(cart.main.router)
app.include_router(orders.main.router)
app.include_router(payment.main.router)
app.include_router(coupon.main.router)
# app.include_router(admin.main.router)
app.include_router(User.main.router)
