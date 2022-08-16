from sqlalchemy.orm import Session
from fastapi import Depends
from dependencies import get_db
from shop import models


# This function will return all the products if slug is not given otherwise returns only filtered product
def product_list(db: Session = Depends(get_db), category_slug: str = None):
    if category_slug:
        category_related = db.query(models.Category).filter_by(slug=category_slug).first()
        return db.query(models.Product).filter(models.Product.category_related == category_related).all()
    return db.query(models.Product).all()


# This function will return the detail of a particular product
def product_detail(db, id: int, slug: str):
    product = db.query(models.Product).filter_by(id=id, slug=slug).first()
    return product
