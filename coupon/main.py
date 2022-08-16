import datetime

from fastapi import APIRouter, Request, Depends, Form, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from User import OAuth2
from coupon.models import Coupon
from dependencies import get_db

router = APIRouter(
    prefix='/coupon'
)


# This method will apply the coupon i.e. It will save the coupon id into session
@router.post("/apply")
def coupon_apply(request: Request, db: Session = Depends(get_db),
                 code: str = Form(...),
                 current_user: int = Depends(OAuth2.get_current_user)):
    now = datetime.datetime.now()
    coupon = db.query(Coupon).filter(Coupon.code == code,
                                     Coupon.valid_from.__le__(now),
                                     Coupon.valid_to.__ge__(now),
                                     Coupon.active == True).first()
    if coupon is None:
        return RedirectResponse(url="/cart?msg=Coupon Invalid", status_code=status.HTTP_303_SEE_OTHER)
    request.session['coupon_id'] = coupon.id
    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)


# This method will remove the coupon i.e. It will clear the session regarding coupon
@router.get("/remove")
def coupon_apply(request: Request, current_user: int = Depends(OAuth2.get_current_user)):
    request.session['coupon_id'] = None
    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)
