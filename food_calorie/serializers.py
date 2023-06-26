from rest_framework import serializers

from .models import Food,Mineral,Vitamin,FoodVitamin,FoodMineral

class VitaminSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vitamin
        fields="__all__"

class MineralSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mineral
        fields="__all__"


class FoodVitaminSerializer(serializers.ModelSerializer):
    vitamin = serializers.StringRelatedField()
    class Meta:
        model=FoodVitamin
        fields = ('vitamin','value')

class FoodMineralSerializer(serializers.ModelSerializer):
    mineral = serializers.StringRelatedField()
    class Meta:
        model=FoodMineral
        fields = ('mineral','value')


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields="__all__"

class FoodDetailedSerializer(serializers.ModelSerializer):
    vitamins=serializers.SerializerMethodField()
    minerals=serializers.SerializerMethodField()

    def get_vitamins(self, obj):
        queryset = obj.vitamins.through.objects.filter(food=obj)
        return FoodVitaminSerializer(queryset, many=True).data
    
    def get_minerals(self, obj):
        queryset = obj.minerals.through.objects.filter(food=obj)
        return FoodMineralSerializer(queryset, many=True).data

    class Meta:
        model=Food
        fields=('id','name','serving','calories','protein','carbohydrate',
        'fat','vitamins','minerals')
       



