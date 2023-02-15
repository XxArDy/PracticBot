import os

from .base import Session, engine, Base
from .data import Product


def create_base():
    if os.path.exists('sweet.db'):
        os.remove('sweet.db')
    Base.metadata.create_all(engine)


def generate_product():
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
    session.add(Product("Naruto Limited Edition Melon Mochi", 180, 500,
                        "Улюблений японський десерт разом з культовим аніме! Класичні тістечка моті зі смаком дині "
                        "в лімітованій упаковці з улюбленими персонажами аніме Наруто."))
    session.commit()
    session.close()
