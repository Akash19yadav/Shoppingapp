from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from User import OAuth2
from dependencies import get_db, templates, env
from shop import crud, models
from fastapi import APIRouter

app = FastAPI()
router = APIRouter(
    prefix="/product"
)


# This function will return all the products on shop page
@router.get("/")
def product_list(request: Request, category_slug: str = None, db: Session = Depends(get_db), page: int = 1,
                 current_user: int = Depends(OAuth2.get_current_user)):
    products = crud.product_list(db=db,
                                 category_slug=category_slug)[16 * (page - 1):16 * page]
    categories = db.query(models.Category).all()
    category = db.query(models.Category).filter(models.Category.slug == category_slug).first()  # None
    template = env.get_template('list.html')
    first_name = current_user.first_name
    return templates.TemplateResponse(template, {"request": request,
                                                 "page": page,
                                                 "msg": first_name,
                                                 "products": jsonable_encoder(products),
                                                 "category": jsonable_encoder(category),
                                                 "categories": jsonable_encoder(categories)})


# This function will return the products based on the category
@router.get("/{category_slug}")
def product_list(request: Request, category_slug: str, db: Session = Depends(get_db), page: int = 1,
                 current_user: int = Depends(OAuth2.get_current_user)):
    print("debug", category_slug)
    products = crud.product_list(db=db, category_slug=category_slug)[16 * (page - 1): 16 * (page)]
    categories = db.query(models.Category).all()
    category = db.query(models.Category).filter(models.Category.slug == category_slug).first()
    template = env.get_template('list.html')
    return templates.TemplateResponse(template, {"request": request,
                                                 "page": page,
                                                 "products": jsonable_encoder(products),
                                                 "category": jsonable_encoder(category),
                                                 "categories": jsonable_encoder(categories)})


# This function will return a particular product
@router.get("/{product_id}/{product_slug}")
def product_detail(request: Request, product_id: int, product_slug: str, db: Session = Depends(get_db),
                   current_user: int = Depends(OAuth2.get_current_user)):
    product = jsonable_encoder(crud.product_detail(db=db, id=product_id, slug=product_slug))
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product does not exist")

    template = env.get_template('detail.html')
    recommended_products = crud.product_list(db)
    return templates.TemplateResponse(template, {"request": request,
                                                 "recommended_products": recommended_products,
                                                 "product": jsonable_encoder(product)})
