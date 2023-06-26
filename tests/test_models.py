import pytest

pytestmark = pytest.mark.django_db

class TestVitaminModel:
    def test_str_method(self,vitamin_factory):
        data=vitamin_factory(name='test')
        assert data.__str__() == "test"

class TestMineralModel:
    def test_str_method(self,mineral_factory):
        data=mineral_factory(name='test')
        assert data.__str__() == "test"

class TestFoodModel:
    def test_str_method(self,food_factory):
        data=food_factory(name='test')
        assert data.__str__() == "test"
        