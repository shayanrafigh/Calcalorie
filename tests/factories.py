import factory
from food_calorie.models import Food,Mineral,Vitamin

class VitaminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Vitamin
    
    name='test'

class MineralFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Mineral
    
    name='test'


class FoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Food
    
    name='test'
    serving = '100gr'
    calories = 1
