from fastapi.encoders import jsonable_encoder
from coupon.models import Coupon
from shop.models import Product
from config import settings


secret_key = settings.session_key


class Cart:

    def __init__(self, request, db):
        self.db = db
        cart = request.session.get(secret_key)  # here cart is the created session

        if not cart:
            cart = request.session[secret_key] = {}  # initializing a empty cart

        self.cart = cart
        self.coupon_id = request.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):  # adding and updating
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

    def remove(self, product):  # remove the product
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

    def remove_all(self):  # remove all the products from cart
        self.cart.clear()

    def __iter__(self):  # It makes the cart object iterable

        product_ids = list(self.cart.keys())
        products = self.db.query(Product).filter(
            Product.id.in_(product_ids)
        ).all()
        cart = self.cart.copy()

        for product in products:  # adding a key named 'product' and its value will be product info as of db
            cart[str(product.id)]['product'] = jsonable_encoder(product)

        for item in cart.values():  # adding a key named 'total_price' which will provide the total price of a product
            item['total_price'] = float((item['product']['price'])) * float(item['quantity'])

            yield item

    def get_total_price(self):  # This will return total price of cart
        return sum(float(item['product']['price']) * float(item['quantity']) for item in self.cart.values())

    @property
    def coupon(self):  # This method will return the coupon if it is applied
        if self.coupon_id:
            coupon_obj = self.db.query(Coupon).filter(Coupon.id == self.coupon_id).first()
            return coupon_obj
        return None

    def get_discount(self):  # This will calculate the discount
        if self.coupon:
            return float("{:.2f}".format((self.coupon.discount / float(100)) * self.get_total_price()))

        return float("{:.2f}".format(0))

    def get_total_price_after_discount(self):  # This is the final price after getting discount
        return float("{:.2f}".format(self.get_total_price() - self.get_discount()))
