from .base import Session
from .data import Order


async def delete_order(user_id: int):
    session = Session()
    session.query(Order).where(Order.user_id == user_id).delete()
    session.commit()
    session.close()


async def remove_one_item(user_id: int, product_id: int):
    session = Session()
    session.query(Order).where(Order.user_id == user_id, Order.product_id == product_id).delete()
    session.commit()
    session.close()
