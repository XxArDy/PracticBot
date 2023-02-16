from .base import Session, engine, Base
from .data import Product, Order

import os


class Database:
    # region get
    async def get_all_product(self):
        session = Session()
        products = session.query(Product).all()
        session.close()
        return products

    async def get_product_by_name(self, product_name):
        session = Session()
        product = session.query(Product).filter(Product.name == product_name).one()
        session.close()
        return product

    async def get_product_by_id(self, product_id: int):
        try:
            session = Session()
            product = session.query(Product).filter(Product.id == product_id).one()
            session.close()
            return product
        except:
            return None

    async def get_order(self, user_id: int):
        session = Session()
        product = session.query(Order).filter(Order.user_id == user_id).all()
        session.close()
        return product

    async def get_quantity(self, user_id: int, product_id: int):
        session = Session()
        product = session.query(Order).filter(Order.user_id == user_id, Order.product_id == product_id).all()
        session.close()
        return product

    async def get_one_quantity(self, user_id: int, product_id: int):
        try:
            session = Session()
            product = session.query(Order).filter(Order.user_id == user_id,
                                                  Order.product_id == product_id).one().quantity
            session.close()
            return product
        except:
            return None
    # endregion

    # region add
    async def add_order(self, user_id: int, product_id: int):
        session = Session()
        count = await self.get_one_quantity(user_id, product_id)
        if count is None:
            session.add(Order(user_id, product_id, 1))
            session.commit()
        else:
            await self.update_cart(user_id, product_id, count + 1)
        session.close()
    # endregion

    # region create
    def create_base(self):
        if os.path.exists('sweet.db'):
            os.remove('sweet.db')
        Base.metadata.create_all(engine)

    def generate_product(self):
        session = Session()
        session.add(Product("Toxic Waste", 20, 100,
                            "Унікальні цукерки з непередавано кислим смаком і з дизайном бочки для токсичних відходів."))
        session.add(Product("SOUR FLUSH", 40, 90,
                            "Час дивних солодощів! SOUR FLUSH – американська солодкість у формі туалету з кислим "
                            "наповнювачем всередині і двома льодяниками-вантузами"))
        session.add(Product("KitKat Wasabi", 12, 70,
                            "Вафлі Kit Kat з додаванням високоякісного фірмового васабі з Tamaruya Honten -  "
                            "магазину васабі з  Японії."))
        session.add(Product("Bean Boozled", 45, 150,
                            "Достатньо купити Бін Бузлд всього одну невелику пачку, щоб зробити будь-яку зустріч із друзями"
                            " трохи крутішими, веселішими. Можна робити ставки, який боб Jelly Belly дістанеться наступному"
                            " бажаючому ризикнути."))
        session.add(Product("Naruto Shippuden Japanese Melon Mochi", 180, 500,
                            "Улюблений японський десерт разом з культовим аніме! Класичні тістечка моті зі смаком дині "
                            "в лімітованій упаковці з улюбленими персонажами аніме Наруто."))
        session.commit()
        session.close()
    # endregion

    # region update
    async def update_cart(self, user_id: int, product_id: int, quantity: int):
        session = Session()
        cart = session.query(Order).filter(Order.user_id == user_id, Order.product_id == product_id).first()
        cart.quantity = quantity
        session.commit()
        session.close()
    # endregion

    # region delete
    async def delete_order(self, user_id: int):
        session = Session()
        session.query(Order).where(Order.user_id == user_id).delete()
        session.commit()
        session.close()

    async def remove_one_item(self, user_id: int, product_id: int):
        session = Session()
        session.query(Order).where(Order.user_id == user_id, Order.product_id == product_id).delete()
        session.commit()
        session.close()
    # endregion
