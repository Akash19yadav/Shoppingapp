from fastapi import APIRouter, Request, Depends, Form, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from cart.cart import Cart
from dependencies import get_db, env, templates
from shop import models, crud
from User import OAuth2

router = APIRouter(
    prefix="/cart"
)


@router.get("/")
def cart_detail(request: Request,
                msg: str = None,  # This message is coming through url if coupon is invalid
                db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
    cart = Cart(request, db)

    template = env.get_template('cart.html')
    recommended_products = crud.product_list(db)
    return templates.TemplateResponse(template, {"request": request,
                                                 "coupon_msg": msg,
                                                 "cart": cart,
                                                 "recommended_products": recommended_products})


@router.post("/add")
def cart_add(request: Request,
             db: Session = Depends(get_db),
             id: int = Form(...),
             quantity: int = Form(...),
             update: bool = Form(...),
             current_user: int = Depends(OAuth2.get_current_user)):
    cart = Cart(request, db)
    product = db.query(models.Product).filter_by(id=id).first()
    cart.add(product=product, quantity=quantity, update_quantity=update)

    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/remove/{id}")
def cart_remove(request: Request,
                id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(OAuth2.get_current_user)):
    cart = Cart(request, db)
    product = db.query(models.Product).filter_by(id=id).first()
    cart.remove(product)

    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/remove_all")
def cart_remove_all(request: Request,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(OAuth2.get_current_user)):
    cart = Cart(request, db)
    cart.remove_all()

    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)
