from .base import Session
from .data import Order


def update_cart(user_id: int, product_id: int, quantity: int):
    session = Session()
    cart = session.query(Order).filter_by(user_id = user_id, product_id = product_id).first()
    cart.quantity = quantity
    session.commit()
    session.close()
