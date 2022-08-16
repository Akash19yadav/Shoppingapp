from fastapi import Depends, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session

from dependencies import get_db
from orders.models import Order, OrderItem


# This method will save the details of order into database
def create_order(db: Session = Depends(get_db),
                 first_name: str = Form(...),
                 last_name: str = Form(...),
                 email: EmailStr = Form(...),
                 address: str = Form(...),
                 postal_code: int = Form(...),
                 city: str = Form(...),
                 coupon_id: int = None,
                 discount: float = 0,
                 total_price: float = 0,
                 user_id: int = 0):

    db_order = Order(first_name=first_name,
                     last_name=last_name,
                     email=email,
                     address=address,
                     postal_code=postal_code,
                     city=city,
                     coupon_id=coupon_id,
                     discount=discount,
                     total_price=total_price,
                     user_id=user_id)
    print(db_order.discount)
    print(db_order.total_price)

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


# This method will provide the info regarding products associated to a particular order
def create_order_item(item, order_id, product_id, db: Session = Depends(get_db)):
    order_item = OrderItem(order_id=order_id,
                           product_id=product_id,
                           price=item['product']['price'],
                           quantity=item['quantity'], )

    db.add(order_item)
    db.commit()
    db.refresh(order_item)

    return order_item
