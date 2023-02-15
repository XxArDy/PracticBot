from .base import Session
from .data import Order
from .get import get_one_quantity
from .update import update_cart


async def add_order(user_id: int, product_id: int):
    session = Session()
    count = await get_one_quantity(user_id, product_id)
    if count is None:
        session.add(Order(user_id, product_id, 1))
        session.commit()
    else:
        await update_cart(user_id, product_id, count + 1)
    session.close()
