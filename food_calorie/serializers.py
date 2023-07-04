from rest_framework import serializers

from .models import Food,Nutrient, FoodNutrient, Card, FoodCard
from django.db.models import Prefetch


class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Nutrient
        fields="__all__"

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields="__all__"

class FoodNutrientSerializer(serializers.ModelSerializer):
    nutrient=serializers.SerializerMethodField()
    
    def get_nutrient(self, obj):
        queryset = obj.nutrient
        return {queryset.groups:queryset.name}
        
    class Meta:
        model=FoodNutrient
        fields = ('nutrient','value')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        value=data['value']
        data=data['nutrient']
        data['value']=value
        return data



    
    

    

class FoodDetailedSerializer(serializers.ModelSerializer):
    nutrients=serializers.SerializerMethodField()
    

    def get_nutrients(self, obj):
        queryset = obj.nutrients.through.objects.filter(food=obj).select_related('nutrient')
        return FoodNutrientSerializer(queryset, many=True).data

    class Meta:
        model=Food
        fields=('id','name','serving','calories','protein','carbohydrate',
        'fat','nutrients')
       


class FoodCardSerializer(serializers.ModelSerializer):
    food=serializers.SerializerMethodField()
    
    def get_food(self, obj):
        queryset = obj.food
        return FoodDetailedSerializer(queryset).data

    class Meta:
        model=FoodCard
        fields = ('food','quantity')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        value=data['food']
        value.pop('id')
        value['quantity']=data['quantity']
        data=value
        return data


class CardSerializer(serializers.ModelSerializer):
    foods=serializers.SerializerMethodField()
    

    def get_foods(self, obj):
        queryset = obj.foods.through.objects.filter(card=obj).select_related('food')
        return FoodCardSerializer(queryset, many=True).data

    class Meta:
        model=Card
        fields=('id','name','foods',
                'total_calories',
                'total_proteins',
                'total_carbohydrates',
                'total_fats',
                'nutrients',           
        )