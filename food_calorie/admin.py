from django.contrib import admin

from .models import Food,Mineral,Vitamin,FoodVitamin,FoodMineral

admin.site.register(Food)

admin.site.register(Mineral)

admin.site.register(Vitamin)

admin.site.register(FoodVitamin)

admin.site.register(FoodMineral)