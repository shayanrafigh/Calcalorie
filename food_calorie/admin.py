from django.contrib import admin

from .models import Food, Nutrient, FoodNutrient , Card,FoodCard

class FoodNutrientInline(admin.TabularInline):
    model=FoodNutrient

class FoodCardInline(admin.TabularInline):
    model=FoodCard
    
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    inlines=[FoodNutrientInline]

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    inlines=[FoodCardInline]

admin.site.register(Nutrient)
admin.site.register(FoodNutrient)
admin.site.register(FoodCard)
