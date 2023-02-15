from .base import Session
from .data import Order


async def update_cart(user_id: int, product_id: int, quantity: int):
    session = Session()
    cart = session.query(Order).filter(Order.user_id == user_id, Order.product_id == product_id).first()
    cart.quantity = quantity
    session.commit()
    session.close()
