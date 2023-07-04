from pytest_factoryboy import register

from .factories import NutrientFactory, FoodFactory

register(NutrientFactory)

register(FoodFactory)

