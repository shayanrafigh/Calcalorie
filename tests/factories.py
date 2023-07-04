import factory
from food_calorie.models import Food,Nutrient

class NutrientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Nutrient
    
    name='test'

class FoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Food
    
    name='test'
    serving = '100gr'
    calories = 1
