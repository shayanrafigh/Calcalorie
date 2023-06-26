from pytest_factoryboy import register

from .factories import VitaminFactory, MineralFactory, FoodFactory

register(VitaminFactory)

register(MineralFactory)

register(FoodFactory)

