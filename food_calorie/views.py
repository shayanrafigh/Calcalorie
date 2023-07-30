from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.db.models import Prefetch
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import status





from .models import Food, Nutrient, FoodNutrient,Card, FoodCard

from .serializers import NutrientSerializer,FoodNutrientSerializer,FoodSerializer,FoodDetailedSerializer \
,CardSerializer,FoodCardSerializer




class FoodView(viewsets.ViewSet):
    queryset=Food.objects.all()
    @extend_schema(responses=FoodSerializer)
    def list(self,request):
        serializer=FoodSerializer(self.queryset,many=True)
        return Response(serializer.data)

class NutrientView(viewsets.ModelViewSet):
    queryset=Nutrient.objects.all()
    serializer_class=NutrientSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    
    def retrieve(self ,request, pk=None):
        serializer=self.serializer_class(get_object_or_404(self.queryset,id=pk))
        return Response(serializer.data)

    @extend_schema(responses=NutrientSerializer)
    def list(self, request):
        nutrients = self.queryset.all()
        page = self.paginate_queryset(nutrients)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(nutrients, many=True)
        return Response(serializer.data)
    
    @extend_schema(responses=NutrientSerializer)
    @action(
        methods=['get'],
        detail=False,
        url_path=r'all',
        url_name='all',
    )
    def list_by_filter(self,request):
        nutrient=self.queryset.all()
        serializer=self.serializer_class(nutrient,many=True)
        return Response(serializer.data)
    
        
        
    


class FoodDetailView(viewsets.ModelViewSet):

    queryset=Food.objects.prefetch_related('food_nutrient__nutrient')

    serializer_class=FoodDetailedSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
       
    
    def retrieve(self ,request, pk=None):

        if pk.isdigit():
            serializer=self.serializer_class(get_object_or_404(self.queryset,id=pk))
        else:
            serializer=self.serializer_class(get_object_or_404(self.queryset,slug=pk))
        
        return Response(serializer.data)
    
    def create(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

    
    @extend_schema(responses=FoodDetailedSerializer)
    def list(self,request):
        
        foods = self.queryset.all()
        
        page = self.paginate_queryset(foods)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            
            return self.get_paginated_response(serializer.data)
        

        serializer=self.serializer_class(self.queryset,many=True)
        return Response(serializer.data)
        
        


    
    @action(
        methods=['get'],
        detail=False,
        url_path=r'nutrient/(?P<nutrient>[\w-]+)',
        url_name='all',
    )
    def list_by_filter(self,request,nutrient=None):
        if nutrient.isdigit():
            serializer=self.serializer_class(self.queryset.filter(nutrients__id=nutrient),many=True)
        else:
            serializer=self.serializer_class(self.queryset.filter(nutrients__name=nutrient),many=True)
        return Response(serializer.data)


class CardView(viewsets.ModelViewSet):
   
    queryset=Card.objects.prefetch_related('food_card__food__food_nutrient__nutrient').all()
    serializer_class=CardSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    
    @extend_schema(responses=CardSerializer)
    def retrieve(self ,request, pk=None):
        serializer=self.serializer_class(get_object_or_404(self.queryset,id=pk))
        return Response(serializer.data)
    
    def create(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
    
    @extend_schema(responses=CardSerializer)
    def list(self,request):
        cards = self.queryset.all()
        page = self.paginate_queryset(cards)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer=self.serializer_class(self.queryset,many=True)
        return Response(serializer.data)



