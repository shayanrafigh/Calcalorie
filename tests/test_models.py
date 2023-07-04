import pytest

pytestmark = pytest.mark.django_db

class TestNutrientModel:
    def test_str_method(self,nutrient_factory):
        data= nutrient_factory(name='test')
        assert data.__str__() == "test"


class TestFoodModel:
    def test_str_method(self,food_factory):
        data=food_factory(name='test')
        assert data.__str__() == "test"
        