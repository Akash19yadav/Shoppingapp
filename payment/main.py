from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from dependencies import env, templates, get_db
from orders.models import Order
from User import OAuth2

router = APIRouter(
    prefix="/payment"
)


# This will be called if something goes wrong
@router.get("/canceled")
def cancel_payment(request: Request):
    template = env.get_template("canceled.html")
    return templates.TemplateResponse(template, {"request": request})


# This function will be called if payment will be successful
@router.get("/done")
def success_payment(request: Request, db: Session = Depends(get_db)):
    order_id = request.session.get('order_id')
    order = db.query(Order).filter_by(id=order_id).first()
    order.is_paid = True
    db.commit()
    db.refresh(order)

    template = env.get_template("done.html")
    return templates.TemplateResponse(template, {"request": request})

