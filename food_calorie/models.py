from django.db import models
from django.urls import reverse



class Vitamin(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        


    def __str__(self):
        return self.name


class Mineral(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]


    def __str__(self):
        return self.name




class Food(models.Model):
    name = models.CharField(max_length=100)
    serving = models.CharField(max_length=200)
    calories = models.PositiveIntegerField()
    protein  = models.DecimalField(max_digits=10, decimal_places=3,default=0)
    carbohydrate  = models.DecimalField(max_digits=10, decimal_places=3,default=0)
    fat = models.DecimalField(max_digits=10, decimal_places=3,default=0)
    vitamins=models.ManyToManyField(Vitamin, through="FoodVitamin")
    minerals=models.ManyToManyField(Mineral, through="FoodMineral")

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        


    def __str__(self):
        return self.name



class FoodVitamin(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    vitamin = models.ForeignKey(Vitamin, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    

class FoodMineral(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    mineral = models.ForeignKey(Mineral, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=3)

    
