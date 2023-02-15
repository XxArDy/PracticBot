from .base import Session
from .data import Order
from .get import check_order_exists


def add_order(user_id: int, product_id: int):
    session = Session()
    if check_order_exists(user_id, product_id) is None:
        session.add(Order(user_id, product_id, 0))
        session.commit()
    session.close()
