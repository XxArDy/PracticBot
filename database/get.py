from .base import Session
from .data import Product, Order


async def get_all_product():
    session = Session()
    products = session.query(Product).all()
    session.close()
    return products


async def get_product_by_name(product_name):
    session = Session()
    product = session.query(Product).filter(Product.name == product_name).one()
    session.close()
    return product


async def get_product_by_id(product_id: int):
    try:
        session = Session()
        product = session.query(Product).filter(Product.id == product_id).one()
        session.close()
        return product
    except:
        return None


async def get_order(user_id: int):
    session = Session()
    product = session.query(Order).filter(Order.user_id == user_id).all()
    session.close()
    return product


async def get_quantity(user_id: int, product_id: int):
    session = Session()
    product = session.query(Order).filter(Order.user_id == user_id, Order.product_id == product_id).all()
    session.close()
    return product


async def get_one_quantity(user_id: int, product_id: int):
    try:
        session = Session()
        product = session.query(Order).filter(Order.user_id == user_id, Order.product_id == product_id).one().quantity
        session.close()
        return product
    except:
        return None

