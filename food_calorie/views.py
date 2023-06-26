from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Food, Vitamin, Mineral
from .serializers import FoodSerializer,FoodDetailedSerializer,VitaminSerializer,MineralSerializer

class FoodView(viewsets.ViewSet):
    queryset=Food.objects.all()
    @extend_schema(responses=FoodSerializer)
    def list(self,request):
        serializer=FoodSerializer(self.queryset,many=True)
        return Response(serializer.data)

class VitaminView(viewsets.ViewSet):
    queryset=Vitamin.objects.all()
    @extend_schema(responses=VitaminSerializer)
    def list(self,request):
        serializer=VitaminSerializer(self.queryset,many=True)
        return Response(serializer.data)

class MineralView(viewsets.ViewSet):
    queryset=Mineral.objects.all()
    @extend_schema(responses=MineralSerializer)
    def list(self,request):
        serializer=MineralSerializer(self.queryset,many=True)
        return Response(serializer.data)

class FoodDetailView(viewsets.ViewSet):
    queryset=Food.objects.all()
    @extend_schema(responses=FoodDetailedSerializer)
    def list(self,request):
        serializer=FoodDetailedSerializer(self.queryset,many=True)
        return Response(serializer.data)


