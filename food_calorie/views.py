from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.db.models import Prefetch




from .models import Food, Nutrient, FoodNutrient,Card, FoodCard

from .serializers import NutrientSerializer,FoodNutrientSerializer,FoodSerializer,FoodDetailedSerializer \
,CardSerializer,FoodCardSerializer
class FoodView(viewsets.ViewSet):
    queryset=Food.objects.all()
    @extend_schema(responses=FoodSerializer)
    def list(self,request):
        serializer=FoodSerializer(self.queryset,many=True)
        return Response(serializer.data)

class NutrientView(viewsets.ViewSet):
    queryset=Nutrient.objects.all()

    
    def retrieve(self ,request, pk=None):
        serializer=NutrientSerializer(self.queryset.filter(id=pk),many=True)
        return Response(serializer.data)

    @extend_schema(responses=NutrientSerializer)
    def list(self,request):
        serializer=NutrientSerializer(self.queryset,many=True)
        return Response(serializer.data)

class FoodDetailView(viewsets.ViewSet):
   
    queryset=Food.objects.all()
    
    def retrieve(self ,request, pk=None):
        if pk.isdigit():
            serializer=FoodDetailedSerializer(self.queryset.filter(id=pk),many=True)
        else:
            serializer=FoodDetailedSerializer(self.queryset.filter(slug=pk),many=True)
        
        
    
        return Response(serializer.data)
    
    
    @extend_schema(responses=FoodDetailedSerializer)
    def list(self,request):
        serializer=FoodDetailedSerializer(self.queryset,many=True)
        return Response(serializer.data)


class CardView(viewsets.ViewSet):
   
    queryset=Card.objects.all()
    
    def retrieve(self ,request, pk=None):

        serializer=CardSerializer(self.queryset.filter(id=pk),many=True)
        
        
        return Response(serializer.data)



