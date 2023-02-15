from .base import Session
from .data import Product, Order


def get_all_product():
    session = Session()
    products = session.query(Product).all()
    session.close()
    return products


def get_product_by_name(product_name):
    session = Session()
    product = session.query(Product).filter_by(name=product_name).one()
    session.close()
    return product


def get_product_by_id(product_id: int):
    try:
        session = Session()
        product = session.query(Product).filter_by(id=product_id).one()
        session.close()
        return product
    except:
        return None


def check_order_exists(user_id: int, product_id: int):
    try:
        session = Session()
        product = session.query(Order).filter(Order.user_id == user_id, Order.product_id == product_id).one()
        session.close()
        return product
    except:
        return None

