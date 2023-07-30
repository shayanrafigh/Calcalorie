from rest_framework import serializers

from .models import Food,Nutrient, FoodNutrient, Card, FoodCard
from django.db.models import Prefetch
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Nutrient
        fields="__all__"

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields="__all__"

class FoodNutrientSerializer(serializers.ModelSerializer):
    
    nutrient=NutrientSerializer()

        
    class Meta:
        model=FoodNutrient
        fields = ('nutrient','value')
        
     
    def to_representation(self, instance):
        data = super().to_representation(instance)
        value=data['value']
        data=data['nutrient']
        Type=data['groups']
        name=data['name']
        data={}
        data['name']=name
        data['type']=Type
        data['value']=value
        return data




    
    

    

class FoodDetailedSerializer(serializers.ModelSerializer):

    nutrients=serializers.SerializerMethodField()
    
    def get_nutrients(self, obj):
        queryset = obj.food_nutrient
        serializer = FoodNutrientSerializer(queryset, many=True)
        return serializer.data
    

    class Meta:
        model=Food
        fields=('id','name','serving','calories','protein','carbohydrate',
        'fat','nutrients')
    
     
    def create(self, validated_data):
        if 'nutrients' in self.initial_data:
            with transaction.atomic():
                food = Food.objects.create(**validated_data)            
                for nutrient in self.initial_data['nutrients']:
                    nutrient_obj=Nutrient.objects.get(pk=nutrient['id'])
                    FoodNutrient.objects.create(food=food,nutrient=nutrient_obj,value=nutrient['value'])
                return food
        else:
            food = Food.objects.create(**validated_data)
            return food
    
    def update(self,instance,validated_data):     
        if 'nutrients' in self.initial_data:
            with transaction.atomic():           
                f=FoodNutrient.objects.filter(food=instance)
                f.delete()
                super().update(instance,validated_data)
                for nutrient in self.initial_data['nutrients']:            
                    nutrient_obj=Nutrient.objects.get(pk=nutrient['id'])                   
                    FoodNutrient.objects.create(food=instance,nutrient=nutrient_obj,value=nutrient['value'])                 
                return instance
        else:
            return super().update(instance,validated_data)
            
            
    
       


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
        queryset = obj.food_card
        serializer = FoodCardSerializer(queryset, many=True)
        return serializer.data
    

    
    def to_representation(self, instance):
        data = super().to_representation(instance)       
        foods=data['foods']
        a=[]
        for i in data['foods']:
            a.append(i['name'])
        data['foods']=a
        
        return data
    
    class Meta:
        model=Card
        fields=('id','name','foods',
                'total_calories',
                'total_proteins',
                'total_carbohydrates',
                'total_fats',
                'nutrients',           
        )
    
    def create(self, validated_data):
        if 'foods' in self.initial_data:
            with transaction.atomic():
                card = Card.objects.create(**validated_data)            
                for food in self.initial_data['foods']:
                    food_obj=Food.objects.get(pk=food['id'])
                    FoodCard.objects.create(food=food_obj,card=card,quantity=food['quantity'])
                return card
        else:
            card = Card.objects.create(**validated_data)
            return card
        
    def update(self,instance,validated_data):     
        if 'foods' in self.initial_data:
            with transaction.atomic():           
                c=FoodCard.objects.filter(card=instance)
                c.delete()
                super().update(instance,validated_data)
                for food in self.initial_data['foods']:
                    food_obj=Food.objects.get(pk=food['id'])
                    FoodCard.objects.create(food=food_obj,card=instance,quantity=food['quantity'])
                return instance
        else:
            return super().update(instance,validated_data)
        
    