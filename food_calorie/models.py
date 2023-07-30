from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator
import json
from decimal import Decimal



class Nutrient(models.Model):
    TYPE = [
    ("Vitamin", "vitamin"),
    ("Mineral", "mineral"),
    ("Others", "others"),
    ]
    name = models.CharField(max_length=300, unique=True)
    groups = models.CharField(
        max_length=10,
        choices=TYPE,
        default='Others',
    )
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        


    def __str__(self):
        return self.name




class Food(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=300 ,default='slug')
    serving = models.CharField(max_length=200)
    calories = models.DecimalField(max_digits=12, decimal_places=4,default=0,validators=[MinValueValidator(0)])
    protein  = models.DecimalField(max_digits=12, decimal_places=4,default=0,validators=[MinValueValidator(0)])
    carbohydrate  = models.DecimalField(max_digits=12, decimal_places=4,default=0,validators=[MinValueValidator(0)])
    fat = models.DecimalField(max_digits=12, decimal_places=4,default=0,validators=[MinValueValidator(0)])
    nutrients =models.ManyToManyField(Nutrient, through="FoodNutrient",related_name="foods",blank=True
)
    

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        


class FoodNutrient(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE,related_name="food_nutrient")
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE,related_name="food_nutrient")
    value =  models.DecimalField(max_digits=12, decimal_places=4,default=0,validators=[MinValueValidator(0)])
    
    class Meta:
        unique_together=('food','nutrient')

class Card(models.Model):
    name = models.CharField(max_length=100, unique=True)
    foods = models.ManyToManyField(Food, through="FoodCard",related_name="cards",blank=True)
    total_calories = models.DecimalField(max_digits=12, decimal_places=4,default=0,validators=[MinValueValidator(0)])
    total_proteins = models.DecimalField(max_digits=12, decimal_places=4,default=0,validators=[MinValueValidator(0)])
    total_carbohydrates = models.DecimalField(max_digits=12, decimal_places=4,default=0,validators=[MinValueValidator(0)])
    total_fats = models.DecimalField(max_digits=12, decimal_places=4,default=0,validators=[MinValueValidator(0)])
    def nutrients_default():
        return {}
    nutrients = models.JSONField(default=nutrients_default,blank=True)
    
    
    
    
    def __str__(self):
        return self.name
 
    
    
  
class FoodCard(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE,related_name="food_card")
    card = models.ForeignKey(Card, on_delete=models.CASCADE,related_name="food_card")
    quantity = models.PositiveIntegerField(default=1)
    
    
    class Meta:
        unique_together=('food','card')
    
    
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
        self.card.total_calories = sum([i.quantity * i.food.calories for i in self.card.food_card.all()])
        self.card.total_proteins = sum([i.quantity * i.food.protein for i in self.card.food_card.all()]) 
        self.card.total_carbohydrates = sum([i.quantity * i.food.carbohydrate for i in self.card.food_card.all()])
        self.card.total_fats = sum([i.quantity * i.food.fat for i in self.card.food_card.all()])

        self.card.nutrients={}
        quantity=0
        for foods in self.card.food_card.all():  
            quantity=foods.quantity
            for n in foods.food.food_nutrient.all():

                if self.card.nutrients.get(n.nutrient.name) is not None:
                    self.card.nutrients[n.nutrient.name]=float(self.card.nutrients[n.nutrient.name])+(float(n.value)*quantity)
                else:
                    self.card.nutrients[n.nutrient.name]=float(n.value)*quantity
                
                      
        self.card.save()
        
        
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.card.total_calories = sum([i.quantity * i.food.calories for i in self.card.food_card.all()])
        self.card.total_proteins = sum([i.quantity * i.food.protein for i in self.card.food_card.all()])    
        self.card.total_carbohydrates = sum([i.quantity * i.food.carbohydrate for i in self.card.food_card.all()])
        self.card.total_fats = sum([i.quantity * i.food.fat for i in self.card.food_card.all()])
            
        self.card.nutrients={}
        quantity=0
        for foods in self.card.food_card.all():  
            quantity=foods.quantity
            for n in foods.food.food_nutrient.all():

                if self.card.nutrients.get(n.nutrient.name) is not None:
                    self.card.nutrients[n.nutrient.name]=float(self.card.nutrients[n.nutrient.name])+(float(n.value)*quantity)
                else:
                    self.card.nutrients[n.nutrient.name]=float(n.value)*quantity
            
        self.card.save()
        
        
        

    
    
    
    

    
